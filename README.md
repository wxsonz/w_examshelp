idk bruh i was going to do C10 but then i realize i have skill issue.
so i waste tokens making things for people in my pool instead.

# ExamsHelp ⚡

A zero-dependency CLI for practising the 42 exams. Python 3 and `gcc`, nothing
else to install.

```bash
./examshelp
```

Put your code in the exercise folder the dashboard points at — for example
`rendu/aff_a/aff_a.c` — save, and run `grademe`. No git, no push, no commit.

The shell scrolls like a normal shell: each command prints below the last, and
your terminal's own scrollback is the history.

## Language

The whole interface speaks English and Thai. `lang th` and `lang en` both work,
and so do `lang thai`, `lang english`, `lang ไทย` — case-insensitive. The current
language sits in the prompt, so it is always in view:

```
🇹🇭 ไทย swift-panda-matcha ❯
```

Subjects, the interface, hints and grading feedback are all translated. The
per-exercise notes written in the pack (`hints=[...]`) are still English only, so
a Thai session shows Thai advice followed by English exercise-specific notes.

## What makes the grading trustworthy

Every exercise ships a **reference solution**. The expected output of every test
is produced by compiling and running that reference, never written by hand, so a
subject and its tests cannot disagree. The build also compiles a do-nothing stub
for each exercise and **refuses to ship any exercise that the stub can pass**.

Currently 75 exercises, 437 tests, all verified.

## Exams, not one long ladder

The pack mirrors the real 2026 Piscine pool: four exams, each with its own levels,
and an exercise sits at a *different* level in each exam it appears in
(`repeat_alpha` is exam 01 level 5 and exam 02 level 0). `exam` lists them and
switches; progress is tracked per exam, and solving an exercise counts wherever
it appears.

A fifth track, `extra`, holds 16 exercises that are not in the 2026 pool. They
stay as drill and are labelled as such everywhere, so they are never mistaken for
exam material.

Your submission is compiled with `-Wall -Wextra -Werror` and compared byte for
byte, so a missing trailing newline fails — as it does in the real exam. Function
exercises are linked against a harness that supplies `main()`, with your own
headers on the include path, so multi-file exercises like the `ft_list_*` family
work properly.

## Commands

| Command | Description |
|---|---|
| `subject` | Read the current assignment |
| `hint` | What to watch out for on this exercise |
| `grademe` | Compile and test what is in `rendu/` |
| `status` | Session, exam, level, and current exercise |
| `list` | This exam's exercises; `list all` for every exam |
| `exam` | List the exams; `exam 03` or `exam extra` switches |
| `skip` | Move to another exercise, and show its subject |
| `lang en\|th` | Switch language (English / ไทย) |
| `archive` | Snapshot `rendu/` into `history/` |
| `history` | Past archived sessions |
| `reset` | Wipe all progress and start over (asks first) |
| `exit` | Archive and quit |

Every command also works as a one-shot: `./examshelp grademe`.

Quitting archives your session to `history/<session-name>/` but **leaves
`rendu/` alone**. Only `reset` clears your code, and it asks first.

## Adding or changing exercises

`engine/config/exercises_db.json` is generated — don't edit it. The source of
truth is `engine/exercises/`. Add an entry with its subject, reference solution,
harness, test inputs and its `exams={"exam_01": 5, ...}` placement, then:

```bash
python3 engine/scripts/build_db.py            # rebuild and verify
python3 engine/scripts/build_db.py --check    # verify without writing
python3 engine/scripts/build_db.py --only ft_split
```

The build fails loudly if a reference does not compile, if its output is
non-deterministic, if a shell transcript written into a subject is not what the
reference actually prints, or if a do-nothing stub passes.

```bash
python3 engine/scripts/selftest.py       # grade every reference and every stub
python3 engine/scripts/audit_corpus.py   # compare the pack to real exam subjects
```

## Checking against real subjects

`build_db.py` proves the pack is self-*consistent*, which is not the same as
being *right*: a subject and its reference can share a misunderstanding and
verify perfectly. `audit_corpus.py` catches that by comparing against real exam
subjects placed in `references/` (external material, gitignored). It checks five
things — replayed `| cat -e` transcripts from both the subject and its
`examples.txt`, program-vs-function and exact prototype, the allowed-functions
list, coverage in both directions, and **placement**: which exam each exercise
belongs to and at what level.

Placement is what keeps the levelling honest. `sort_int_tab` sat at level 1 of
the old flat ladder when the real pool puts it at exam 04 level 2; that class of
mistake is now a build-time disagreement rather than something to notice by eye.

It earned its keep immediately: `aff_a`, `aff_z`, `str_capitalizer`,
`ft_countdown`, `lcm` and `ft_atoi_base` were all confidently wrong until it ran.
If you have no corpus, the script says so and exits 0.

Good luck with your studies.
