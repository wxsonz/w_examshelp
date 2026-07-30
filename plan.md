# Plan: align ExamsHelp with the 2026 Piscine exam pool

Status: **done** (v0.5.0). 75 exercises, 437 tests, zero corpus disagreements
including the new placement axis. Sections 1-8 all landed; the "Deferred" list at
the bottom is still deferred and is the natural next pass.

Two things were decided while implementing, and differ from the text below:

- the database and state key is `tracks` / `current_track`, not `exams` /
  `current_exam` -- `extra` is a track and calling it an exam would be a lie;
- `completed_exercises` stays a single global list rather than being split per
  exam. Names are unique across the pool, and solving `ft_strcpy` in exam_01
  should not leave it unsolved in exam_02.

Everything below is the plan as agreed, kept for the reasoning.

## Context

The pack's low levels are outdated relative to the 2026 Piscine and its difficulty
ordering is wrong. `references/PISCINE_PART` (4 exams, 71 exercises, 112
authoritative `subject.en.txt`) makes it measurable:

- **The 11 easiest real exercises — the pack has only 5.** Missing `only_a`,
  `only_z`, `maff_alpha`, `maff_revalpha`, `aff_first_param`, `aff_last_param`,
  plus `ft_putstr` and `search_and_replace` just above. The bottom of the ladder
  is where a learner starts and it is the thinnest part.
- **Levels disagree with reality.** `sort_int_tab` sits at pack level 1 but is
  `exam_04/2` — near the top. The flat 10-level ladder was assigned by hand and
  never checked against ground truth.
- **16 pack exercises are not in the 2026 pool at all**, yet are presented with
  the same authority as real exam material.

Outcome: the pack mirrors the real structure (pick an exam, climb its levels), the
easy end is properly populated, and non-2026 material is visibly drill.

### Decisions taken

| Question | Decision |
|---|---|
| Corpus source | **Both** `references/PISCINE_PART` and `references/new` (does not exist yet); `references/new` wins on conflict |
| Level model | **Mirror the exams** — add an exam concept rather than one flat ladder |
| The 16 off-pool exercises | **Keep, clearly flagged** as a separate `extra` track |
| Scope of this pass | **Low levels first** — the 8 easy exercises + re-levelling |

### Corpus caveat

Corpus *solutions* are not trustworthy: 22 of 67 fail `-Wall -Wextra -Werror`, and
`ft_strdup` reads an uninitialised variable. Use their `subject.en.txt`,
`examples.txt` and level placement; write every reference by hand.

`references/` is gitignored (it carries its own `.git`), which is why the
placement data is written out in full below.

## 1. Corpus loading (both sources)

`engine/scripts/audit_corpus.py` globs two fixed layouts today and misses
PISCINE_PART entirely. Replace the loaders with one recursive walk:

- find every `subject*.txt` under the corpus root;
- **key each subject by its `Assignment name :` field, not by path** — robust
  across all three layouts and whatever shape `references/new` has;
- when the path matches `exam_(\d+)/(\d+)/<name>/`, record `(exam, level)` as the
  corpus placement;
- ingest `examples.txt` as an extra transcript source — it is already in the
  `$> ./prog … | cat -e` form, so reuse `_parse_transcripts` from
  `engine/scripts/build_db.py` instead of writing a second parser;
- `references/new` wins when the same assignment name appears in both.

Keep the current "no corpus → say so, exit 0" behaviour.

## 2. Exam/level data model

`engine/exercises/spec.py` — replace the single `level=` argument:

```python
ex(name, exams={"exam_01": 4, "exam_02": 0}, source="piscine_2026", ...)
```

- `exams`: exam id → level within that exam. An exercise legitimately appears in
  several exams at different levels, and the levels are **not** a constant offset
  (`repeat_alpha` is `exam_01/5` but `exam_02/0`).
- `source`: `"piscine_2026"` or `"extra"`. Validated in `spec.validate()`: an
  `extra` exercise must live in the `extra` track and must not claim an exam id.

`engine/config/exercises_db.json` — store each exercise **once**, index placement
separately, so multi-exam exercises are not duplicated:

```json
{ "exercises": { "aff_a": {...} },
  "exams": { "exam_01": { "levels": { "0": ["aff_a", "..."] } } } }
```

`engine/scripts/build_db.py` emits the new shape. All existing guarantees stay:
reference compiles, output deterministic, subject transcripts match, do-nothing
stub must fail.

## 3. Progress state, with migration

`engine/state.py` — progress becomes per-exam:

```json
{ "current_exam": "exam_01",
  "progress": { "exam_01": {"level": 2, "completed": ["aff_a"]} },
  "total_completions": 12 }
```

Migration matters because **level numbers change meaning**. On loading an old
state file: keep `completed_exercises` (names are still valid) and
`total_completions`, then recompute each exam's level as the lowest level still
holding an uncompleted exercise. Do not carry old level integers across.

`get_current_exercise`, `_advance_exercise` and
`_select_random_exercise_for_level` become exam-scoped. The level ceiling is
per-exam (exam_01 has 8 levels, exam_04 has 4), not a hardcoded 10.

## 4. New exercises (8, all low level)

Each needs a hand-written reference, EN + TH subject, tests and hints. Confirmed
against both the corpus subjects and their solutions.

| exercise | placement | kind | allowed | behaviour |
|---|---|---|---|---|
| `only_a` | exam_01/3 | program | write | writes `a`, **no newline** |
| `only_z` | exam_01/3 | program | write | writes `z`, **no newline** |
| `maff_alpha` | exam_01/1 | program | write | `aBcDeFgHiJkLmNoPqRsTuVwXyZ` + `\n` |
| `maff_revalpha` | exam_01/3 | program | write | `zYxWvUtSrQpOnMlKjIhGfEdCbA` + `\n` |
| `aff_first_param` | exam_01/2 | program | write | first arg + `\n`; no args → `\n` |
| `aff_last_param` | exam_01/2 | program | write | last arg + `\n`; no args → `\n` |
| `ft_putstr` | exam_01/6 | function | write | `void ft_putstr(char *str);` |
| `search_and_replace` | exam_01/5 | program | write, exit | exactly 3 args; arg2 and arg3 must each be a single character (`argv[n][1] == '\0'`), else `\n` only; replace every occurrence, then `\n` |

Gotchas worth not re-litigating later:

- `only_a` / `only_z` print **no** trailing newline. The subject is silent; only
  the corpus solution settles it. Leave a comment in the pack saying so.
- `maff_alpha` — "even letters uppercase, odd lowercase" counts from 1, so `a`
  (1st, odd) is lowercase: `aBcDeF…`.
- `search_and_replace` rejects multi-character search/replace args:
  `./search_and_replace "zaz" "art" "zul"` prints only a newline.
- `ft_putstr` needs a harness. The corpus `main.c` calls `ft_putstr(argv[1])` with
  no `argc` check — write a hardened one instead of copying it.

## 5. Corpus placement (authoritative, for re-levelling)

Derive every `exams=` mapping from this table rather than by judgement.

```
exam_01/0  aff_a ft_countdown ft_print_numbers
exam_01/1  hello maff_alpha
exam_01/2  aff_first_param aff_last_param aff_z
exam_01/3  maff_revalpha only_a only_z
exam_01/4  ft_strcpy ft_strlen
exam_01/5  repeat_alpha search_and_replace ulstr
exam_01/6  first_word ft_putstr ft_swap
exam_01/7  rev_print rot_13 rotone

exam_02/0  ft_strcpy ft_strlen repeat_alpha
exam_02/1  search_and_replace ulstr
exam_02/2  first_word ft_putstr ft_swap
exam_02/3  rev_print rot_13 rotone
exam_02/4  ft_atoi ft_strdup inter
exam_02/5  last_word reverse_bits swap_bits union
exam_02/6  alpha_mirror do_op ft_strcmp ft_strrev
exam_02/7  is_power_of_2 max print_bits wdmatch

exam_03/0  ft_atoi ft_strdup inter last_word reverse_bits swap_bits union
exam_03/1  alpha_mirror do_op ft_strcmp ft_strrev is_power_of_2 max print_bits wdmatch
exam_03/2  add_prime_sum epur_str ft_list_size ft_rrange hidenp pgcd print_hex rstr_capitalizer
exam_03/3  expand_str ft_atoi_base ft_range lcm paramsum str_capitalizer tab_mult

exam_04/0  add_prime_sum epur_str ft_list_size ft_rrange hidenp pgcd print_hex rstr_capitalizer
exam_04/1  expand_str ft_atoi_base ft_range lcm paramsum str_capitalizer tab_mult
exam_04/2  brainfuck check_mate flood_fill fprime ft_itoa ft_itoa_base ft_list_foreach
           ft_list_remove_if ft_split rev_wstr rostring sort_int_tab sort_list
exam_04/3  biggest_pal brackets cycle_detector options print_memory rpn_calc
```

## 6. The `extra` track

These 16 are not in the 2026 pool. Move them to a fifth track `extra`, keeping
their current relative order compressed to contiguous levels 0..N. They stay
usable as drill and are never shown as exam material.

```
fizzbuzz  ft_putchar  is_negative  ft_strspn  ft_strjoin  ft_sort_string_tab
ft_list_at  ft_list_push_front  ft_list_push_back  ft_list_reverse
ft_list_sort  sorted_list_insert  eval_expr  permutations  ft_printf  n_queens
```

Note `ft_list_sort` stays an extra: the corpus's equivalent is `sort_list`
(`exam_04/2`) with a different prototype, and that one is deferred.

## 7. UI and i18n

- New `exam` command: list exams with progress, and switch. Accept `exam 02`,
  `exam_02`, `extra` — reuse the alias-resolution pattern from
  `resolve_language` in `engine/i18n.py`.
- `status`: show the current exam alongside the level, and the exercise's track.
- `list`: default to the current exam grouped by level; `list all` for everything.
- `subject`: show the track so `extra` is unmistakable.
- New message keys in **both** `en` and `th` in `engine/i18n.py`.
  `validate_catalog()` already enforces key/placeholder parity, and `check_ui()`
  in `engine/scripts/selftest.py` already drives every command in every language —
  add `exam` and its failure paths to its `invocations` list.

## 8. Placement audit (new axis)

Add a fifth axis to `audit_corpus.py` beside behaviour / structure / constraints /
coverage: **placement** — every `piscine_2026` exercise's `exams` mapping must
equal the corpus's. This is the check that would have caught `sort_int_tab`, and
it makes the re-levelling self-verifying instead of hand-checked.

## Verification

```bash
python3 engine/scripts/build_db.py            # rebuild; all invariants enforced
python3 engine/scripts/selftest.py            # references pass, stubs fail, UI smoke
python3 engine/scripts/audit_corpus.py        # must report zero disagreements
```

Expected: **75 exercises** (67 + 8), zero corpus disagreements including the new
placement axis, and `only_a`/`only_z` proving the no-newline rule via their
generated tests.

Then drive the real thing, since state and UI both changed:

```bash
./examshelp                 # exam switching, level progression, list, status
./examshelp lang th         # exam UI in Thai
```

Manually confirm: a fresh run starts at `exam_01` level 0 among
`aff_a`/`ft_countdown`/`ft_print_numbers`; an old `.examshelp_state.json` migrates
without losing completed exercises; `extra` reads as a separate track.

## Deferred (not this pass)

The other 12 missing 2026 exercises, each needing a trustworthy hand-written
reference:

```
brainfuck  check_mate  fprime  ft_itoa_base  rev_wstr  sort_list
rstr_capitalizer  biggest_pal  brackets  cycle_detector  options  rpn_calc
```

The placement audit will keep reporting these as missing coverage until they
land. That is the correct signal, not a failure.
