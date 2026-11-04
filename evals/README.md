# Evals

`commands.yaml` lists messages in Thai and English with the tool Aiko should pick (`none` means a normal reply).
`scripts/run_evals.py` scores tool-choice accuracy and speed with the model in `config.yaml`:

```powershell
.venv\Scripts\python.exe scripts\run_evals.py                 # model from config.yaml
.venv\Scripts\python.exe scripts\run_evals.py --model qwen3:4b # compare another model
```

Phase 1 baseline (qwen3:1.7b, i5-12450H, no GPU): 16/18 correct (89%), 4.4 s per message on average.
Misses: "จำไว้นะว่า..." and "ขอดูโน้ตล่าสุด" got a normal reply instead of a tool.
Longer tool descriptions with more Thai keywords made it worse (72%), so keep them short.

Prompt tries on 2026-11-04 (2 rounds each, 36 tool cases + 16 Thai replies checked for ค่ะ):

| Prompt | Tool choice | Avg time | Female-only Thai endings |
| --- | --- | --- | --- |
| Current (with the ค่ะ/คะ line) | 31/36 (86%) | 6.0 s | 14/16 |
| Shorter, names `take_note`/`list_notes` in the prompt | 17/36 (47%) | 3.9 s | 14/16 |
| Current + "never ผม" | 26/36 (72%) | 4.5 s | 13/16 |

Kept the current prompt. The remaining ครับ/ผม slips are fixed in code by `female_thai()` in `application/prompts.py`.
qwen3:4b was too slow on this PC (over 20 minutes for the eval, RAM full), so it was dropped.
