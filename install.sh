#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
skill_home="${CODEX_HOME:-$HOME/.codex}/skills"

for tool in node python3 unzip; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "Missing required tool: $tool" >&2
    exit 1
  fi
done

node_major="$(node -p 'process.versions.node.split(".")[0]')"
if (( node_major < 18 )); then
  echo "Node.js 18 or newer is required (found $(node --version))." >&2
  exit 1
fi

archive="$repo_root/ppt-skills.zip"
if [[ ! -f "$archive" ]]; then
  echo "Missing $archive" >&2
  exit 1
fi

mkdir -p "$repo_root/skills" "$skill_home"
unzip -oq "$archive" -d "$repo_root"

for name in presentations gravity-ppt-skill pixel-ppt-skill; do
  source_dir="$repo_root/skills/$name"
  if [[ ! -f "$source_dir/SKILL.md" ]]; then
    echo "Missing $source_dir/SKILL.md after extraction" >&2
    exit 1
  fi
  rm -rf "$skill_home/$name"
  cp -R "$source_dir" "$skill_home/$name"
  echo "Installed $name to $skill_home/$name"
done

node "$repo_root/skills/gravity-ppt-skill/scripts/validate-deck.mjs" \
  "$repo_root/skills/gravity-ppt-skill/assets/template.html" --template
node "$repo_root/skills/pixel-ppt-skill/scripts/validate-deck.mjs" \
  "$repo_root/skills/pixel-ppt-skill/assets/template" --template

echo "HTML presentation skills are ready."
echo "The Presentations skill additionally requires the Codex presentation runtime."
