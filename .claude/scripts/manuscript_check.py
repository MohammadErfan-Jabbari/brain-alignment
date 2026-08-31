#!/usr/bin/env python3
"""Small deterministic gate for the live or frozen manuscript.

Checks evidence-marker resolution, bare result-like numbers, keyed-number
resolution, optional gap survival, and LaTeX compilation. It does not judge
scientific scope or prose quality; one fresh independent review owns that job.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

EVD = re.compile(r"\\evd\{([ELel]\d+)\}")
ANY_SOURCE = re.compile(r"\\evd\{[ELel]\d+\}|\\result\{[^}]+\}")
RESULT = re.compile(r"(?<![\w.])([+\-]?\d+\.\d+|\d+(?:\.\d+)?%|n\s*=\s*\d+|±\s*\d|\+/-\s*\d)")
WHITELIST = re.compile(
    r"\b(19|20)\d{2}\b|\b(section|sec|figure|fig|table|tab|eq|equation|page|chapter|appendix)\.?\s*\d"
    r"|\bv\d+(\.\d+)*\b|\b[ELSDQRA]\d+\b", re.I
)
DECLARE = re.compile(r"\\DeclareResult\{([^}]+)\}\{(.*)\}\s*(?:%.*)?$")
USE = re.compile(r"\\result\{([^}]+)\}")
INPUT = re.compile(r"\\(?:input|include)\{([^}]+)\}")
GAP = re.compile(r"\\gap\{")
FORMAT_ONLY = re.compile(
    r"^\s*\\(?:specialrule|vspace|par\\vspace|renewcommand\{\\arraystretch\})"
)
# LaTeX dimensions and TikZ coordinates are layout, not results. Stripped before the
# bare-number check so `[width=3.2cm]`, `\\[1.2em]` and `at (3.2,0.65)` stop reading as
# unsourced findings. The FORMAT_ONLY line whitelist above only covered whole lines.
LAYOUT = re.compile(
    r"\d+(?:\.\d+)?\s*(?:pt|mm|cm|in|em|ex|bp|dd|pc|sp"
    r"|\\(?:text|line|column|page)width|\\(?:text|page)height|\\baselineskip)\b"
    r"|\(\s*-?\d+(?:\.\d+)?\s*,\s*-?\d+(?:\.\d+)?\s*\)"
)


def repo_root(start: Path) -> Path:
    for parent in [start.resolve(), *start.resolve().parents]:
        if (parent / "docs" / "experiments").is_dir():
            return parent
    raise SystemExit("could not locate repository root")


def source_files(target: Path) -> list[Path]:
    """The .tex files whose prose is checked."""
    if target.is_file():
        return [target.resolve()]
    # `style/` is a vendored publisher template (neurips_2025.tex), not our prose.
    return sorted(
        p.resolve() for p in target.rglob("*.tex")
        if ".archive-manuscript" not in p.parts and "style" not in p.parts
    )


def declaration_scope(files: list[Path]) -> list[Path]:
    """Every .tex whose \\DeclareResult lines are in scope when `files` compile.

    Declarations live in one shared numbers.tex that the target usually does not
    \\input itself, so the scope is the \\input/\\include closure of both the
    target files and the enclosing main*.tex. Without this, checking one section
    reports every key as undefined, and the submission twin reports all of them
    because it compiles against ../rewrite/numbers.
    """
    seen = set(files)
    for path in files:
        for directory in (path.parent, path.parent.parent):
            seen.update(m.resolve() for m in directory.glob("main*.tex"))
    queue = list(seen)
    while queue:
        path = queue.pop()
        for _, line in prose_lines(path):
            for name in INPUT.findall(line):
                dep = (path.parent / (name if name.endswith(".tex") else name + ".tex")).resolve()
                if dep.is_file() and dep not in seen:
                    seen.add(dep)
                    queue.append(dep)
    return sorted(seen)


def resolves(key: str, root: Path) -> bool:
    kind, number = key[0].upper(), int(key[1:])
    if kind == "E":
        return any((root / "docs" / "experiments").glob(f"E{number:03d}_*.md"))
    if kind == "L":
        text = (root / "docs" / "learnings.md").read_text(encoding="utf-8", errors="replace")
        return re.search(rf"\bL{number:03d}\b|\bL{number}\b", text) is not None
    return False


def prose_lines(path: Path):
    for lineno, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if raw.lstrip().startswith("%"):
            continue
        yield lineno, raw


def check_sources(files: list[Path], root: Path, share_ready: bool) -> list[str]:
    findings: list[str] = []
    declarations: dict[str, str] = {}
    for path in declaration_scope(files):
        for lineno, line in prose_lines(path):
            match = DECLARE.search(line)
            if match:
                key, value = match.group(1).strip(), match.group(2).strip()
                if key in declarations and declarations[key] != value:
                    findings.append(f"{path}:{lineno}: conflicting declaration for {key}")
                declarations[key] = value
    for path in files:
        for lineno, line in prose_lines(path):
            for key in EVD.findall(line):
                if not resolves(key, root):
                    findings.append(f"{path}:{lineno}: unresolved evidence marker {key}")
            for key in USE.findall(line):
                if key not in declarations:
                    findings.append(f"{path}:{lineno}: undefined keyed number {key}")
            if share_ready and GAP.search(line):
                findings.append(f"{path}:{lineno}: unresolved \\gap")
            if path.name == "numbers.tex" or "\\newcommand" in line or "\\DeclareResult" in line:
                continue
            if FORMAT_ONLY.search(line):
                continue
            line = LAYOUT.sub("", line)
            if RESULT.search(line) and not ANY_SOURCE.search(line) and not WHITELIST.search(line):
                findings.append(f"{path}:{lineno}: result-like number lacks \\evd or \\result")
    return findings


def compile_latex(target: Path) -> list[str]:
    directory = target if target.is_dir() else target.parent
    mains = sorted(directory.glob("main*.tex"))
    if len(mains) != 1:
        return [f"{directory}: expected one manuscript main .tex file"]
    main = mains[0]
    if shutil.which("tectonic"):
        command = ["tectonic", "-X", "compile", main.name, "--keep-intermediates"]
    elif shutil.which("latexmk"):
        command = ["latexmk", "-pdf", "-interaction=nonstopmode", main.name]
    else:
        return ["LaTeX build unavailable: install latexmk or tectonic"]
    try:
        proc = subprocess.run(
            command,
            cwd=directory, text=True, capture_output=True, timeout=180
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return [f"LaTeX build failed to start: {exc}"]
    output = (proc.stdout or "") + "\n" + (proc.stderr or "")
    findings = []
    if proc.returncode != 0:
        tail = "\n".join(output.splitlines()[-30:])
        findings.append(f"LaTeX build failed (exit {proc.returncode}):\n{tail}")
    if re.search(r"LaTeX Warning:.*undefined|There were undefined references|Citation .* undefined", output, re.I):
        findings.append("LaTeX build reports undefined citations or references")
    return findings


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", type=Path, default=Path("docs/manuscript/rewrite"))
    parser.add_argument("--share-ready", action="store_true", help="also reject every unresolved \\gap")
    parser.add_argument("--no-build", action="store_true")
    args = parser.parse_args(argv)
    root = repo_root(args.path)
    target = args.path if args.path.is_absolute() else root / args.path
    files = source_files(target)
    if not files:
        print(f"manuscript-check: no .tex sources under {target}", file=sys.stderr)
        return 1
    findings = check_sources(files, root, args.share_ready)
    if not args.no_build:
        findings.extend(compile_latex(target))
    if findings:
        print("manuscript-check: FAIL")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print(f"manuscript-check: PASS ({len(files)} source files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
