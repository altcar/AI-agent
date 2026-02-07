Changes made

OmniParser/pyproject.toml + OmniParser/uv.lock + OmniParser/.python-version created; dependencies pulled from OmniParser/requirements.txt plus huggingface-hub for the CLI in OmniParser/h.md.
OpenManus/pyproject.toml + OpenManus/uv.lock + OpenManus/.python-version created; dependencies pulled from OpenManus/requirements.txt.
patchright/pyproject.toml + patchright/uv.lock + patchright/.python-version created; added patchright for patchright/script.py.
Added python-dotenv to browser-use/pyproject.toml and windowsuse/pyproject.toml (needed by run/my_agent.py and main.py).
Compatibility/installation review

OpenManus mismatch: OpenManus/setup.py requires Python >=3.12 but OpenManus/.python-version and OpenManus/pyproject.toml now say >=3.11. This will block installs on other machines if they use 3.11. Recommended fix is to align OpenManus to 3.12.
OmniParser has heavy ML deps (torch/paddle/ultralytics). These are platform-specific and may require extra system tooling or GPU wheels; installs can fail without the right platform/driver setup.
browser-use and windowsuse require Python >=3.12 (already set).
Script review findings

browser-use/run/my_agent.py references openai_api_key but never defines it; use os.getenv("OPENAI_API_KEY") (or similar) before constructing ChatOpenAI.
patchright/script.py and browser-use/run/my_agent.py contain hard‑coded session tokens; move to env vars and rotate.
open-interpreter/h.md and agent-tars/h.md contain API keys; rotate and move to env vars.
patchright/h.md has a malformed command (python run script.py); should be python script.py.
OmniParser/h.md and windowsuse/h.md use absolute paths; not portable to other machines.
Install + run on a new machine (portable versions of the h.md commands) OmniParser

cd OmniParser
uv sync
uv run huggingface-cli download microsoft/OmniParser-v2.0 --local-dir weights --repo-type model --include "icon_detect/*"
uv run huggingface-cli download microsoft/OmniParser-v2.0 --local-dir weights --repo-type model --include "icon_caption/*"
# rename weights\icon_caption -> weights\icon_caption_florence
uv run python -m omniparserserver
uv run python omnitool/gradio/app.py --windows_host_url localhost:8006 --omniparser_server_url localhost:8000
OpenManus

cd OpenManus
uv sync
uv run python main.py
browser-use

cd browser-use
uv sync
uv run python run/my_agent.py
windowsuse

cd windowsuse
uv sync
uv run python main.py --api_base "<BASE_URL>" --api_key "<KEY>" --model "qwen-plus"
patchright

cd patchright
uv sync
uv run python script.py
open-interpreter (already Poetry-based)

cd open-interpreter
poetry install  # or: uv pip install -e .
interpreter -y --api_base "<BASE_URL>" --api_key "<KEY>" --model "<MODEL>"
Notes on “install right away”

Use uv sync --locked for each uv project to enforce uv.lock.
OpenManus should be run with Python 3.12 unless you want to change OpenManus/setup.py.
If you want, I can also:

Align OpenManus to Python 3.12 (update OpenManus/.python-version, OpenManus/pyproject.toml, and OpenManus/setup.py).
Sanitize the secrets in open-interpreter/h.md, agent-tars/h.md, patchright/script.py, and browser-use/run/my_agent.py.
Fix the openai_api_key usage in browser-use/run/my_agent.py so it runs out of the box.