# คู่มือโปรเจกต์ AIKOs

AIKOs (Artificial Intelligence Kontrol Operating System) คือเลขาส่วนตัวที่สั่งงานด้วยเสียง และรันบนคอมพิวเตอร์ของเราเอง
เอกสารนี้สรุปว่าทำอะไรไปแล้ว ติดตั้งอะไรไว้ โค้ดจัดโครงสร้างแบบไหน และไฟล์ไหนทำหน้าที่อะไร เอาไว้อ่านทบทวนภายหลัง

อัปเดตล่าสุด: 2026-10-21 (หลังจบ Phase 0 และปรับโครงสร้างเป็น Clean Architecture)

---

## 1. สิ่งที่ทำไปแล้ว (ไทม์ไลน์)

| ขั้น | สิ่งที่ทำ | ผล |
| --- | --- | --- |
| Phase 0 | รันสคริปต์ `setup-phase0.ps1` เพื่อติดตั้งโปรแกรม สร้างโปรเจกต์ และโหลดโมเดล | ทดสอบผ่าน 3/3 (อังกฤษ 29.8 tokens/s, ไทย 17.3 tokens/s) |
| Phase 0 | สร้าง repo แบบ private บน GitHub และ push commit แรก | https://github.com/0x4cc3ssd3n13d/aikos (`db0a048`) |
| เครื่องมือ | ติดตั้ง Node.js LTS, uv, graphify, Anthropic skills, ponytail, omniroute แบบ global | ใช้ได้กับทุกโปรเจกต์ |
| Clean Architecture | Pull request #1 ปรับโค้ดเป็น 4 ชั้น (domain, application, infrastructure, interface) | merge แล้ว (`d4687e6`) เทสต์ผ่าน 21/21 และกฎโครงสร้างผ่าน 4/4 |

ปัญหาที่เจอระหว่างทาง (เผื่อเจออีก):
- **ดาวน์โหลดไม่ผ่าน** (error `0x80072ee7`, `0x80072f19`, `0x80072ee2`): เน็ตหลุดหรือช้า แก้ด้วยการโหลดแบบต่อจากจุดเดิม (`curl.exe -C -`)
- **ติดตั้งไม่ผ่าน** (error `1602` หรือ `1603`): หน้าต่าง Windows ขออนุญาตไม่ได้ถูกกด Yes หรือหมดเวลา
- **PowerShell ไม่รัน `npm`**: Windows บล็อกสคริปต์ `.ps1` ให้ใช้ `npm.cmd` แทน
- **โปรแกรมเพิ่งติดตั้งแต่หาไม่เจอ**: ต้องปิดแล้วเปิดหน้าต่าง PowerShell ใหม่ เพื่อให้ค่า PATH อัปเดต

---

## 2. ข้อมูลเครื่อง

| รายการ | ค่า |
| --- | --- |
| OS | Windows 11 Home Single Language (10.0.26200) |
| RAM | 15.7 GB |
| CPU | Intel Core i5-12450H (8 cores, 12 threads) |
| GPU | Intel UHD Graphics (ไม่มีการ์ดจอแยก โมเดลรันบน CPU) |
| ดิสก์ | SSD ว่างประมาณ 290 GB |
| โปรไฟล์ที่ใช้ | `minimum` (ออกแบบให้รันได้บนเครื่อง RAM 4 GB) แต่เครื่องนี้แรงพอสำหรับ `standard` |

---

## 3. สิ่งที่ติดตั้งแล้ว

### โปรแกรมหลัก

| โปรแกรม | เวอร์ชัน | ใช้ทำอะไร |
| --- | --- | --- |
| Python | 3.12.10 | ภาษาหลักของ AIKOs |
| Git | 2.55.0 | เก็บประวัติโค้ด ย้อนกลับได้ |
| VS Code | 1.128.0 | โปรแกรมเขียนโค้ด (มี extension Python) |
| Ollama | 0.40.5 | รันโมเดล AI ในเครื่อง ที่ `http://127.0.0.1:11434` |
| GitHub CLI (`gh`) | 2.102.0 | ล็อกอิน GitHub และจัดการ repo หรือ PR ผ่านคำสั่ง |
| Node.js LTS | 24.20.0 | ใช้รันเครื่องมือที่เขียนด้วย JavaScript (npm, npx) |
| uv | 0.13.3 | ติดตั้งเครื่องมือ Python แบบ global |

### โมเดล AI (Ollama)

| โมเดล | ขนาด | ใช้ทำอะไร |
| --- | --- | --- |
| `qwen3:1.7b` | 1.4 GB | สมองหลักของ AIKOs สำหรับคุยและตอบคำถาม |
| `nomic-embed-text` | 274 MB | แปลงข้อความเป็นตัวเลข ใช้ค้นหาความจำ (Phase หลัง) |

### แพ็กเกจ Python ในโปรเจกต์ (อยู่ใน `.venv`)

| แพ็กเกจ | เวอร์ชัน | ใช้ทำอะไร |
| --- | --- | --- |
| ollama | 0.6.3 | คุยกับ Ollama จาก Python |
| PyYAML | 6.0.3 | อ่านไฟล์ `config.yaml` |
| pydantic | 2.14.1 | ตรวจว่าค่าตั้งค่าถูกต้อง |
| pytest | 9.1.1 | รันเทสต์ (สำหรับพัฒนา) |
| import-linter | 2.15 | ตรวจกฎ Clean Architecture (สำหรับพัฒนา) |

### เครื่องมือสำหรับ Claude Code (ติดตั้งแบบ global)

| เครื่องมือ | อยู่ที่ไหน | ใช้ทำอะไร |
| --- | --- | --- |
| graphify 0.9.93 | `~/.claude/skills/graphify` | สร้างแผนผังความสัมพันธ์ของโค้ด สั่งด้วย `/graphify .` |
| Anthropic skills (20 ตัว) | `~/.claude/skills/` | เช่น `pdf`, `docx`, `xlsx`, `pptx`, `skill-creator`, `mcp-builder`, `webapp-testing` |
| ponytail | plugin ใน `~/.claude/settings.json` | บังคับให้ AI เขียนโค้ดน้อยที่สุดที่ยังครบงาน มี `/ponytail-review` ไว้รีวิวโค้ด |
| plugin ทางการของ Anthropic 6 ตัว | `~/.claude/settings.json` (marketplace `claude-plugins-official`) | ralph-loop, feature-dev, pr-review-toolkit, code-simplifier, security-guidance, claude-security (ดูหัวข้อ 8) |
| omniroute 3.8.52 | npm global | ตัวกลางเชื่อมเครื่องมือเขียนโค้ดกับผู้ให้บริการ AI หลายเจ้า |

การตั้งค่า omniroute:
- เปิดใช้งาน: พิมพ์ `omniroute.cmd` ใน PowerShell แล้วเปิด http://127.0.0.1:20128
- ตั้ง `OMNIROUTE_SERVER_HOST=127.0.0.1` (ตัวแปรของ user) ให้เข้าได้จากเครื่องนี้เท่านั้น
- กุญแจเข้ารหัส API key อยู่ที่ `C:\Users\csnv_\.omniroute\.env` ห้ามลบหรือแชร์ ถ้าหาย จะเปิดอ่าน key ที่บันทึกไว้ไม่ได้
- ฐานข้อมูลเก่าจากครั้งแรกเก็บไว้ที่ `C:\Users\csnv_\.omniroute\backup-before-encryption-20261021-013812`

---

## 4. โครงสร้างโค้ด: Clean Architecture

### แนวคิดแบบง่าย

แบ่งโค้ดเป็นชั้นเหมือนหัวหอม ชั้นในสุดคือกฎของงาน ชั้นนอกคือเครื่องมือจริง (Ollama, ไฟล์, Windows)
**ชั้นนอกเรียกใช้ชั้นในได้ แต่ชั้นในห้ามรู้จักชั้นนอก**
ข้อดี: ถ้าวันหนึ่งเปลี่ยนจาก Ollama เป็น Claude ก็แก้แค่ชั้นนอก ส่วนกฎและ use case ไม่ต้องแตะ และเทสต์ชั้นในได้โดยไม่ต้องเปิด Ollama

```text
        ┌───────────────────────────────────────────┐
        │ bootstrap  (อ่าน config + ประกอบทุกชิ้น)   │
        │  ┌──────────────┐    ┌──────────────────┐ │
        │  │ interface    │    │ infrastructure   │ │
        │  │ CLI, เสียง    │    │ Ollama, ไฟล์      │ │
        │  └──────┬───────┘    └────────┬─────────┘ │
        │         ▼                     ▼           │
        │       ┌───────────────────────────┐       │
        │       │ application               │       │
        │       │ use cases + ports         │       │
        │       │   ┌───────────────────┐   │       │
        │       │   │ domain            │   │       │
        │       │   │ กฎและข้อมูลล้วน     │   │       │
        │       │   └───────────────────┘   │       │
        │       └───────────────────────────┘       │
        └───────────────────────────────────────────┘
        ลูกศร = ทิศทางการ import (ชี้เข้าข้างในเท่านั้น)
```

| ชั้น | โฟลเดอร์ | import ได้จาก | หน้าที่ |
| --- | --- | --- | --- |
| Domain | `src/aikos/domain/` | ไม่มี (Python ล้วน) | กฎและข้อมูล เช่น ข้อความต้องไม่ว่าง เวลาต้องมี time zone |
| Application | `src/aikos/application/` | domain | สิ่งที่ AIKOs ทำได้ (use case) และ "ปลั๊ก" ที่ต้องการ (port) |
| Infrastructure | `src/aikos/infrastructure/` | application, domain, ไลบรารีภายนอก | ของจริงที่เสียบเข้า port เช่น Ollama, ไฟล์ Markdown |
| Interface | `src/aikos/interface/` | application, domain | ช่องทางที่ผู้ใช้คุยกับ AIKOs เช่น terminal, เสียง (ภายหลัง) |
| Bootstrap | `src/aikos/bootstrap/` | ทุกชั้น | อ่าน `config.yaml` แล้วประกอบชิ้นส่วนเข้าด้วยกัน |

คำศัพท์:
- **Port**: สัญญาว่า "ต้องมีความสามารถนี้" เขียนเป็น `Protocol` เช่น `LanguageModel` ต้องมีเมธอด `reply()`
- **Adapter**: ของจริงที่ทำตามสัญญา เช่น `OllamaLanguageModel` ทำตาม `LanguageModel`
- **Use case**: งานหนึ่งอย่าง เป็นคลาสที่มีเมธอด `execute()` เช่น `Chat`, `TakeNote`
- **Composition root**: จุดเดียวที่ประกอบทุกอย่างเข้าด้วยกัน (`bootstrap/container.py`)

กฎถูกบังคับด้วย `lint-imports` (สัญญา 4 ข้อใน `pyproject.toml`) และ `tests/test_architecture.py`
**ห้ามแก้สัญญาให้หลวมลงเพื่อให้โค้ดผ่าน**

---

## 5. ไฟล์ไหนทำอะไร

### ไฟล์ระดับบนสุด

| ไฟล์ | หน้าที่ |
| --- | --- |
| `config.yaml` | ค่าตั้งค่าทั้งหมด (ชื่อ, โมเดล, เสียง, cloud, ความปลอดภัย, โฟลเดอร์ข้อมูล) ห้าม hard-code ในโค้ด |
| `pyproject.toml` | ข้อมูลแพ็กเกจ, dependency, ค่าของ pytest และกฎ import-linter |
| `requirements.txt` | แพ็กเกจที่ใช้ตอนรันจริง (สคริปต์ Phase 0 ใช้ติดตั้ง) |
| `CLAUDE.md` | กฎสำหรับ Claude เวลาทำงานในโปรเจกต์นี้ |
| `README.md` | ภาพรวมสั้นๆ และคำสั่งรัน |
| `.gitignore` | ไฟล์ที่ไม่เก็บใน Git: `.venv/`, `data/`, `sandbox/`, `.env`, `pc-specs.txt` |
| `pc-specs.txt` | สเปกเครื่อง (ไม่ขึ้น GitHub) |

### `src/aikos/`

| ไฟล์ | ชั้น | หน้าที่ |
| --- | --- | --- |
| `main.py` | จุดเริ่ม | อ่าน `--config`, โหลดค่าตั้ง, ประกอบ container แล้วเปิดหน้าแชท |
| `__main__.py` | จุดเริ่ม | ทำให้รัน `python -m aikos` ได้ |
| `domain/conversation.py` | Domain | `Role`, `Message` (ห้ามว่าง), `Conversation` (จำแค่ `max_turns` รอบล่าสุด) |
| `domain/note.py` | Domain | `Note` ต้องมีข้อความ และเวลาต้องมี time zone |
| `domain/reminder.py` | Domain | `Reminder` และ `is_due()` (ใช้ใน Phase 4) |
| `domain/errors.py` | Domain | `DomainError`, `InvalidInput` สำหรับข้อมูลผิดกฎ |
| `application/prompts.py` | Application | system prompt ของ Aiko (ชื่อ ไอโกะ, แทนตัวว่า "ฉัน", ภาษา, ห้ามอ้างว่าทำสิ่งที่ไม่ได้ทำ) |
| `application/ports/language_model.py` | Application | port `LanguageModel.reply(messages)` |
| `application/ports/note_repository.py` | Application | port `NoteRepository.save()` และ `list_recent()` |
| `application/ports/clock.py` | Application | port `Clock.now()` (ทำให้เทสต์ล็อกเวลาได้) |
| `application/ports/speech.py` | Application | port เสียง: `SpeechToText`, `TextToSpeech`, `WakeWordDetector` (Phase 2-3) |
| `application/use_cases/chat.py` | Application | `Chat.execute(text)` ส่งประวัติแชทให้โมเดลแล้วจำคำตอบ |
| `application/use_cases/take_note.py` | Application | `TakeNote.execute(text)` สร้างโน้ตพร้อมเวลาแล้วบันทึก |
| `infrastructure/llm/ollama_model.py` | Infrastructure | `OllamaLanguageModel` เรียก Ollama, เติม `/no_think`, ตัด `<think>...</think>` ออก |
| `infrastructure/storage/markdown_notes.py` | Infrastructure | `MarkdownNoteRepository` เก็บโน้ตเป็นไฟล์ `data/notes/YYYY-MM-DD.md` วันละไฟล์ |
| `infrastructure/system/clock.py` | Infrastructure | `SystemClock` เวลาเครื่องพร้อม time zone |
| `infrastructure/{calendar,email,files,notify,scheduler,speech}/` | Infrastructure | โฟลเดอร์เตรียมไว้สำหรับ Phase หลัง (ยังว่าง) |
| `interface/cli/chat_cli.py` | Interface | `run_chat()` หน้าแชทใน terminal: `/note`, `/help`, `/quit` |
| `interface/{voice,tray}/` | Interface | เตรียมไว้สำหรับเสียงและไอคอนถาด (ยังว่าง) |
| `bootstrap/settings.py` | Bootstrap | โมเดล pydantic ของค่าตั้ง และ `load_settings()` อ่าน `config.yaml` |
| `bootstrap/container.py` | Bootstrap | `build_container()` ประกอบ Ollama + ไฟล์โน้ต + นาฬิกา เข้ากับ use case |

### `tests/`, `scripts/`, `evals/`

| ไฟล์ | หน้าที่ |
| --- | --- |
| `tests/conftest.py` | ของปลอมสำหรับเทสต์: `FakeLanguageModel`, `FixedClock`, `InMemoryNotes` |
| `tests/unit/...` | เทสต์แต่ละชั้นด้วยของปลอม ไม่ต้องเปิด Ollama |
| `tests/integration/test_markdown_notes.py` | เทสต์การเขียนและอ่านไฟล์โน้ตจริง |
| `tests/integration/test_ollama_model.py` | เทสต์กับโมเดลจริง (ต้องตั้ง `AIKOS_LIVE=1`) |
| `tests/test_architecture.py` | รัน import-linter ภายใน pytest |
| `scripts/check_phase0.py` | ตรวจ Python, แพ็กเกจ ollama และให้โมเดลตอบอังกฤษ/ไทย |
| `evals/README.md` | แผนชุดทดสอบคำสั่งเสียง (Phase 4) |

### เส้นทางของข้อความ 1 ครั้ง

```text
ผู้ใช้พิมพ์ "สวัสดี"
  → interface/cli/chat_cli.py      run_chat() รับข้อความ
  → application/use_cases/chat.py  Chat.execute() เพิ่มลง Conversation
  → port LanguageModel.reply()     (ไม่รู้ว่าข้างหลังคือใคร)
  → infrastructure/llm/ollama_model.py  ส่งไป Ollama แล้วตัด <think>
  ← คำตอบกลับมา Chat จำไว้ใน Conversation
  ← chat_cli แสดง "AIKOs> ..."
```

---

## 6. คำสั่งที่ใช้บ่อย

รันในโฟลเดอร์โปรเจกต์ (`cd $HOME\OneDrive\Desktop\aikos`):

```powershell
.venv\Scripts\python.exe -m aikos                     # คุยกับ AIKOs (/note ข้อความ, /help, /quit)
.venv\Scripts\python.exe -m pytest                    # รันเทสต์ทั้งหมด
$env:AIKOS_LIVE="1"; .venv\Scripts\python.exe -m pytest -m live   # เทสต์กับโมเดลจริง
.venv\Scripts\lint-imports.exe                        # ตรวจกฎ Clean Architecture
.venv\Scripts\python.exe scripts\check_phase0.py      # ตรวจว่า Ollama และโมเดลทำงาน
.venv\Scripts\python.exe -m pip install -e ".[dev]"   # ติดตั้งแพ็กเกจหลังดึงโค้ดใหม่
git pull                                              # ดึงโค้ดล่าสุดจาก GitHub
```

---

## 7. วิธีเพิ่มความสามารถใหม่ (ตามลำดับชั้น)

ตัวอย่าง: เพิ่ม "ตั้งเตือนความจำ" (AddReminder)

1. **Domain**: มี `Reminder` แล้ว ถ้ามีกฎใหม่ให้เพิ่มที่นี่
2. **Application**: เพิ่ม port `ReminderRepository` (Protocol) แล้วเพิ่ม use case `AddReminder` ที่มี `execute()` ไฟล์ละ 1 use case
3. **Infrastructure**: เขียน adapter เช่น `MarkdownReminderRepository` ที่ทำตาม port
4. **Bootstrap**: ประกอบใน `container.py` ถ้ามีค่าตั้งใหม่ ให้เพิ่มใน `settings.py` และ `config.yaml` (ถามผู้ใช้ก่อนแก้ config)
5. **Interface**: ให้ CLI หรือระบบเสียงเรียก use case
6. **Tests**: unit test ด้วยของปลอมใน `conftest.py`, integration test สำหรับ adapter และ eval ใน `evals/`
7. **ตรวจก่อนจบ**: `pytest` และ `lint-imports` ต้องผ่านทั้งคู่

กฎสำคัญจาก `CLAUDE.md`:
- ค่าทุกอย่างมาจาก `config.yaml`; API key มาจาก environment variable เท่านั้น
- ห้ามเรียกเน็ต ยกเว้น `cloud.enabled: true` (Ollama ในเครื่องเรียกได้)
- การกระทำที่เปลี่ยนแปลงอะไร (บันทึก, ส่ง, ลบ, เขียนทับ) ต้องถามผู้ใช้ก่อน และอีเมลทำได้แค่ร่าง
- ออกแบบให้รันบนเครื่อง RAM 4 GB ไม่มี GPU: โหลดโมเดลทีละตัว และไม่ใส่ dependency หนักใน core

---

## 8. Skills สำหรับงานนี้

plugin ทางการทั้ง 6 ตัวมาจาก marketplace `anthropics/claude-plugins-official` (ผู้สร้างคือ Anthropic) ชื่อคำสั่งจริงดูได้จาก `/help` หลังเปิด Claude Code ใหม่

| ด้าน | Skill / Plugin | ใช้เมื่อ |
| --- | --- | --- |
| เฉพาะ AIKOs | `aikos-guide` (skill ใน repo) | อยากเข้าใจหรือเพิ่มฟีเจอร์ใน AIKOs |
| Loop | `ralph-loop` | ให้ Claude ทำงานเดิมซ้ำเป็นรอบจนเสร็จ **ต้องกำหนดจำนวนรอบสูงสุดทุกครั้ง** |
| Loop | `feature-dev` | พัฒนาฟีเจอร์ครบวงจร: สำรวจโค้ด → ออกแบบ → ลงมือ → รีวิว |
| Clean code | `pr-review-toolkit` | รีวิวแยกด้าน: คุณภาพโค้ด, เทสต์, error handling, type, comment |
| Clean code | `code-simplifier` | ทำโค้ดที่เพิ่งแก้ให้อ่านง่ายขึ้น โดยไม่เปลี่ยนการทำงาน |
| Clean code | `ponytail-review` | รีวิวว่าโค้ดถูก ปลอดภัย และไม่เขียนเกินจำเป็น |
| Bug | `code-review` (มีใน Claude Code) | หาบั๊กใน diff หรือ PR |
| Security | `security-guidance` | เตือนอัตโนมัติเมื่อโค้ดมีจุดเสี่ยง (injection, XSS, รหัสลับในโค้ด ฯลฯ) และรีวิวก่อน commit |
| Security | `claude-security` | สแกนช่องโหว่แบบลึกเมื่อสั่ง แล้วเสนอวิธีแก้ให้เลือก |

ลำดับที่แนะนำเวลาทำฟีเจอร์ใหม่: `feature-dev` (หรือ `ralph-loop` สำหรับงานที่วนแก้จนผ่าน) → `pytest` + `lint-imports` → `pr-review-toolkit` → `claude-security` ก่อนเปิด PR

---

## 9. แผนต่อไป

| Phase | เป้าหมาย |
| --- | --- |
| 1 | คุยผ่านข้อความ และใช้เครื่องมือแรก (มีแชทและ `/note` แล้ว) |
| 2 | ฟังเสียง (faster-whisper) และพูดตอบด้วยเสียงผู้หญิง (Piper `en_US-amy-medium` ภาษาอังกฤษ, Edge TTS `th-TH-PremwadeeNeural` ภาษาไทย) กดปุ่ม `ctrl+alt+space` เพื่อพูด |
| 3 | คำปลุก: ได้ยิน "ไอโกะ", "Aiko" หรือ "สวัสดี ไอโกะ" แล้วตื่นทันที (วิธีตรวจจับคำไทยเลือกใน Phase 3) |

### บุคลิกของผู้ช่วย

- ชื่อ: **Aiko** ออกเสียงแบบชื่อญี่ปุ่น ภาษาไทยเรียกว่า **ไอโกะ** (โปรเจกต์ยังชื่อ AIKOs)
- แทนตัวเองว่า **"ฉัน"** และใช้เสียงผู้หญิง
- ตั้งค่าใน `config.yaml`: `assistant.name`, `assistant.name_th`, `assistant.self_pronoun_th`, `speech.wake_words`, `speech.tts_english_voice`, `speech.tts_thai_voice`
- Edge TTS ต้องใช้อินเทอร์เน็ต (บริการของ Microsoft) ซึ่งขัดกับกฎ "ไม่เรียกเน็ต" ต้องตัดสินใจใน Phase 2 ว่าจะยอมใช้ หรือหาเสียงไทยที่รันในเครื่องได้
| 4 | งานเลขา: เตือนความจำ, ตารางวันนี้, ร่างอีเมล, ค้นไฟล์ + ชุด eval |
| 6 | ใช้ Claude บน cloud เมื่อเปิด `cloud.enabled` (งบรายเดือนตาม `config.yaml`) |
