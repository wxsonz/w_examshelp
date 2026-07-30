"""UI strings in English and Thai.

Lives in engine/ rather than engine/ui/ because the grader and the hint engine
produce user-facing text too, and neither should have to import the renderer.

Not translated here: the per-exercise subjects (they carry their own subject_th)
and the per-exercise hints written in the pack, which are still English only.
"""

from engine.tracks import track_number

LANGUAGES = {
    "en": {"flag": "🇬🇧", "short": "EN", "name": "English"},
    "th": {"flag": "🇹🇭", "short": "TH", "name": "ไทย"},
}

DEFAULT = "en"

# `lang thai` is what people actually type, so accept the obvious spellings
# rather than making them guess the two-letter code.
ALIASES = {
    "en": "en", "eng": "en", "english": "en", "gb": "en", "us": "en",
    "อังกฤษ": "en",
    "th": "th", "tha": "th", "thai": "th", "ไทย": "th", "ภาษาไทย": "th",
}


def resolve_language(value):
    """Map user input to a language code, or None if unrecognised."""
    if not value:
        return None
    return ALIASES.get(value.strip().lower().lstrip("-"))


def accepted_languages():
    """Human-readable list of what `lang` accepts, for the error message."""
    return "en / english, th / thai"

MESSAGES = {
    "en": {
        # chrome
        "app.tagline": "42 exam practice",
        "bar.level": "L{level}",
        "ui.dashboard": "DASHBOARD",
        "ui.subject": "SUBJECT",
        "ui.hints": "HINTS",
        "ui.commands": "COMMANDS",
        "ui.curriculum": "CURRICULUM",
        "ui.exams": "EXAMS",
        "ui.history": "SESSION HISTORY",
        "ui.language": "Language",
        # tracks
        "track.exam": "exam {number}",
        "track.extra": "extra",
        "track.extra_note": "not in the 2026 exam pool, drill only",
        "track.added_note": (
            "not from the 2026 pool -- placed on this exam by difficulty, as extra "
            "practice"
        ),
        # dashboard fields
        "field.session": "Session",
        "field.exam": "Exam",
        "field.level": "Level",
        "field.completed": "Completed",
        "field.exercise": "Exercise",
        "field.type": "Type",
        "field.files": "Expected files",
        "field.workspace": "Workspace",
        "field.allowed": "Allowed",
        "field.prototype": "Prototype",
        "kind.program": "full program (with main)",
        "kind.function": "function only (no main)",
        "progress.session": "{count} this session",
        "progress.overall": "{done} of {total} overall",
        # subject / hints
        "subject.footer": "{track} · level {level}",
        "subject.switch": "`lang {other}` to switch language · also saved in subjects/",
        # grading
        "grade.running": "grading rendu/{name}/  ({files})",
        "grade.passed": "PASSED",
        "grade.not_yet": "NOT YET",
        "grade.byte_for_byte": "Every recorded test matched byte for byte.",
        "grade.ratio": "passed {passed}/{total}",
        "grade.test": "test {index}",
        "grade.expect": "expect",
        "grade.got": "got",
        "grade.nothing": "(nothing)",
        "grade.timed_out": "timed out -- {detail}",
        "grade.crashed": "crashed -- {detail}",
        "grade.stderr": "stderr: {text}",
        "grade.more_failures": "... and {count} more failing test(s)",
        "grade.look_at": "WHAT TO LOOK AT",
        "grade.compiler_output": "Compiler output",
        "grade.next_up": "next up: {name}  ·  run `subject`",
        "grade.substitution_note": (
            "the compiler emitted {names}; on the real exam this may count as a "
            "forbidden function"
        ),
        # evaluator results
        "result.unusable": (
            "Exercise `{name}` has no expected output recorded, so it cannot be graded."
        ),
        "result.missing_files": "Missing file(s): {files}",
        "result.no_c_file": "No .c file found among the expected files.",
        "result.has_main": (
            "{file} defines main(), but this exercise asks for a function only."
        ),
        "result.forbidden": "Forbidden function(s) used: {names}",
        "result.compile_failed": "Compilation failed.",
        "result.all_passed": "All {total} tests passed.",
        "result.some_failed": "{failed} of {total} tests failed.",
        # navigation
        "nav.skipped": "skipped {name}",
        "nav.now_on": "now on",
        "nav.level_note": "({track} · level {level})",
        "nav.subjects_updated": "subjects/ updated",
        "nav.nothing_left": "Skipped {name}. No exercises left.",
        "nav.reset_done": "Progress reset -- back to {track}, level 0.",
        "nav.starting_from": "starting from",
        "nav.archived": "archived",
        "nav.archived_to": "to",
        "nav.rendu_cleared": "rendu/ was cleared",
        "nav.rendu_kept": "your code in rendu/ was left untouched",
        "nav.nothing_to_archive": "Nothing to archive -- rendu/ is empty.",
        "nav.session_saved": "SESSION SAVED",
        "nav.skipped_title": "SKIPPED",
        "nav.reset_title": "RESET",
        "nav.no_sessions": "No archived sessions yet.",
        # list
        "list.level": "level {level}",
        "list.progress": "({done}/{total} done{locked})",
        "list.locked_suffix": ", locked",
        "list.tests": "{count} test",
        "list.tests_plural": "{count} tests",
        "list.legend_done": "done",
        "list.legend_current": "current",
        "list.legend_locked": "locked",
        "list.legend_added": "added, not from the 2026 pool",
        "list.col_session": "session",
        "list.col_archived": "archived",
        "list.col_level": "lvl",
        "list.col_done": "done",
        "list.all_hint": "`list all` for every exam · `exam` to switch",
        # exams
        "exam.row_level": "level {level}/{total}",
        "exam.row_done": "{done}/{total} done",
        "exam.current": "on {track}. `exam 02` switches, `exam extra` is drill.",
        "exam.unknown": "Unknown exam `{name}`. Accepted: {accepted}.",
        "exam.set": "now on {track}, level {level}",
        # examselect
        "select.hint": "`examselect <name>` jumps straight to one — `examselect fizz` works too",
        "select.jumped": "now on {name}  ·  {track} · level {level}",
        "select.unknown": "No exercise called `{name}`.",
        "select.did_you_mean": "No exercise called `{name}`. Did you mean: {suggestions}?",
        "select.ambiguous": "`{name}` matches {suggestions}. Be more specific.",
        # shell
        "shell.no_exercise": "No active exercise.",
        "shell.unknown_command": "Unknown command `{name}`. Type `help`.",
        "shell.help_hint": "`help` for commands · `subject` to start reading",
        "shell.lang_current": "language is `{lang}`. Use `lang en` or `lang th`.",
        "shell.lang_unknown": "Unknown language `{lang}`. Accepted: {accepted}.",
        "shell.lang_set": "language set to {flag} {name}",
        "shell.confirm_reset": "This erases all progress AND everything in rendu/. Continue?",
        "shell.cancelled": "cancelled",
        "shell.goodbye": "See you.",
        "shell.no_db": "No exercises found in engine/config/.",
        "shell.build_db": "Build it with: python3 engine/scripts/build_db.py",
        # updates
        "update.available": "update available: {latest} — you have {current}",
        "update.how": "git pull, then: python3 engine/scripts/build_db.py",
        "update.current": "up to date ({current})",
        "update.checking": "checking for updates...",
        "update.unknown": "could not reach the update source — {current} it is",
        # command descriptions
        "cmd.subject": "read the current assignment",
        "cmd.hint": "what to watch out for",
        "cmd.grademe": "compile and test what is in rendu/",
        "cmd.status": "session, level and current exercise",
        "cmd.list": "this exam's exercises and your progress",
        "cmd.exam": "pick an exam (01-04) or the extra drill track",
        "cmd.examselect": "list every exercise, or jump straight to one by name",
        "cmd.skip": "move to another exercise",
        "cmd.lang": "switch language (en / th)",
        "cmd.archive": "snapshot rendu/ into history/",
        "cmd.history": "past archived sessions",
        "cmd.reset": "wipe all progress and start over",
        "cmd.version": "show the version and check for updates",
        "cmd.exit": "archive and quit",
        # hint engine
        "hint.function_only": "Write the function only -- no main(). Prototype: {prototype}",
        "hint.signature_exact": (
            "The grader supplies a main() that calls your function, so the "
            "signature must match exactly."
        ),
        "hint.full_program": "Write a full program with int main(int argc, char **argv).",
        "hint.check_argc": (
            "Check argc before reading argv, and handle the wrong-argument case "
            "exactly as the subject describes."
        ),
        "hint.allowed": "Allowed functions: {names}",
        "hint.nothing_allowed": (
            "With nothing allowed you cannot even call write() -- everything must "
            "be pure computation on the arguments you were given."
        ),
        "hint.submit_all": "Submit every expected file: {files}",
        "hint.byte_compare": "Output is compared byte for byte, newline included.",
        "hint.check_malloc": "Check malloc's return before you write through it.",
        "hint.none": "none",
        "hint.compile.multiple_main": (
            "Your file defines main(), but the grader supplies its own. Remove yours."
        ),
        "hint.compile.undefined_ref": (
            "A function was declared but never defined -- check the spelling of "
            "your function name against the required prototype."
        ),
        "hint.compile.implicit": (
            "Missing #include, or a typo: unistd.h for write, stdlib.h for malloc, "
            "stdio.h for printf."
        ),
        "hint.compile.unused": (
            "-Werror rejects unused variables. Delete it, or silence a "
            "required-but-unused parameter with (void)name;"
        ),
        "hint.compile.conflicting": (
            "Your signature differs from the required prototype -- compare them "
            "character by character, including const and *."
        ),
        "hint.compile.syntax": "Look for a missing semicolon or an unclosed brace.",
        "hint.compile.no_return": "A code path is missing its return statement.",
        "hint.compile.read_first": (
            "Read the first error only -- the later ones are usually knock-on "
            "effects of it."
        ),
        "hint.run.segv_1": "Segmentation fault: you read or wrote memory you do not own.",
        "hint.run.segv_2": "Check for NULL before dereferencing, especially malloc's result.",
        "hint.run.segv_3": (
            "Check your indices -- walking one past the end of a string or array "
            "is the usual cause."
        ),
        "hint.run.abrt_1": "Abort: the allocator detected corruption.",
        "hint.run.abrt_2": (
            "Look for a double free, a free() of something never malloc'd, or a "
            "write past the end of an allocation."
        ),
        "hint.run.fpe": "Arithmetic error -- almost always a division or modulo by zero.",
        "hint.run.other": "The program ended abnormally ({detail}).",
        "hint.run.timeout": "A test never finished. Check your loop conditions and increments.",
        "hint.diff.empty": (
            "Your program printed nothing at all. Check that the code path you "
            "expect is actually reached."
        ),
        "hint.diff.missing_newline": (
            "The text is right but you are missing {count} trailing newline(s). "
            "Almost every subject ends with one."
        ),
        "hint.diff.extra_newline": (
            "The text is right but you printed {count} newline(s) too many at the end."
        ),
        "hint.diff.whitespace": (
            "The text matches once whitespace is ignored -- check leading and "
            "trailing spaces and newlines."
        ),
        "hint.diff.case": "Only the letter case differs.",
        "hint.diff.spacing": (
            "Only the spacing differs -- count the spaces in the subject's example."
        ),
        "hint.diff.compare": (
            "Compare the two outputs below character by character; the first "
            "difference is where your logic diverges."
        ),
    },
    "th": {
        "app.tagline": "ฝึกทำข้อสอบ 42",
        "bar.level": "ระดับ {level}",
        "ui.dashboard": "แดชบอร์ด",
        "ui.subject": "โจทย์",
        "ui.hints": "คำแนะนำ",
        "ui.commands": "คำสั่งทั้งหมด",
        "ui.curriculum": "รายการโจทย์",
        "ui.exams": "ชุดข้อสอบ",
        "ui.history": "ประวัติเซสชัน",
        "ui.language": "ภาษา",
        "track.exam": "ข้อสอบชุดที่ {number}",
        "track.extra": "แบบฝึกเสริม",
        "track.extra_note": "ไม่ได้อยู่ในชุดข้อสอบปี 2026 ใช้สำหรับฝึกซ้อมเท่านั้น",
        "track.added_note": (
            "ไม่ได้มาจากชุดข้อสอบปี 2026 แต่จัดไว้ในชุดนี้ตามระดับความยาก เพื่อเป็นแบบฝึกเพิ่มเติม"
        ),
        "field.session": "เซสชัน",
        "field.exam": "ชุดข้อสอบ",
        "field.level": "ระดับ",
        "field.completed": "ทำเสร็จแล้ว",
        "field.exercise": "โจทย์",
        "field.type": "ประเภท",
        "field.files": "ไฟล์ที่ต้องส่ง",
        "field.workspace": "โฟลเดอร์ทำงาน",
        "field.allowed": "ฟังก์ชันที่ใช้ได้",
        "field.prototype": "ต้นแบบฟังก์ชัน",
        "kind.program": "โปรแกรมเต็ม (มี main)",
        "kind.function": "ฟังก์ชันเท่านั้น (ไม่มี main)",
        "progress.session": "{count} ข้อในเซสชันนี้",
        "progress.overall": "{done} จาก {total} ข้อทั้งหมด",
        "subject.footer": "{track} · ระดับ {level}",
        "subject.switch": "พิมพ์ `lang {other}` เพื่อเปลี่ยนภาษา · บันทึกไว้ในโฟลเดอร์ subjects/ ด้วย",
        "grade.running": "กำลังตรวจ rendu/{name}/  ({files})",
        "grade.passed": "ผ่านแล้ว",
        "grade.not_yet": "ยังไม่ผ่าน",
        "grade.byte_for_byte": "ผลลัพธ์ตรงกันทุกไบต์ในทุกกรณีทดสอบ",
        "grade.ratio": "ผ่าน {passed}/{total}",
        "grade.test": "กรณีที่ {index}",
        "grade.expect": "ควรได้",
        "grade.got": "ได้จริง",
        "grade.nothing": "(ไม่มีผลลัพธ์)",
        "grade.timed_out": "ทำงานนานเกินกำหนด -- {detail}",
        "grade.crashed": "โปรแกรมล่ม -- {detail}",
        "grade.stderr": "ข้อความผิดพลาด: {text}",
        "grade.more_failures": "... และอีก {count} กรณีที่ไม่ผ่าน",
        "grade.look_at": "จุดที่ควรตรวจสอบ",
        "grade.compiler_output": "ข้อความจากคอมไพเลอร์",
        "grade.next_up": "ข้อต่อไป: {name}  ·  พิมพ์ `subject`",
        "grade.substitution_note": (
            "คอมไพเลอร์เรียกใช้ {names} ในข้อสอบจริงอาจถือว่าเป็นฟังก์ชันที่ห้ามใช้"
        ),
        "result.unusable": "โจทย์ `{name}` ไม่มีผลลัพธ์ที่คาดหวังบันทึกไว้ จึงตรวจไม่ได้",
        "result.missing_files": "ไม่พบไฟล์: {files}",
        "result.no_c_file": "ไม่พบไฟล์ .c ในรายการไฟล์ที่ต้องส่ง",
        "result.has_main": "{file} มีฟังก์ชัน main() แต่โจทย์ข้อนี้ต้องการเฉพาะฟังก์ชัน",
        "result.forbidden": "ใช้ฟังก์ชันที่ห้ามใช้: {names}",
        "result.compile_failed": "คอมไพล์ไม่ผ่าน",
        "result.all_passed": "ผ่านทั้งหมด {total} กรณีทดสอบ",
        "result.some_failed": "ไม่ผ่าน {failed} จาก {total} กรณีทดสอบ",
        "nav.skipped": "ข้ามข้อ {name}",
        "nav.now_on": "ข้อปัจจุบัน",
        "nav.level_note": "({track} · ระดับ {level})",
        "nav.subjects_updated": "อัปเดตโฟลเดอร์ subjects/ แล้ว",
        "nav.nothing_left": "ข้ามข้อ {name} แล้ว ไม่มีโจทย์เหลืออีก",
        "nav.reset_done": "รีเซ็ตความก้าวหน้าแล้ว กลับไปที่{track} ระดับ 0",
        "nav.starting_from": "เริ่มจากข้อ",
        "nav.archived": "บันทึกเซสชัน",
        "nav.archived_to": "ไปที่",
        "nav.rendu_cleared": "ล้างโฟลเดอร์ rendu/ แล้ว",
        "nav.rendu_kept": "โค้ดในโฟลเดอร์ rendu/ ยังอยู่ครบ",
        "nav.nothing_to_archive": "ไม่มีอะไรให้บันทึก -- โฟลเดอร์ rendu/ ว่างอยู่",
        "nav.session_saved": "บันทึกเซสชันแล้ว",
        "nav.skipped_title": "ข้ามข้อแล้ว",
        "nav.reset_title": "รีเซ็ต",
        "nav.no_sessions": "ยังไม่มีเซสชันที่บันทึกไว้",
        "list.level": "ระดับ {level}",
        "list.progress": "(ทำแล้ว {done}/{total}{locked})",
        "list.locked_suffix": ", ยังไม่ปลดล็อก",
        "list.tests": "{count} กรณี",
        "list.tests_plural": "{count} กรณี",
        "list.legend_done": "ทำแล้ว",
        "list.legend_current": "ข้อปัจจุบัน",
        "list.legend_locked": "ยังไม่ปลดล็อก",
        "list.legend_added": "เพิ่มเข้ามา ไม่ได้มาจากชุดข้อสอบปี 2026",
        "list.col_session": "เซสชัน",
        "list.col_archived": "บันทึกเมื่อ",
        "list.col_level": "ระดับ",
        "list.col_done": "ทำแล้ว",
        "list.all_hint": "พิมพ์ `list all` เพื่อดูทุกชุด · พิมพ์ `exam` เพื่อเปลี่ยนชุด",
        "exam.row_level": "ระดับ {level}/{total}",
        "exam.row_done": "ทำแล้ว {done}/{total}",
        "exam.current": "กำลังทำ{track} พิมพ์ `exam 02` เพื่อเปลี่ยนชุด หรือ `exam extra` สำหรับแบบฝึกเสริม",
        "exam.unknown": "ไม่รู้จักชุดข้อสอบ `{name}` ค่าที่ใช้ได้: {accepted}",
        "exam.set": "เปลี่ยนไปที่{track} ระดับ {level}",
        "select.hint": "พิมพ์ `examselect <ชื่อโจทย์>` เพื่อข้ามไปที่โจทย์นั้นทันที · พิมพ์แค่บางส่วนก็ได้ เช่น `examselect fizz`",
        "select.jumped": "ไปที่โจทย์ {name} แล้ว  ·  {track} · ระดับ {level}",
        "select.unknown": "ไม่มีโจทย์ชื่อ `{name}`",
        "select.did_you_mean": "ไม่มีโจทย์ชื่อ `{name}` หมายถึงข้อนี้หรือไม่: {suggestions}",
        "select.ambiguous": "`{name}` ตรงกับหลายข้อ: {suggestions} กรุณาระบุให้ชัดเจนขึ้น",
        "shell.no_exercise": "ไม่มีโจทย์ที่กำลังทำอยู่",
        "shell.unknown_command": "ไม่รู้จักคำสั่ง `{name}` พิมพ์ `help` เพื่อดูคำสั่งทั้งหมด",
        "shell.help_hint": "พิมพ์ `help` เพื่อดูคำสั่ง · พิมพ์ `subject` เพื่อเริ่มอ่านโจทย์",
        "shell.lang_current": "ภาษาปัจจุบันคือ `{lang}` ใช้ `lang en` หรือ `lang th`",
        "shell.lang_unknown": "ไม่รู้จักภาษา `{lang}` ค่าที่ใช้ได้: {accepted}",
        "shell.lang_set": "เปลี่ยนภาษาเป็น {flag} {name}",
        "shell.confirm_reset": "การทำเช่นนี้จะลบความก้าวหน้าทั้งหมดและทุกอย่างในโฟลเดอร์ rendu/ ต้องการทำต่อหรือไม่?",
        "shell.cancelled": "ยกเลิกแล้ว",
        "shell.goodbye": "เจอกันใหม่",
        "shell.no_db": "ไม่พบโจทย์ในโฟลเดอร์ engine/config/",
        "shell.build_db": "สร้างได้ด้วยคำสั่ง: python3 engine/scripts/build_db.py",
        "update.available": "มีเวอร์ชันใหม่: {latest} — ของคุณคือ {current}",
        "update.how": "รัน git pull แล้วตามด้วย: python3 engine/scripts/build_db.py",
        "update.current": "เป็นเวอร์ชันล่าสุดแล้ว ({current})",
        "update.checking": "กำลังตรวจหาเวอร์ชันใหม่...",
        "update.unknown": "ติดต่อแหล่งอัปเดตไม่ได้ ใช้เวอร์ชัน {current} ต่อไป",
        "cmd.subject": "อ่านโจทย์ข้อปัจจุบัน",
        "cmd.hint": "ดูจุดที่ต้องระวังในข้อนี้",
        "cmd.grademe": "คอมไพล์และทดสอบโค้ดในโฟลเดอร์ rendu/",
        "cmd.status": "ดูเซสชัน ระดับ และโจทย์ข้อปัจจุบัน",
        "cmd.list": "ดูรายการโจทย์ในชุดนี้และความก้าวหน้า",
        "cmd.exam": "เลือกชุดข้อสอบ (01-04) หรือแบบฝึกเสริม",
        "cmd.examselect": "ดูรายการโจทย์ทั้งหมด หรือข้ามไปที่โจทย์ที่ต้องการโดยระบุชื่อ",
        "cmd.skip": "ข้ามไปทำโจทย์ข้ออื่น",
        "cmd.lang": "เปลี่ยนภาษา (en / th)",
        "cmd.archive": "บันทึกโฟลเดอร์ rendu/ เก็บไว้ใน history/",
        "cmd.history": "ดูเซสชันที่บันทึกไว้ก่อนหน้า",
        "cmd.reset": "ลบความก้าวหน้าทั้งหมดและเริ่มใหม่",
        "cmd.version": "ดูเวอร์ชันและตรวจหาเวอร์ชันใหม่",
        "cmd.exit": "บันทึกแล้วออกจากโปรแกรม",
        "hint.function_only": "เขียนเฉพาะฟังก์ชัน ไม่ต้องมี main() ต้นแบบ: {prototype}",
        "hint.signature_exact": (
            "ตัวตรวจมี main() ของตัวเองที่จะเรียกฟังก์ชันของคุณ "
            "ดังนั้นรูปแบบฟังก์ชันต้องตรงกันทุกตัวอักษร"
        ),
        "hint.full_program": "เขียนโปรแกรมเต็มที่มี int main(int argc, char **argv)",
        "hint.check_argc": (
            "ตรวจ argc ก่อนอ่าน argv และจัดการกรณีอาร์กิวเมนต์ผิดให้ตรงตามที่โจทย์กำหนด"
        ),
        "hint.allowed": "ฟังก์ชันที่ใช้ได้: {names}",
        "hint.nothing_allowed": (
            "เมื่อไม่มีฟังก์ชันใดใช้ได้เลย แม้แต่ write() ก็เรียกไม่ได้ "
            "ทุกอย่างต้องคำนวณจากอาร์กิวเมนต์ที่ได้รับเท่านั้น"
        ),
        "hint.submit_all": "ต้องส่งไฟล์ให้ครบทุกไฟล์: {files}",
        "hint.byte_compare": "ผลลัพธ์ถูกเทียบทุกไบต์ รวมถึงการขึ้นบรรทัดใหม่",
        "hint.check_malloc": "ตรวจค่าที่ malloc คืนมาก่อนเขียนข้อมูลลงไป",
        "hint.none": "ไม่มี",
        "hint.compile.multiple_main": (
            "ไฟล์ของคุณมี main() แต่ตัวตรวจมี main() ของตัวเองอยู่แล้ว ให้ลบของคุณออก"
        ),
        "hint.compile.undefined_ref": (
            "มีการประกาศฟังก์ชันแต่ไม่มีการเขียนตัวฟังก์ชัน "
            "ให้ตรวจการสะกดชื่อฟังก์ชันเทียบกับต้นแบบที่โจทย์กำหนด"
        ),
        "hint.compile.implicit": (
            "ลืม #include หรือสะกดผิด: unistd.h สำหรับ write, stdlib.h สำหรับ malloc, "
            "stdio.h สำหรับ printf"
        ),
        "hint.compile.unused": (
            "-Werror ไม่ยอมให้มีตัวแปรที่ไม่ได้ใช้ ให้ลบออก "
            "หรือถ้าเป็นพารามิเตอร์ที่จำเป็นแต่ไม่ได้ใช้ ให้เขียน (void)ชื่อตัวแปร;"
        ),
        "hint.compile.conflicting": (
            "รูปแบบฟังก์ชันของคุณต่างจากต้นแบบที่กำหนด "
            "ให้เทียบทีละตัวอักษร รวมถึง const และ *"
        ),
        "hint.compile.syntax": "ตรวจหาเครื่องหมาย ; ที่ขาดไป หรือปีกกาที่ยังไม่ได้ปิด",
        "hint.compile.no_return": "มีเส้นทางการทำงานบางเส้นที่ไม่มีคำสั่ง return",
        "hint.compile.read_first": (
            "อ่านข้อผิดพลาดบรรทัดแรกก่อน บรรทัดถัด ๆ ไปมักเป็นผลพวงจากบรรทัดแรก"
        ),
        "hint.run.segv_1": "Segmentation fault: มีการอ่านหรือเขียนหน่วยความจำที่ไม่ได้เป็นของโปรแกรม",
        "hint.run.segv_2": "ตรวจ NULL ก่อนใช้พอยน์เตอร์ โดยเฉพาะค่าที่ malloc คืนมา",
        "hint.run.segv_3": (
            "ตรวจดัชนีของอาเรย์ สาเหตุที่พบบ่อยคือการเดินเลยท้ายข้อความหรือท้ายอาเรย์ไปหนึ่งตำแหน่ง"
        ),
        "hint.run.abrt_1": "Abort: ตัวจัดการหน่วยความจำตรวจพบความเสียหาย",
        "hint.run.abrt_2": (
            "ตรวจหาการ free ซ้ำสองครั้ง การ free สิ่งที่ไม่ได้มาจาก malloc "
            "หรือการเขียนข้อมูลเลยขอบเขตที่จองไว้"
        ),
        "hint.run.fpe": "ข้อผิดพลาดทางคณิตศาสตร์ เกือบทุกครั้งคือการหารหรือมอดุโลด้วยศูนย์",
        "hint.run.other": "โปรแกรมจบการทำงานผิดปกติ ({detail})",
        "hint.run.timeout": "มีกรณีทดสอบที่ทำงานไม่จบ ให้ตรวจเงื่อนไขและการเพิ่มค่าในลูป",
        "hint.diff.empty": (
            "โปรแกรมไม่แสดงผลลัพธ์อะไรเลย ให้ตรวจว่าเส้นทางการทำงานที่คาดไว้ถูกเรียกจริงหรือไม่"
        ),
        "hint.diff.missing_newline": (
            "ข้อความถูกต้องแล้ว แต่ขาดการขึ้นบรรทัดใหม่ท้ายสุดอยู่ {count} ครั้ง "
            "โจทย์เกือบทุกข้อจบด้วยการขึ้นบรรทัดใหม่"
        ),
        "hint.diff.extra_newline": (
            "ข้อความถูกต้องแล้ว แต่ขึ้นบรรทัดใหม่ท้ายสุดเกินมา {count} ครั้ง"
        ),
        "hint.diff.whitespace": (
            "ข้อความตรงกันถ้าไม่นับช่องว่าง ให้ตรวจช่องว่างนำหน้า ต่อท้าย และการขึ้นบรรทัดใหม่"
        ),
        "hint.diff.case": "ต่างกันแค่ตัวพิมพ์เล็กพิมพ์ใหญ่",
        "hint.diff.spacing": "ต่างกันแค่ช่องว่าง ให้นับจำนวนช่องว่างในตัวอย่างของโจทย์",
        "hint.diff.compare": (
            "เทียบผลลัพธ์สองบรรทัดข้างล่างทีละตัวอักษร "
            "จุดที่ต่างกันจุดแรกคือจุดที่ตรรกะเริ่มผิด"
        ),
    },
}


def t(lang, key, /, **kwargs):
    """Look up a message, falling back to English then to the key itself.

    `lang` and `key` are positional-only on purpose: message templates contain
    placeholders like {lang} and {count}, and a placeholder that happened to
    share a name with a parameter here would raise TypeError at the call site.
    That is not hypothetical -- `lang thai` crashed the shell exactly this way.
    """
    table = MESSAGES.get(lang, MESSAGES[DEFAULT])
    template = table.get(key) or MESSAGES[DEFAULT].get(key) or key
    if not kwargs:
        return template
    try:
        return template.format(**kwargs)
    except (KeyError, IndexError):
        return template


def validate_catalog():
    """Report catalog inconsistencies. Returns a list of problem descriptions.

    t() deliberately falls back rather than raising, so a translation that lost a
    {placeholder} would quietly print literal braces instead of a number. This is
    the check that catches it. engine/scripts/selftest.py runs it.
    """
    import re

    placeholders = re.compile(r"\{(\w+)\}")
    problems = []
    english = MESSAGES[DEFAULT]

    for lang, table in MESSAGES.items():
        if lang == DEFAULT:
            continue
        missing = sorted(set(english) - set(table))
        extra = sorted(set(table) - set(english))
        if missing:
            problems.append(f"{lang}: {len(missing)} untranslated key(s): {', '.join(missing)}")
        if extra:
            problems.append(f"{lang}: {len(extra)} key(s) not in {DEFAULT}: {', '.join(extra)}")

        for key in sorted(set(english) & set(table)):
            want = set(placeholders.findall(english[key]))
            got = set(placeholders.findall(table[key]))
            if want != got:
                problems.append(
                    f"{lang}: placeholders differ for {key!r}: "
                    f"{DEFAULT} has {sorted(want) or 'none'}, "
                    f"{lang} has {sorted(got) or 'none'}"
                )

    for code in LANGUAGES:
        if code not in MESSAGES:
            problems.append(f"{code} is offered in LANGUAGES but has no message table")
        if ALIASES.get(code) != code:
            problems.append(f"{code} is not an alias of itself")
    for alias, code in ALIASES.items():
        if code not in LANGUAGES:
            problems.append(f"alias {alias!r} maps to unknown language {code!r}")

    return problems


def flag(lang):
    return LANGUAGES.get(lang, LANGUAGES[DEFAULT])["flag"]


def language_badge(lang):
    """The indicator shown in the status bar, e.g. "🇹🇭 ไทย"."""
    entry = LANGUAGES.get(lang, LANGUAGES[DEFAULT])
    return f"{entry['flag']} {entry['name']}"


def other_language(lang):
    return "th" if lang == "en" else "en"


def track_name(lang, track):
    """"exam 02" / "extra", in the reader's language."""
    number = track_number(track)
    if number is None:
        return t(lang, "track.extra")
    return t(lang, "track.exam", number=number)
