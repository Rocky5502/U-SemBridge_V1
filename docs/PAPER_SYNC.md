# Paper ↔ code synchronization

During pre-experiment development, the code repository is the source of truth for configs, prompts, dataset manifests, result schemas, and analysis code. The manuscript is kept separately to reduce stale duplication.

At every paper milestone:
1. record the code commit used;
2. export tables/plots from that commit’s result files;
3. copy only generated artifacts and verified text changes into the manuscript;
4. store the code commit in the paper reproducibility statement;
5. at submission, archive/sync the exact manuscript source under `paper/` or a release tag.
