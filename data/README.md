# Data

Raw and processed benchmark files are intentionally ignored by git.

## Acquire

```bash
python scripts/download_datasets.py --all
python scripts/prepare_folio.py
```

The downloader stores source repositories in `data/raw/` and writes exact source commit manifests to `data/manifests/`.

## Integrity rules

- Never edit files under `data/raw/`.
- Every transformation must be deterministic and scripted.
- Keep **Unknown** distinct from **False** for open-world benchmarks.
- Do not use evaluation examples as demonstrations, calibration data, or hyperparameter tuning data.
- If third-party terms prohibit redistribution, publish only IDs/hashes/derived metadata.
- LegalBridge is planned and must not be treated as an existing public gold dataset.
