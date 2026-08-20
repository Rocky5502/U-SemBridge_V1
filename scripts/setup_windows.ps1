$ErrorActionPreference = "Stop"

if (-not (Test-Path ".venv")) {
  python -m venv .venv
}

& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
python -m usembridge doctor
pytest -q
python scripts\semantic_gap_demo.py
Write-Host "Core setup complete. For local LLMs: pip install -e '.[llm]'" -ForegroundColor Green
