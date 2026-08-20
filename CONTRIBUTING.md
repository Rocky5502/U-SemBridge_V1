# Contributing

This is a research repository. Contributions should preserve reproducibility and avoid unverifiable claims.

## Before opening a PR
- run `pytest -q`;
- run `ruff check src tests scripts`;
- run `python scripts/smoke_test.py`;
- do not commit raw third-party datasets, model weights, API keys, or private annotations;
- add or update a config for any experimental change;
- document result-affecting changes in the PR body.

## Result integrity
Never edit final metric values directly into manuscript tables. Generate them from raw prediction/result files and preserve the run manifest.
