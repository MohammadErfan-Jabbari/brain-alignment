#!/usr/bin/env python3
"""Build a metadata-only acquisition manifest for E028.

This script reads remote object listings and small descriptive metadata. It does
not download neural time series, audio, model weights, checkpoints, or result
tables, and it does not inspect any endpoint value.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "outputs" / "E028" / "acquisition_manifest.json"
OPENNEURO_BUCKET = "https://s3.amazonaws.com/openneuro.org"
ECOG_DATASET = "ds005574"
FMRI_DATASET = "ds003020"
EXPECTED_ECOG_DOI = "doi:10.18112/openneuro.ds005574.v1.0.2"
EXPECTED_ECOG_LICENSE = "CC0"
EXPECTED_ECOG_PARTICIPANTS = 9
EXPECTED_ECOG_HIGHGAMMA_FILES = 9

HIGHGAMMA_RE = re.compile(
    r"^ds005574/derivatives/ecogprep/sub-\d{2}/ieeg/"
    r"sub-\d{2}_task-podcast_desc-highgamma_ieeg\.fif$"
)
SUBJECT_METADATA_RE = re.compile(
    r"^ds005574/sub-\d{2}/ieeg/sub-\d{2}_(?:"
    r"task-podcast_channels\.tsv|task-podcast_ieeg\.json|"
    r"space-MNI152NLin2009aSym_electrodes\.tsv|"
    r"space-MNI152NLin2009aSym_coordsystem\.json)$"
)
SMALL_DATASET_KEYS = {
    "ds005574/CHANGES",
    "ds005574/README",
    "ds005574/dataset_description.json",
    "ds005574/environment.yml",
    "ds005574/participants.json",
    "ds005574/participants.tsv",
    "ds005574/stimuli/podcast_transcript.csv",
}
PODCAST_AUDIO_KEY = "ds005574/stimuli/podcast.wav"


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fetch_bytes(url: str, timeout: int = 30) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "brain-alignment-e028-metadata-audit/1.0"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def fetch_json(url: str) -> dict[str, Any]:
    return json.loads(fetch_bytes(url).decode("utf-8"))


def s3_listing(dataset: str) -> list[dict[str, Any]]:
    query = urllib.parse.urlencode(
        {"list-type": "2", "prefix": f"{dataset}/", "max-keys": "1000"}
    )
    payload = fetch_bytes(f"{OPENNEURO_BUCKET}?{query}")
    root = ET.fromstring(payload)
    namespace = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}
    truncated = root.findtext("s3:IsTruncated", namespaces=namespace)
    if truncated != "false":
        raise RuntimeError(
            f"{dataset} listing is truncated; pagination must be implemented before use"
        )

    objects: list[dict[str, Any]] = []
    for content in root.findall("s3:Contents", namespace):
        key = content.findtext("s3:Key", namespaces=namespace)
        size = content.findtext("s3:Size", namespaces=namespace)
        etag = content.findtext("s3:ETag", namespaces=namespace)
        modified = content.findtext("s3:LastModified", namespaces=namespace)
        if key is None or size is None:
            raise RuntimeError("Malformed OpenNeuro S3 listing entry")
        objects.append(
            {
                "key": key,
                "size_bytes": int(size),
                "remote_etag_not_sha256": etag.strip('"') if etag else None,
                "last_modified": modified,
                "sha256_after_acquisition": None,
            }
        )
    return objects


def remote_small_metadata(dataset: str, names: list[str]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for name in names:
        payload = fetch_bytes(f"{OPENNEURO_BUCKET}/{dataset}/{name}")
        result[name] = {
            "url": f"{OPENNEURO_BUCKET}/{dataset}/{name}",
            "size_bytes": len(payload),
            "sha256": sha256_bytes(payload),
        }
        if name == "dataset_description.json":
            result[name]["parsed"] = json.loads(payload.decode("utf-8"))
    return result


def github_head(repository: str) -> dict[str, Any]:
    url = f"https://api.github.com/repos/{repository}/commits/main"
    data = fetch_json(url)
    return {
        "repository": f"https://github.com/{repository}",
        "commit": data["sha"],
        "committed_at": data["commit"]["committer"]["date"],
        "archive_sha256_after_acquisition": None,
    }


def git_head(path: Path) -> str | None:
    if not (path / ".git").exists():
        return None
    result = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def local_lebel_coverage() -> dict[str, Any]:
    root = ROOT / "data" / "lebel_ds003020"
    coverage: dict[str, Any] = {
        "root": str(root),
        "neural_values_opened": False,
        "subjects": {},
    }
    for subject in ("UTS01", "UTS02", "UTS03"):
        subject_dir = root / "preprocessed_data" / subject
        files = sorted(subject_dir.glob("*.hf5")) if subject_dir.exists() else []
        coverage["subjects"][subject] = {
            "file_count": len(files),
            "total_size_bytes_from_stat": sum(path.stat().st_size for path in files),
            "filenames": [path.name for path in files],
            "content_sha256": None,
        }

    textgrids = sorted((root / "derivatives" / "TextGrids").glob("*"))
    audio = sorted((ROOT / "data" / "stimuli_wav").glob("*.wav"))
    coverage["textgrid_file_count"] = sum(path.is_file() for path in textgrids)
    coverage["audio_file_count"] = len(audio)
    coverage["audio_filenames"] = [path.name for path in audio]
    return coverage


def build_manifest() -> dict[str, Any]:
    ecog_objects = s3_listing(ECOG_DATASET)
    ecog_metadata = remote_small_metadata(
        ECOG_DATASET,
        ["dataset_description.json", "README", "participants.tsv", "CHANGES"],
    )
    fmri_metadata = remote_small_metadata(
        FMRI_DATASET,
        ["dataset_description.json", "CHANGES"],
    )

    description = ecog_metadata["dataset_description.json"]["parsed"]
    participants = fetch_bytes(
        f"{OPENNEURO_BUCKET}/{ECOG_DATASET}/participants.tsv"
    ).decode("utf-8")
    participant_rows = [
        line for line in participants.splitlines()[1:] if line.strip()
    ]

    highgamma = [item for item in ecog_objects if HIGHGAMMA_RE.match(item["key"])]
    acquisition_objects = [
        item
        for item in ecog_objects
        if (
            item["key"] in SMALL_DATASET_KEYS
            or item["key"] == PODCAST_AUDIO_KEY
            or HIGHGAMMA_RE.match(item["key"])
            or SUBJECT_METADATA_RE.match(item["key"])
        )
    ]
    acquisition_objects.sort(key=lambda item: item["key"])

    checks = {
        "ecog_listing_not_truncated": True,
        "ecog_dataset_doi_matches": description.get("DatasetDOI")
        == EXPECTED_ECOG_DOI,
        "ecog_license_matches": description.get("License")
        == EXPECTED_ECOG_LICENSE,
        "ecog_participant_count_matches": len(participant_rows)
        == EXPECTED_ECOG_PARTICIPANTS,
        "ecog_highgamma_file_count_matches": len(highgamma)
        == EXPECTED_ECOG_HIGHGAMMA_FILES,
        "ecog_audio_present": any(
            item["key"] == PODCAST_AUDIO_KEY for item in ecog_objects
        ),
        "endpoint_bytes_downloaded": False,
        "endpoint_values_opened": False,
    }
    if not all(
        value
        for key, value in checks.items()
        if key not in {"endpoint_bytes_downloaded", "endpoint_values_opened"}
    ):
        raise RuntimeError(f"E028 metadata preflight failed: {checks}")

    remote_code = []
    for repository in (
        "hassonlab/podcast-ecog-paper",
        "hassonlab/podcast-ecog-tutorials",
    ):
        remote_code.append(github_head(repository))

    manifest = {
        "schema": "brain-alignment.e028.acquisition-manifest.v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "metadata_only": True,
        "script": {
            "path": str(Path(__file__).resolve()),
            "sha256": sha256_path(Path(__file__).resolve()),
        },
        "paper": {
            "title": (
                "Fine-tuning Language Encoding Models on Slow fMRI Improves "
                "Prediction for Fast ECoG"
            ),
            "arxiv": "2605.19224v1",
            "url": "https://arxiv.org/abs/2605.19224",
            "paper_specific_code": None,
            "paper_specific_checkpoint_sha256": None,
            "paper_specific_result_table_sha256": None,
        },
        "ecog": {
            "dataset": ECOG_DATASET,
            "expected_snapshot": "1.0.2",
            "expected_doi": EXPECTED_ECOG_DOI,
            "metadata": ecog_metadata,
            "remote_object_count": len(ecog_objects),
            "remote_total_size_bytes": sum(
                item["size_bytes"] for item in ecog_objects
            ),
            "minimal_acquisition_object_count": len(acquisition_objects),
            "minimal_acquisition_size_bytes": sum(
                item["size_bytes"] for item in acquisition_objects
            ),
            "minimal_acquisition_objects": acquisition_objects,
        },
        "fmri": {
            "dataset": FMRI_DATASET,
            "latest_visible_snapshot_at_audit": fmri_metadata[
                "dataset_description.json"
            ]["parsed"].get("DatasetDOI"),
            "paper_used_snapshot": None,
            "metadata": fmri_metadata,
            "local_coverage": local_lebel_coverage(),
        },
        "code": {
            "remote_metadata_heads": remote_code,
            "local_reusable_repositories": [
                {
                    "path": str(
                        ROOT / "data" / "paper-repos" / "multi-brain-tuning"
                    ),
                    "commit": git_head(
                        ROOT / "data" / "paper-repos" / "multi-brain-tuning"
                    ),
                    "scope": (
                        "LoRA, spatial-correlation, and fMRI alignment "
                        "scaffolding; not the Vaidya implementation"
                    ),
                },
                {
                    "path": str(ROOT / "data" / "paper-repos" / "brain-tuning"),
                    "commit": git_head(
                        ROOT / "data" / "paper-repos" / "brain-tuning"
                    ),
                    "scope": (
                        "speech brain-tuning scaffolding; not the Vaidya "
                        "implementation"
                    ),
                },
            ],
        },
        "required_before_download": [
            "Author confirmation of the exact ds003020 snapshot and story list",
            "Exact WavLM Base+ model identifier, revision, and file SHA-256",
            "Paper-specific code commit and environment lock",
            "Three principal LoRA checkpoints and SHA-256 values",
            "ECoG electrode inclusion table and fold/lag implementation",
        ],
        "checks": checks,
    }
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    manifest = build_manifest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(manifest, indent=2, sort_keys=True).encode("utf-8") + b"\n"
    args.output.write_bytes(payload)
    print(f"wrote={args.output}")
    print(f"sha256={sha256_bytes(payload)}")
    print(
        "minimal_ecog_bytes="
        f"{manifest['ecog']['minimal_acquisition_size_bytes']}"
    )
    print("metadata_only=true endpoint_values_opened=false")


if __name__ == "__main__":
    main()
