import os
import shutil
import signal
import subprocess
import tempfile

from engine.compiler import (
    Compiler,
    check_allowed_functions,
    defines_main,
)
from engine.hints import HintEngine
from engine.i18n import t

RUN_TIMEOUT = 5

_SIGNAL_NAMES = {
    signal.SIGSEGV: "SIGSEGV (segmentation fault)",
    signal.SIGABRT: "SIGABRT (abort -- often a double free or heap corruption)",
    signal.SIGFPE: "SIGFPE (arithmetic error -- often division by zero)",
    signal.SIGBUS: "SIGBUS (bad memory access)",
    signal.SIGILL: "SIGILL (illegal instruction)",
}


class Evaluator:
    """Compiles a submission and runs it against the exercise's recorded tests.

    Every exercise in the pack ships expected output generated from a verified
    reference solution, so grading is a byte comparison. If an exercise somehow
    reaches here without assertable output, grading REFUSES rather than passing
    it -- the previous engine defaulted to `expected_stdout: None` and handed out
    "All tests passed" to an empty main().
    """

    def __init__(self, workspace_rendu="rendu", lang="en"):
        self.workspace_rendu = workspace_rendu
        self.lang = lang
        self.compiler = Compiler()

    def _fail(self, stage, key, args=None, **extra):
        """Build a result whose message the UI can re-render in any language."""
        args = args or {}
        result = {
            "ok": False,
            "stage": stage,
            "msg_key": key,
            "msg_args": args,
            "message": t(self.lang, key, **args),
        }
        result.update(extra)
        return result

    def evaluate(self, exercise):
        submission_dir = os.path.join(self.workspace_rendu, exercise["name"])
        expected_files = exercise["expected_files"]
        if isinstance(expected_files, str):  # tolerate the pre-rebuild format
            expected_files = [f.strip() for f in expected_files.split(",") if f.strip()]

        tests = exercise.get("tests") or []
        assertable = [
            test for test in tests if test.get("expected_stdout") is not None
        ]
        if not assertable:
            return self._fail(
                "unusable",
                "result.unusable",
                {"name": exercise["name"]},
                hints=[
                    "This is a bug in the exercise pack, not in your code.",
                    "Regenerate the database with: python3 engine/scripts/build_db.py",
                ],
            )

        missing = [
            name
            for name in expected_files
            if not os.path.isfile(os.path.join(submission_dir, name))
        ]
        if missing:
            return self._fail(
                "files",
                "result.missing_files",
                {"files": ", ".join(missing)},
                hints=[
                    f"Put your code in {os.path.abspath(submission_dir)}/",
                    f"This exercise expects: {', '.join(expected_files)}",
                ],
            )

        with tempfile.TemporaryDirectory() as work_dir:
            return self._grade(exercise, submission_dir, expected_files, assertable, work_dir)

    # ------------------------------------------------------------------ stages

    def _grade(self, exercise, submission_dir, expected_files, tests, work_dir):
        build_dir = os.path.join(work_dir, "build")
        os.makedirs(build_dir)

        student_c_files = []
        for name in expected_files:
            destination = os.path.join(build_dir, os.path.basename(name))
            shutil.copyfile(os.path.join(submission_dir, name), destination)
            if name.endswith(".c"):
                student_c_files.append(destination)

        if not student_c_files:
            return self._fail(
                "files",
                "result.no_c_file",
                hints=["At least one C source file is required."],
            )

        is_function = exercise.get("kind", "program") == "function"

        # A function exercise is graded against our own main(), so a main() in
        # the submission would collide at link time. Say so plainly.
        if is_function:
            for path in student_c_files:
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    if defines_main(f.read()):
                        return self._fail(
                            "structure",
                            "result.has_main",
                            {"file": os.path.basename(path)},
                            hints=[
                                t(self.lang, "hint.compile.multiple_main"),
                                t(self.lang, "hint.function_only",
                                  prototype=exercise["prototype"]),
                            ],
                        )

        forbidden, advisory = self._check_functions(
            exercise, student_c_files, build_dir, work_dir
        )
        if forbidden:
            allowed_names = ", ".join(exercise["allowed_functions"]) or t(
                self.lang, "hint.none"
            )
            return self._fail(
                "forbidden",
                "result.forbidden",
                {"names": ", ".join(forbidden)},
                hints=[t(self.lang, "hint.allowed", names=allowed_names)],
            )

        sources = list(student_c_files)
        if exercise.get("harness"):
            harness_path = os.path.join(build_dir, "__examshelp_main.c")
            with open(harness_path, "w", encoding="utf-8") as f:
                f.write(exercise["harness"])
            sources.append(harness_path)

        binary = os.path.join(work_dir, "submission")
        ok, log = self.compiler.compile(sources, binary, include_dirs=[build_dir])
        if not ok:
            return self._fail(
                "compile",
                "result.compile_failed",
                compiler_log=self._tidy_log(log, build_dir),
                hints=HintEngine.get_compilation_hint(log, self.lang),
                advisory=advisory,
            )

        results = [self._run_one(binary, test, i) for i, test in enumerate(tests, 1)]
        passed = sum(1 for r in results if r["status"] == "pass")

        if passed == len(results):
            return {
                "ok": True,
                "stage": "passed",
                "msg_key": "result.all_passed",
                "msg_args": {"total": passed},
                "message": t(self.lang, "result.all_passed", total=passed),
                "results": results,
                "passed": passed,
                "total": len(results),
                "advisory": advisory,
                "compiler_log": self._tidy_log(log, build_dir),
            }

        failed = [r for r in results if r["status"] != "pass"]
        return self._fail(
            "tests",
            "result.some_failed",
            {"failed": len(failed), "total": len(results)},
            results=results,
            passed=passed,
            total=len(results),
            hints=self._failure_hints(failed, exercise),
            advisory=advisory,
        )

    def _check_functions(self, exercise, student_c_files, build_dir, work_dir):
        """Inspect only the student's own objects, never the harness."""
        allowed = exercise.get("allowed_functions") or []
        if isinstance(allowed, str):
            allowed = [a.strip() for a in allowed.split(",")]

        symbols = set()
        for index, path in enumerate(student_c_files):
            object_path = os.path.join(work_dir, f"student{index}.o")
            ok, _ = self.compiler.compile_object(
                path, object_path, include_dirs=[build_dir]
            )
            if not ok:
                return [], []  # let the real compile stage report the error
            found = self.compiler.undefined_symbols(object_path)
            if found is None:
                return [], []
            symbols |= found

        return check_allowed_functions(symbols, allowed)

    def _run_one(self, binary, test, index):
        record = {
            "index": index,
            "argv": test.get("argv", []),
            "stdin": test.get("stdin", ""),
            "note": test.get("note", ""),
            "expected": test["expected_stdout"],
        }
        try:
            proc = subprocess.run(
                [binary] + [str(a) for a in record["argv"]],
                input=record["stdin"],
                capture_output=True,
                text=True,
                timeout=RUN_TIMEOUT,
            )
        except subprocess.TimeoutExpired:
            record.update(
                status="timeout",
                got="",
                stderr="",
                detail=f"still running after {RUN_TIMEOUT}s",
            )
            return record

        record["got"] = proc.stdout
        record["stderr"] = proc.stderr.strip()

        if proc.returncode < 0:
            crash = -proc.returncode
            record.update(
                status="crash",
                detail=_SIGNAL_NAMES.get(crash, f"killed by signal {crash}"),
            )
            return record

        if proc.returncode != 0:
            record.update(
                status="crash", detail=f"exited with status {proc.returncode}"
            )
            return record

        record["status"] = "pass" if proc.stdout == record["expected"] else "fail"
        return record

    def _failure_hints(self, failed, exercise):
        hints = []
        first = failed[0]
        if first["status"] == "timeout":
            hints.append(t(self.lang, "hint.run.timeout"))
        elif first["status"] == "crash":
            hints.extend(HintEngine.get_runtime_hint(first["detail"], self.lang))
        else:
            hints.extend(
                HintEngine.get_mismatch_hint(
                    first["got"], first["expected"], self.lang
                )
            )
        for hint in exercise.get("hints", []):
            if hint not in hints:
                hints.append(hint)
        return hints

    @staticmethod
    def _tidy_log(log, build_dir):
        """Strip the temporary build path so errors read as plain filenames."""
        if not log:
            return ""
        return log.replace(build_dir + os.sep, "").replace(build_dir, "")
