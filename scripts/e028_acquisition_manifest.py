#!/usr/bin/env python3
"""Build the metadata-only acquisition manifest for E028.

The program is deliberately incapable of acquiring an E028 endpoint payload. It
reads OpenNeuro object-listing metadata, a small allowlist of descriptive files,
GitHub commit metadata, and local filenames/file sizes. It does not download
audio, neural arrays, model weights, checkpoints, or paper result tables; it
does not open any neural value; and it does not train or score a model.

The access declarations in the resulting manifest describe this invocation of
this script only. They make no claim about activity by another process or user.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
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
EXPECTED_ECOG_SNAPSHOT = "1.0.2"
EXPECTED_ECOG_DOI = "doi:10.18112/openneuro.ds005574.v1.0.2"
EXPECTED_ECOG_LICENSE = "CC0"
EXPECTED_ECOG_SUBJECTS = tuple(f"sub-{index:02d}" for index in range(1, 10))

GLOBAL_REQUIRED_KEYS = (
    "ds005574/CHANGES",
    "ds005574/README",
    "ds005574/dataset_description.json",
    "ds005574/environment.yml",
    "ds005574/participants.json",
    "ds005574/participants.tsv",
    "ds005574/stimuli/podcast.wav",
    "ds005574/stimuli/podcast_transcript.csv",
)

HIGHGAMMA_LAYOUT_RE = re.compile(
    r"^ds005574/derivatives/ecogprep/(?P<directory>sub-\d{2})/ieeg/"
    r"(?P<filename>sub-\d{2})_task-podcast_desc-highgamma_ieeg\.fif$"
)
SUBJECT_METADATA_LAYOUT_RE = re.compile(
    r"^ds005574/(?P<directory>sub-\d{2})/ieeg/"
    r"(?P<filename>sub-\d{2})_(?P<role>"
    r"task-podcast_channels\.tsv|task-podcast_ieeg\.json|"
    r"space-MNI152NLin2009aSym_electrodes\.tsv|"
    r"space-MNI152NLin2009aSym_coordsystem\.json)$"
)


def subject_required_keys(subject: str) -> dict[str, str]:
    """Return the five endpoint/accompanying objects required for one patient."""

    return {
        "highgamma": (
            f"ds005574/derivatives/ecogprep/{subject}/ieeg/"
            f"{subject}_task-podcast_desc-highgamma_ieeg.fif"
        ),
        "channels": (
            f"ds005574/{subject}/ieeg/{subject}_task-podcast_channels.tsv"
        ),
        "ieeg_json": (
            f"ds005574/{subject}/ieeg/{subject}_task-podcast_ieeg.json"
        ),
        "electrodes": (
            f"ds005574/{subject}/ieeg/"
            f"{subject}_space-MNI152NLin2009aSym_electrodes.tsv"
        ),
        "coordsystem": (
            f"ds005574/{subject}/ieeg/"
            f"{subject}_space-MNI152NLin2009aSym_coordsystem.json"
        ),
    }


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return sha256_bytes(payload)


def fetch_bytes(url: str, timeout: int = 30) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "brain-alignment-e028-metadata-audit/2.0"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def fetch_json(url: str) -> dict[str, Any]:
    return json.loads(fetch_bytes(url).decode("utf-8"))


def s3_listing(dataset: str) -> list[dict[str, Any]]:
    """Read one dataset's object metadata; reject rather than hide pagination."""

    query = urllib.parse.urlencode(
        {"list-type": "2", "prefix": f"{dataset}/", "max-keys": "1000"}
    )
    payload = fetch_bytes(f"{OPENNEURO_BUCKET}?{query}")
    root = ET.fromstring(payload)
    namespace = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}
    truncated = root.findtext("s3:IsTruncated", namespaces=namespace)
    if truncated != "false":
        raise RuntimeError(
            f"{dataset} listing is truncated; implement pagination before use"
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
                # Multipart ETags are not content SHA-256 values.
                "remote_etag_not_sha256": etag.strip('"') if etag else None,
                "last_modified": modified,
                "sha256_after_future_acquisition": None,
            }
        )

    keys = [item["key"] for item in objects]
    if len(keys) != len(set(keys)):
        raise RuntimeError(f"{dataset} listing contains duplicate object keys")
    return sorted(objects, key=lambda item: item["key"])


def listing_identity(objects: list[dict[str, Any]]) -> dict[str, Any]:
    """Hash exact listing fields, independently of manifest timestamps."""

    rows = [
        {
            "key": item["key"],
            "size_bytes": item["size_bytes"],
            "remote_etag_not_sha256": item["remote_etag_not_sha256"],
            "last_modified": item["last_modified"],
        }
        for item in objects
    ]
    return {
        "canonical_fields": [
            "key",
            "last_modified",
            "remote_etag_not_sha256",
            "size_bytes",
        ],
        "object_count": len(rows),
        "canonical_listing_sha256": canonical_sha256(rows),
    }


def remote_small_metadata(
    dataset: str, names: tuple[str, ...]
) -> tuple[dict[str, Any], dict[str, bytes]]:
    """Fetch only explicitly allowed descriptive metadata files."""

    result: dict[str, Any] = {}
    bodies: dict[str, bytes] = {}
    for name in names:
        url = f"{OPENNEURO_BUCKET}/{dataset}/{name}"
        payload = fetch_bytes(url)
        bodies[name] = payload
        result[name] = {
            "url": url,
            "size_bytes": len(payload),
            "sha256": sha256_bytes(payload),
        }
        if name == "dataset_description.json":
            result[name]["parsed"] = json.loads(payload.decode("utf-8"))
    return result, bodies


def github_head(repository: str) -> dict[str, Any]:
    url = f"https://api.github.com/repos/{repository}/commits/main"
    data = fetch_json(url)
    return {
        "repository": f"https://github.com/{repository}",
        "commit": data["sha"],
        "committed_at": data["commit"]["committer"]["date"],
        "archive_sha256_after_future_acquisition": None,
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
    """Inventory names and stat metadata only; never open an hf5 or WAV body."""

    root = ROOT / "data" / "lebel_ds003020"
    coverage: dict[str, Any] = {
        "root": str(root),
        "access_scope": "filenames and filesystem stat metadata only",
        "neural_value_files_opened_by_this_script_run": [],
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


def parse_participant_ids(payload: bytes) -> list[str]:
    reader = csv.DictReader(io.StringIO(payload.decode("utf-8")), delimiter="\t")
    if reader.fieldnames is None or "participant_id" not in reader.fieldnames:
        raise RuntimeError("participants.tsv has no participant_id column")
    ids = [row["participant_id"].strip() for row in reader if row["participant_id"]]
    if len(ids) != len(set(ids)):
        raise RuntimeError("participants.tsv contains duplicate participant_id values")
    return ids


def validate_ecog_layout(
    objects: list[dict[str, Any]], participant_payload: bytes
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Validate exact subjects, required keys, and subject/path agreement."""

    by_key = {item["key"]: item for item in objects}
    participant_ids = parse_participant_ids(participant_payload)
    expected_ids = list(EXPECTED_ECOG_SUBJECTS)
    if participant_ids != expected_ids:
        raise RuntimeError(
            "participants.tsv IDs/order differ from exact expected IDs: "
            f"observed={participant_ids} expected={expected_ids}"
        )

    missing_global = [key for key in GLOBAL_REQUIRED_KEYS if key not in by_key]
    if missing_global:
        raise RuntimeError(f"Missing required global ECoG objects: {missing_global}")

    patient_matrix: dict[str, Any] = {}
    expected_highgamma: set[str] = set()
    expected_metadata: set[str] = set()
    selected_keys: set[str] = set(GLOBAL_REQUIRED_KEYS)
    for subject in EXPECTED_ECOG_SUBJECTS:
        roles = subject_required_keys(subject)
        missing = [role for role, key in roles.items() if key not in by_key]
        if missing:
            raise RuntimeError(f"{subject} is missing required roles: {missing}")

        highgamma_match = HIGHGAMMA_LAYOUT_RE.fullmatch(roles["highgamma"])
        if highgamma_match is None or {
            highgamma_match.group("directory"),
            highgamma_match.group("filename"),
        } != {subject}:
            raise RuntimeError(f"High-gamma path/filename mismatch for {subject}")

        for role in ("channels", "ieeg_json", "electrodes", "coordsystem"):
            match = SUBJECT_METADATA_LAYOUT_RE.fullmatch(roles[role])
            if match is None or {
                match.group("directory"),
                match.group("filename"),
            } != {subject}:
                raise RuntimeError(
                    f"Metadata path/filename mismatch for {subject} role={role}"
                )

        expected_highgamma.add(roles["highgamma"])
        expected_metadata.update(
            roles[role]
            for role in ("channels", "ieeg_json", "electrodes", "coordsystem")
        )
        selected_keys.update(roles.values())
        patient_matrix[subject] = {
            "highgamma_object_count": 1,
            "metadata_object_count": 4,
            "objects_by_role": roles,
            "path_filename_subject_agreement": True,
        }

    observed_highgamma = {
        item["key"] for item in objects if HIGHGAMMA_LAYOUT_RE.fullmatch(item["key"])
    }
    observed_metadata = {
        item["key"]
        for item in objects
        if SUBJECT_METADATA_LAYOUT_RE.fullmatch(item["key"])
    }
    if observed_highgamma != expected_highgamma:
        raise RuntimeError(
            "High-gamma object set differs from the exact one-per-patient set: "
            f"extra={sorted(observed_highgamma - expected_highgamma)} "
            f"missing={sorted(expected_highgamma - observed_highgamma)}"
        )
    if observed_metadata != expected_metadata:
        raise RuntimeError(
            "Patient metadata object set differs from exact four-per-patient set: "
            f"extra={sorted(observed_metadata - expected_metadata)} "
            f"missing={sorted(expected_metadata - observed_metadata)}"
        )

    selected_objects = [by_key[key] for key in sorted(selected_keys)]
    layout = {
        "participant_ids_from_tsv": participant_ids,
        "expected_participant_ids": expected_ids,
        "required_global_keys": list(GLOBAL_REQUIRED_KEYS),
        "required_global_key_count": len(GLOBAL_REQUIRED_KEYS),
        "patient_object_matrix": patient_matrix,
        "highgamma_object_count": len(observed_highgamma),
        "patient_metadata_object_count": len(observed_metadata),
        "all_exact_paths_present": True,
        "all_path_filename_subjects_agree": True,
        "one_highgamma_and_four_metadata_objects_per_patient": True,
    }
    return layout, selected_objects


def build_manifest() -> dict[str, Any]:
    ecog_objects = s3_listing(ECOG_DATASET)
    ecog_metadata, ecog_bodies = remote_small_metadata(
        ECOG_DATASET,
        ("dataset_description.json", "README", "participants.tsv", "CHANGES"),
    )
    fmri_metadata, _ = remote_small_metadata(
        FMRI_DATASET,
        ("dataset_description.json", "CHANGES"),
    )

    description = ecog_metadata["dataset_description.json"]["parsed"]
    layout, acquisition_objects = validate_ecog_layout(
        ecog_objects, ecog_bodies["participants.tsv"]
    )
    ecog_listing_identity = listing_identity(ecog_objects)
    acquisition_identity = listing_identity(acquisition_objects)

    checks = {
        "ecog_listing_not_truncated": True,
        "ecog_dataset_doi_matches_v1_0_2": (
            description.get("DatasetDOI") == EXPECTED_ECOG_DOI
        ),
        "ecog_license_matches": description.get("License") == EXPECTED_ECOG_LICENSE,
        "ecog_exact_subject_ids_and_order_match": (
            layout["participant_ids_from_tsv"] == list(EXPECTED_ECOG_SUBJECTS)
        ),
        "ecog_all_required_keys_present": layout["all_exact_paths_present"],
        "ecog_path_filename_subject_agreement": (
            layout["all_path_filename_subjects_agree"]
        ),
        "ecog_one_highgamma_and_four_metadata_per_patient": (
            layout["one_highgamma_and_four_metadata_objects_per_patient"]
        ),
        "this_script_run_endpoint_payload_objects_downloaded": False,
        "this_script_run_neural_value_files_opened": False,
        "this_script_run_training_or_scoring_performed": False,
        "this_script_run_author_communications_performed": False,
    }
    structural_checks = {
        key: value
        for key, value in checks.items()
        if not key.startswith("this_script_run_")
    }
    if not all(structural_checks.values()):
        raise RuntimeError(f"E028 metadata preflight failed: {checks}")

    remote_code = [
        github_head(repository)
        for repository in (
            "hassonlab/podcast-ecog-paper",
            "hassonlab/podcast-ecog-tutorials",
        )
    ]

    paper_artifacts = {
        # These arrays remain empty until author-supplied items are acquired and hashed.
        "paper_specific_code_archives": [],
        "environment_locks": [],
        "base_model_files": [],
        "training_and_validation_manifests": [],
        "principal_lora_checkpoints": [],
        "epoch_selection_records": [],
        "ecog_masks_and_fold_lag_manifests": [],
        "ecog_result_tables_or_prediction_pointers": [],
    }

    manifest = {
        "schema": "brain-alignment.e028.acquisition-manifest.v2",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "manifest_scope": (
            "metadata-only preflight; not an endpoint artifact and not evidence of "
            "design readiness"
        ),
        "script": {
            "path": str(Path(__file__).resolve()),
            "sha256": sha256_path(Path(__file__).resolve()),
        },
        "this_script_run_access": {
            "scope": (
                "Only actions performed by this invocation of "
                "scripts/e028_acquisition_manifest.py"
            ),
            "remote_object_listing_metadata_read": [ECOG_DATASET],
            "remote_descriptive_metadata_files_read": {
                ECOG_DATASET: sorted(ecog_metadata),
                FMRI_DATASET: sorted(fmri_metadata),
            },
            "remote_git_commit_metadata_read": [
                item["repository"] for item in remote_code
            ],
            "local_file_contents_read": [str(Path(__file__).resolve())],
            "local_git_commit_metadata_read": [
                str(ROOT / "data" / "paper-repos" / "multi-brain-tuning"),
                str(ROOT / "data" / "paper-repos" / "brain-tuning"),
            ],
            "local_paths_names_and_stat_metadata_read": [
                str(ROOT / "data" / "lebel_ds003020"),
                str(ROOT / "data" / "stimuli_wav"),
            ],
            "local_files_written": [],
            "endpoint_payload_objects_downloaded": [],
            "neural_value_files_opened": [],
            "model_training_or_scoring_runs": [],
            "author_communications": [],
        },
        "paper": {
            "title": (
                "Fine-tuning Language Encoding Models on Slow fMRI Improves "
                "Prediction for Fast ECoG"
            ),
            "arxiv": "2605.19224v1",
            "url": "https://arxiv.org/abs/2605.19224",
            "paper_specific_artifacts": paper_artifacts,
        },
        "ecog": {
            "dataset": ECOG_DATASET,
            "expected_snapshot": EXPECTED_ECOG_SNAPSHOT,
            "expected_doi": EXPECTED_ECOG_DOI,
            "metadata": ecog_metadata,
            "snapshot_listing_identity": {
                "binding": (
                    "This digest is accepted only with the simultaneously verified "
                    f"DatasetDOI {EXPECTED_ECOG_DOI}"
                ),
                **ecog_listing_identity,
            },
            "remote_object_count": len(ecog_objects),
            "remote_total_size_bytes": sum(
                item["size_bytes"] for item in ecog_objects
            ),
            "validated_layout": layout,
            "minimal_acquisition_listing_identity": acquisition_identity,
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
            "dataset_owner_remote_metadata_heads": remote_code,
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
        "required_before_payload_acquisition": [
            "Independent precheck DESIGN PASS and READY-TO-RUN: YES",
            "Frozen runner/analyzer/config hashes and dimension-scale synthetic benchmark",
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
    manifest["this_script_run_access"]["local_files_written"] = [
        str(args.output.resolve())
    ]
    payload = json.dumps(manifest, indent=2, sort_keys=True).encode("utf-8") + b"\n"
    args.output.write_bytes(payload)
    print(f"wrote={args.output}")
    print(f"sha256={sha256_bytes(payload)}")
    print(
        "snapshot_listing_sha256="
        f"{manifest['ecog']['snapshot_listing_identity']['canonical_listing_sha256']}"
    )
    print(
        "minimal_ecog_bytes="
        f"{manifest['ecog']['minimal_acquisition_size_bytes']}"
    )
    print(
        "scope=this_script_run metadata_only=true "
        "endpoint_payload_objects_downloaded=0 neural_value_files_opened=0"
    )


if __name__ == "__main__":
    main()
