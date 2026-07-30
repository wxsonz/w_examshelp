# Adding an exercise

An exercise is a directory of ordinary files under `exercises/`. No Python, no
escaping, no editing a file somebody else is also editing.

```bash
python3 engine/scripts/new_exercise.py alen --exams exam_01/4
python3 engine/scripts/build_db.py --only alen
```

The skeleton it writes is a *working* exercise — it compiles, its tests run, its
stub fails. Check that it builds, then change one thing at a time.

## The directory

```
exercises/alen/
├── exercise.conf      where it sits, and what may be called
├── subject.en.txt     the subject, exactly as the student reads it
├── subject.th.txt     the same in Thai
├── alen.c             your reference solution — a real .c file
├── tests              one test per line
└── hints.en.txt       optional
```

Optional extras, picked up by being there:

| file | meaning |
|---|---|
| `harness.c` | the `main()` the grader links against. Required for function exercises. |
| `stub.c` | a hand-written do-nothing solution, when the generated one will not compile. |
| anything else `.c` / `.h` | part of what the student submits (`ft_list.h`). |

`gcc exercises/alen/alen.c` works from a shell. That is the point.

## exercise.conf

```
exams     : exam_01/5 exam_02/1
allowed   : write, exit
prototype : void ft_putstr(char *str);
```

| key | |
|---|---|
| `exams` | **required.** `exam_01/5` is exam 01, level 5. List several, space separated — an exercise sits at a *different* level in each exam it appears in. |
| `allowed` | **required.** Comma separated. Empty means nothing at all, not even `write()`. |
| `prototype` | Present ⇒ this is a function exercise, and `harness.c` must supply `main()`. |
| `source` | `piscine_2026` (default), `added`, or `extra`. See below. |
| `files` | Only if the derived order is wrong. Defaults to `<name>.c` first, then every other `.c`/`.h` in the directory. |

Anything else in the file is a typo and the build says so, because a silently
ignored typo in `allowed` is a grading bug.

### source

- **`piscine_2026`** — really in the 2026 pool. `audit_corpus.py` will check your
  placement against the real exams and fail the build if it disagrees.
- **`added`** — not in the pool, but good enough to earn a place on a ladder.
  Shown with a note on the subject and a `*` in `list`.
- **`extra`** — drill only. Then the only placement allowed is `extra/N`.

## tests

```
# a bare `$` runs it with no arguments
$ hello
$ 'two words'
$ ''
$
$ 'has  spaces'   # comments are allowed
```

Use `\t` and `\n` for a tab or newline inside an argument, and `\\` for a
backslash.

**You never write the expected output.** The build compiles your reference,
runs it against each line, and records what it actually printed. That is why a
subject and its tests cannot drift apart — and why your reference has to be
right.

## What the build will refuse

`python3 engine/scripts/build_db.py` fails, loudly, if:

- the reference does not compile with `-Wall -Wextra -Werror`;
- it produces different output on two runs of the same input;
- a `$> ./prog ... | cat -e` transcript written into the subject is not what the
  reference actually prints;
- **a do-nothing stub passes every test.** An exercise that cannot tell a real
  solution from `int main(void){return 0;}` asserts nothing, and will not ship.

Then:

```bash
python3 engine/scripts/selftest.py        # grade every reference and every stub
python3 engine/scripts/audit_corpus.py    # compare against real exam subjects
```

## Writing the subject

Say exactly what is printed, including whether it ends with a newline — the
grader compares bytes. Write examples as real shell transcripts:

```
  $> ./alen "hello" | cat -e
  5$
```

Every `$>` line in a subject is executed against your reference at build time, so
an example that lies is a build failure rather than a student's wasted hour.

Both `subject.en.txt` and `subject.th.txt` are required. If you cannot write the
Thai, open the PR with the English in both and say so — it is easier to fix a
translation than to write the exercise.
