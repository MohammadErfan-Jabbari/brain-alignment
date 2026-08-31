#!/usr/bin/env python3
"""PreToolUse gate for Bash. Decides from the command string alone.

Two denials, both for actions a later reviewer arrives too late to fix:

1. `codex exec` without `--sandbox danger-full-access`. Bubblewrap cannot
   initialise in this container (L033), so the sandboxed form returns values the
   model guessed (`COUNT=0`) that are indistinguishable from a real answer.
2. Irreversible git. Loses committed or stashed work with no recovery path.
   Recoverable staging hygiene (`git add -A`) is deliberately NOT here: D039
   declined that, and a gate that nags is worse than a contract line.

Reads no repo path and no file contents, so it cannot go stale the way the
retired writecheck hooks did (L052, D068).
"""
import json
import re
import sys

# The program name must sit at a command position, and for git the subcommand must
# follow it directly (only global flags between). Without both, writing documentation
# ABOUT this gate trips it: a commit message mentioning the sandbox flag, or prose
# like "irreversible git: hard reset", matched an earlier looser pattern. A backtick
# or quote immediately before the name is therefore not a command position, which is
# what keeps quoted mentions out. `[^;&|]*` keeps a flag match inside one segment.
CMD = r"(?:^|[\s;&|(])(?:sudo\s+|env\s+\S+=\S+\s+|rtk\s+)*"
GIT = (
    CMD + r"git\s+"
    # global flags, including the ones that take a separate argument (`git -C path reset`)
    r"(?:(?:-C|-c|--git-dir|--work-tree|--namespace|--exec-path)\s+\S+\s+"
    r"|-[\w-]+\s+|--[\w-]+(?:=\S+)?\s+)*"
)
CODEX_EXEC = CMD + r"codex\s+exec\b"
GIT_DENY = [
    (GIT + r"reset\b[^;&|]*--hard\b", "this discards committed and staged work"),
    (GIT + r"clean\b[^;&|]*-[a-z]*f", "this deletes untracked files permanently"),
    (GIT + r"push\b[^;&|]*(--force(?!-with-lease)|(?<!\w)-f(?!\w))",
     "this overwrites remote history; use --force-with-lease"),
    (GIT + r"commit\b[^;&|]*--amend\b", "this rewrites a commit, and the repo contract forbids amending"),
    (GIT + r"branch\b[^;&|]*(?<!\w)-D(?!\w)", "this force-deletes an unmerged branch"),
    (GIT + r"stash\b[^;&|]*\b(drop|clear)\b", "this destroys stashed work"),
]


def deny(reason: str) -> int:
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason + " Ask Erfan before running this.",
    }}))
    return 0


def main() -> int:
    try:
        cmd = (json.load(sys.stdin).get("tool_input") or {}).get("command") or ""
    except Exception:
        return 0

    if re.search(CODEX_EXEC, cmd) and "danger-full-access" not in cmd:
        return deny(
            "an unsandboxed codex exec returns fabricated output in this container "
            "(L033); pass the explicit full-access sandbox flag, and note that a "
            "-c key=val override has silently reverted it once."
        )
    for pattern, reason in GIT_DENY:
        match = re.search(pattern, cmd)
        if match:
            return deny(f"`{match.group(0).strip()}...`: {reason}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
