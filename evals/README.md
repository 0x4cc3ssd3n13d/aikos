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
