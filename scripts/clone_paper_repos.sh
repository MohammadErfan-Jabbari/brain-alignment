#!/usr/bin/env bash
# Clone paper code repos as read-only reference examples.
#
# Reads scripts/paper-repos.tsv (tracked) and shallow-clones each repo into
# data/paper-repos/<name>/ (gitignored). Idempotent: existing clones are skipped.
# We want code to read, not history -> --depth 1. Records resolved commit SHAs in
# data/paper-repos/MANIFEST.tsv (local, gitignored) so you know exactly what you have.
#
# Usage:
#   scripts/clone_paper_repos.sh           # clone missing
#   UPDATE=1 scripts/clone_paper_repos.sh  # also `git pull` repos already present
set -uo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
manifest="$repo_root/scripts/paper-repos.tsv"
dest="$repo_root/data/paper-repos"
lock="$dest/MANIFEST.tsv"

mkdir -p "$dest"
printf 'name\turl\tcategory\tpaper\tcommit\n' > "$lock"

ok=0; skip=0; fail=0; failed_urls=()

while IFS=$'\t' read -r url category paper; do
  # skip blanks and comments
  [[ -z "${url// }" || "${url:0:1}" == "#" ]] && continue
  name="$(basename "$url")"
  target="$dest/$name"

  if [[ -d "$target/.git" ]]; then
    if [[ "${UPDATE:-0}" == "1" ]]; then
      echo "↻ updating $name"
      git -C "$target" pull --ff-only --quiet || echo "  (pull failed, keeping existing)"
    else
      echo "✓ skip (exists) $name"
    fi
    skip=$((skip+1))
  else
    echo "⇣ cloning $name  ($paper)"
    if git clone --depth 1 --quiet "$url" "$target"; then
      ok=$((ok+1))
    else
      echo "  ✗ FAILED: $url"
      fail=$((fail+1)); failed_urls+=("$url")
      continue
    fi
  fi

  sha="$(git -C "$target" rev-parse --short HEAD 2>/dev/null || echo '?')"
  printf '%s\t%s\t%s\t%s\t%s\n' "$name" "$url" "$category" "$paper" "$sha" >> "$lock"
done < "$manifest"

echo
echo "── done: $ok cloned, $skip skipped, $fail failed ──"
if (( fail > 0 )); then
  echo "failed repos (resolve URL or check access):"
  printf '  %s\n' "${failed_urls[@]}"
fi
echo "local record: $lock"
