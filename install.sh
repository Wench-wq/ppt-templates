#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
skill_home="${CODEX_HOME:-$HOME/.codex}/skills"

for tool in node npm python3 unzip; do
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

python3 - <<'PY'
import sys
if sys.version_info < (3, 10):
    raise SystemExit('Python 3.10 or newer is required.')
PY

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
  if [[ -e "$skill_home/$name" ]]; then
    echo "Keeping existing $skill_home/$name"
  else
    cp -R "$source_dir" "$skill_home/$name"
    echo "Installed $name to $skill_home/$name"
  fi
done

npm ci --prefix "$repo_root" --no-audit --no-fund
python3 -m venv "$repo_root/.venv"
"$repo_root/.venv/bin/python" -m pip install --disable-pip-version-check -r "$repo_root/requirements.txt"

if [[ "${SKIP_BROWSER_INSTALL:-0}" != "1" ]]; then
  "$repo_root/node_modules/.bin/playwright" install chromium
  REPO_ROOT="$repo_root" node - <<'JS'
const { chromium } = require(process.env.REPO_ROOT + '/node_modules/playwright');
chromium.launch({headless: true}).then(async browser => {
  await browser.close();
  console.log('Chromium browser launch passed.');
}).catch(error => {
  console.error('Chromium could not start. Install OS browser libraries if required.');
  console.error(error.message);
  process.exitCode = 1;
});
JS
fi

node "$repo_root/skills/gravity-ppt-skill/scripts/validate-deck.mjs" \
  "$repo_root/skills/gravity-ppt-skill/assets/template.html" --template
node "$repo_root/skills/pixel-ppt-skill/scripts/validate-deck.mjs" \
  "$repo_root/skills/pixel-ppt-skill/assets/template" --template

echo "HTML presentation skills are ready."
if [[ -n "${RUNTIME_NODE_MODULES:-${CODEX_PRIMARY_RUNTIME_NODE_MODULES:-}}" ]]; then
  runtime_modules="${RUNTIME_NODE_MODULES:-${CODEX_PRIMARY_RUNTIME_NODE_MODULES}}"
  if [[ -d "$runtime_modules/@oai/artifact-tool" ]]; then
    echo "Codex presentation runtime detected."
  else
    echo "Codex presentation runtime was not found in $runtime_modules."
  fi
else
  echo "Codex presentation runtime not detected; PPTX authoring depends on the target account's bundled runtime."
fi
