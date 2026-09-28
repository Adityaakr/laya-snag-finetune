# Checkpoints

The fine-tuned weights are **not stored in git**: each is 843 MB (GitHub rejects files over 100 MB), and none met the quality bar for distribution. This card records what exists and how to rebuild it.

| Checkpoint | What it is | Parameters | Weights file | SHA-256 of `model.safetensors` |
|---|---|---|---|---|
| `remit-laya-v1` | first fine-tune (OracleJev data, 2 epochs, top 6 layers); held-out question accuracy 82.1%, end-to-end 1/21 held-out defects | 421,293,830 | 843 MB (fp16) | `bb4a25640e532e2fb20a303ea180306efa8cf356ff07f5691233dc558f653773` |
| `remit-laya-stageA` | Stage A diagnostic (adjudicated data, 4 core questions, short inputs); failed its gate | 421,293,830 | 843 MB (fp16) | `aeeb64903f1a723d1a4a6a65e90484e363941228e9db4ebdd75d2d9d88c9923c` |

E7 (the controlled pair experiment) trains a fresh model per fold and saves results only (`training/laya/pairs/results-*.json`).

## Layout of a checkpoint folder

```
model.safetensors        full state dict, fp16 (encoder, 2-layer head, type embeddings, scorer, act head)
encoder/config.json      ModernBERT-large config (max_position_embeddings 8192)
tokenizer/               tokenizer files
rl_agent_config.json     Laya config: max_len 4096, head_max_len 512, fitted temperatures, provenance
```

Load with `laya.agent.Agent("/abs/path/to/checkpoint")`, or serve with `LAYA_REMIT_DIR=<dir> python scripts/laya/server.py` (model name `remit-laya`).

## Rebuild

```bash
.venv/bin/python -u scripts/laya/train.py --epochs 2 --accum 8 --checkpointing --name remit-laya-rebuild
```

Training is deterministic up to MPS kernel nondeterminism, so checksums of a rebuild will differ; compare the metrics in the log instead. The dataset hash in `.laya/runs/<name>/manifest.json` identifies the exact encoded data.
