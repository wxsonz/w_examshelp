# ExamsHelp CLI (Antigravity Edition) ⚡

`ExamsHelp` is an educational, stress-free alternative to 42 Network's traditional "examshell". Designed for progressive learning and mastery, `ExamsHelp` guides users through C programming exercises using mechanical edge-case testing, non-punitive feedback, targeted debugging hints, exercise skipping, and session history archiving.

---

## 🚀 Key Features

* **🔒 Encapsulated Engine (`engine/`)**: All application code, databases, and visual modules are encapsulated inside `engine/` to prevent accidental deletion.
* **🐾 Cute Passphrase Session Naming**: Every session receives a passphrase name (e.g. `whistling-bear-macaron`, `brave-otter-mango`, `cosmic-fox-matcha`).
* **💾 Automatic Session Archiving (`exit` / `quit`)**: When exiting, your C submissions, active subjects, and progress are automatically saved into `history/<session_name>/`. `rendu/` is cleaned so your workspace stays neat for the next session.
* **📜 Session History Viewer (`history`)**: View all past archived sessions, completion counts, dates, and submitted `.c` files.
* **Instant Workspace Self-Healing**: Automatically repairs `subjects/` and `rendu/` if files or directories are accidentally deleted.
* **118 Exercises Across 10 Levels**: Features 18 official 42 exam exercises + 100 extended custom practice exercises.
* **Forgiving & Educational Grading**: Catch compilation errors, segfaults (`signal -11`), infinite loop timeouts (>5s), or output mismatches with **0 penalization**.

---

## 🛠️ Installation & Requirements

* **Python**: `3.8+`
* **C Compiler**: `gcc`
* **Dependencies**: `rich` (`pip install rich`)

---

## 💻 Usage & Commands

Launch `ExamsHelp` directly using the root executable:
```bash
./examshelp
```

Or execute direct commands:
```bash
./examshelp status    # Show active session name, level progress bar & assignment details
./examshelp grademe   # Evaluate your C solution in rendu/
./examshelp subject   # View the active exercise description
./examshelp hint      # View targeted advice on what to look out for in the current question
./examshelp skip      # Skip the current question and advance to the next exercise
./examshelp history   # View all past archived sessions in history/
./examshelp list      # View all 10 levels and unlocked exercises
```

---

## 📂 Reorganized Project Layout

```
examshelp/
├── engine/                   # Protected Application Core
│   ├── config/
│   │   └── exercises_db.json # 118-exercise database catalog
│   ├── ui/
│   │   ├── terminal.py       # Rich visual UI renderer
│   │   └── themes.py         # Color themes
│   ├── compiler.py           # GCC runner
│   ├── evaluator.py          # Non-punitive test runner
│   ├── hints.py              # Hint engine
│   ├── session.py            # Passphrase session manager & archiver
│   ├── state.py              # State manager & self-healing health check
│   ├── main.py               # Engine main entrypoint
│   └── scripts/
│       └── build_db.py       # Data generator
├── subjects/                 # User workspace (Active exercise text)
├── rendu/                    # User workspace (Student C source files)
├── history/                  # Session archives (C submissions & subjects)
├── examshelp                 # Executable root launcher script
└── README.md                 # User documentation
```
