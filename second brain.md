# Second Brain (local-first)

This workspace sets up pgvector + MemGPT and a local ingestion pipeline for your Obsidian vault.

## A) Prerequisites (Windows + WSL2)
- Docker Desktop with WSL2 backend (already installed per your note)
- Python 3.10+ on Windows
- Git (optional)

## B) PostgreSQL + pgvector (Docker Compose)
1) .env is created with your password.
2) Data is stored in local folder: db/data
3) Start the database with Docker Desktop (WSL2 backend):
   - docker compose up -d

Connection string format:
`postgresql://memgpt:<PASSWORD>@localhost:5432/memgpt_db`

## C) MemGPT (Python install)
1) Use separate venvs to avoid dependency conflicts:
   - .venv-oi for Open Interpreter
   - .venv-letta for MemGPT/Letta
2) Install Letta (MemGPT successor) in .venv-letta.
3) Configure environment variables:
   - config/memgpt.env is created with your endpoint/key (do not commit)
4) Launch/initialize MemGPT:
   - Use the script: scripts/run_memgpt.ps1 (runs Letta CLI)

Notes:
- If MemGPT has rebranded to Letta in your environment, install `letta` and use `letta` CLI instead.
- Keep your API key out of git.

## D) Obsidian ingestion (JSONL chunking)
This produces JSONL for archival ingestion.

1) Run chunker:
   - python scripts/ingest_obsidian.py --vault "C:\l\Anytype.20250218.013428.84" --out data/obsidian_chunks.jsonl

2) Import into MemGPT archival memory (choose one):
   - If your MemGPT CLI supports JSONL import, use it here.
   - If not, I can wire a direct archival API client once your MemGPT server endpoint is confirmed.

## E) MCP servers (filesystem + desktop vision/control)
### DesktopCommanderMCP (primary for terminal + file/code editing)
Preferred install (Windows):
- npx @wonderwhy-er/desktop-commander setup
   Alternative: git clone https://github.com/wonderwhy-er/DesktopCommanderMCP, then npm install, npm run build, npm start

Required config (strict allow-list + approvals):
- Allowed folders (config file created):
   - C:\l\Anytype.20250218.013428.84
- Deny internet/dangerous commands by default
- Approval required for writes, exec, process control
- PowerShell backend (per your request)

Config template to apply in DesktopCommanderMCP:
- See [config/desktopcommander.allowed.json](config/desktopcommander.allowed.json)

Default port: 8765 (or the tool’s default)

### Open Interpreter (vision + browser + GUI control)
Install:
- pip install open-interpreter

Run in computer-use mode (vision + OS control):
- Use the script: scripts/run_open_interpreter.ps1

Edge Remote Debugging (for browser control):
- Start Edge with: msedge.exe --remote-debugging-port=9222

Integration goal:
- Use DesktopCommanderMCP for file and terminal operations
- Use Open Interpreter for vision + GUI interactions (screenshots, mouse/keyboard)

I will add a MemGPT tool config stub once you confirm your remaining allowed folders and preferred shell (PowerShell vs WSL2).

## F) Test queries (examples)
- “Summarize my Obsidian notes on Python async.”
- “Look at my current desktop and tell me what’s open in Edge.”
- “Find quotes about innovation and relate them to my coding projects.”
Additional control tests:
- “Use terminal to git status in my main repo.”
- “Edit utils.py: add type hint to function process_data.”
- “Open Edge, go to remote debugger docs, take screenshot of the console panel.”
- “What’s currently visible on my desktop? Describe open apps and video editor state.”
- “Click the play button in my video timeline if it’s paused.”
