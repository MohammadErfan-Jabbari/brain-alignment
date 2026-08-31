"""Self-check for the bash_gate PreToolUse hook.

Run: uv run python tests/test_bash_gate.py
"""
import json
import pathlib
import subprocess
import sys

HOOK = str(pathlib.Path(__file__).resolve().parent.parent / ".claude/hooks/bash_gate.py")

# (command, expect_deny)
CASES = [
    # --- must deny: irreversible git ---
    ("git " + "reset --hard origin/main", True),
    ("git " + "clean -fd", True),
    ("git " + "clean --force", True),
    ("git " + "push --force", True),
    ("git " + "push -f origin main", True),
    ("git " + "commit --amend --no-edit", True),
    ("git " + "branch -D feature/x", True),
    ("git " + "stash drop", True),
    ("git " + "stash clear", True),
    ("rtk git " + "reset --hard HEAD~1", True),          # rtk-prefixed still caught
    ("cd /tmp && git " + "reset --hard", True),          # later in a chain
    # --- must deny: unsandboxed codex ---
    ('codex exec "count the files"', True),
    ("codex exec -c sandbox_mode=read-only 'x'", True),
    # --- must allow: safe forms ---
    ("git " + "push --force-with-lease", False),
    ("git status --short", False),
    ("git add docs/x.md", False),
    ("git " + "commit -m 'msg'", False),
    ("git " + "stash list", False),
    ("git " + "branch -d merged", False),                # lowercase -d is safe
    ("git " + "log --format=%H", False),
    ("git " + "checkout -b newbranch", False),
    ('codex exec --sandbox danger-full-access "count"', False),
    ("uv run python .claude/scripts/manuscript_check.py docs/manuscript/rewrite", False),
    # --- must allow: the pattern only as text, no git token ---
    ('grep -rn "reset --hard" docs/', False),
    ('echo "never run clean -f here"', False),
    # --- must allow: prose ABOUT the gate (the false positive that bit in-session) ---
    ("python3 - <<'EOF'\ntext = 'Irreversible git: `reset --hard`, `clean -f`, `push --force`'\nEOF", False),
    ('echo "Overrides D039: a git add -A guard is recoverable; reset --hard is not"', False),
    ("cat >| f.md <<'EOF'\nRetired the git-related gate covering reset --hard and stash drop.\nEOF", False),
    # --- must still deny even with a wrapper or leading path ---
    ("sudo git " + "clean -fdx", True),
    ("git -C /tmp/repo " + "reset --hard", True),
    ("cd /tmp; codex exec 'x'", True),
    # --- must allow: a QUOTED mention is not a command position ---
    # (a commit message documenting this gate tripped the earlier pattern)
    ("git commit -m 'denies unsandboxed `codex exec` per L033'", False),
    ('echo "run `codex exec` only with the full-access sandbox"', False),
    ("git commit -m 'gate covers `git reset --hard` and `git stash drop`'", False),
]


def denied(cmd: str) -> bool:
    out = subprocess.run(
        [sys.executable, HOOK],
        input=json.dumps({"tool_name": "Bash", "tool_input": {"command": cmd}}),
        capture_output=True, text=True,
    ).stdout.strip()
    if not out:
        return False
    return json.loads(out)["hookSpecificOutput"]["permissionDecision"] == "deny"


fails = []
for cmd, want in CASES:
    got = denied(cmd)
    if got != want:
        fails.append(f"  {'expected DENY, got allow' if want else 'expected allow, got DENY'}: {cmd}")

print(f"{len(CASES) - len(fails)}/{len(CASES)} cases pass")
if fails:
    print("FAILURES:")
    print("\n".join(fails))
    sys.exit(1)
print("bash_gate OK")
