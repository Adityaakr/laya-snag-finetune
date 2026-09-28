# Snag integration files

These files run inside the Snag monorepo (the TypeScript review pipeline and its eval CLI). They are included so the data generation and evaluation are inspectable, not because they run standalone here.

| File | Role in Snag |
|---|---|
| `build-trainset.ts` | runs Snag's real pipeline on every mutation-corpus dev item with `OracleJev`, writing `.laya/data/records.jsonl` (published here as `training/laya/data/oracle-records.jsonl.gz`) |
| `oracle.ts` | `OracleJev`: answers typed questions from item labels and seed annotations, records a training target only where the labels decide it, and refuses test-split seeds |
| `adjudications.ts` | audited label corrections applied by the oracle (exclude uncertain, relabel audited cases) |
| `eval-remit-laya.sh` | starts the local engine and runs golden, mutations and SWE-bench evaluations |
| `slice-report.mjs` | slices a mutation report by seed |
| `probe-llm-jev.ts` | probes the LLM-backed engine used as the reference |

In Snag they live at `scripts/laya/` and `packages/eval/src/`.
