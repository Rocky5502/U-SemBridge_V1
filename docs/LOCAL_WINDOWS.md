# Local Windows runbook

1. Install Python 3.11 64-bit and verify `py -3.11 --version`.
2. Run:
```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\setup_windows.ps1
```
3. Verify NVIDIA driver separately with `nvidia-smi`.
4. Install a PyTorch build compatible with the local driver/CUDA using the current PyTorch instructions, then `pip install -e ".[llm]"`.
5. Fetch data/baselines:
```powershell
python scripts\download_datasets.py --all
python scripts\prepare_folio.py
python scripts\fetch_baselines.py --all
```
6. Before model inference:
```powershell
python -m usembridge doctor
pytest -q
python scripts\smoke_test.py
```
Do not assume CUDA compatibility from this repository alone.
