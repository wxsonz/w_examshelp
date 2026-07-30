"""Advice attached to failures and to the `hint` command.

get_exercise_hints() used to exist here and never be called -- `hint` printed the
one-line filler stored in the database instead. It is now the source of the
`hint` command's output, combined with the per-exercise hints from the pack.

The generic advice below is translated. The per-exercise hints written in
engine/exercises/ are English only, so a Thai session shows Thai advice followed
by English exercise-specific notes.
"""

from engine.i18n import t


class HintEngine:
    @staticmethod
    def get_exercise_hints(exercise, lang="en"):
        """What to watch out for on the current exercise."""
        if not exercise:
            return [t(lang, "shell.no_exercise")]

        hints = []
        name = exercise["name"]
        is_function = exercise.get("kind", "program") == "function"
        allowed = exercise.get("allowed_functions") or []
        if isinstance(allowed, str):
            allowed = [a.strip() for a in allowed.split(",") if a.strip()]

        if is_function:
            hints.append(t(lang, "hint.function_only", prototype=exercise["prototype"]))
            hints.append(t(lang, "hint.signature_exact"))
        else:
            hints.append(t(lang, "hint.full_program"))
            hints.append(t(lang, "hint.check_argc"))

        hints.append(
            t(lang, "hint.allowed",
              names=", ".join(allowed) if allowed else t(lang, "hint.none"))
        )
        if not allowed:
            hints.append(t(lang, "hint.nothing_allowed"))

        files = exercise.get("expected_files") or []
        if isinstance(files, str):
            files = [f.strip() for f in files.split(",") if f.strip()]
        if len(files) > 1:
            hints.append(t(lang, "hint.submit_all", files=", ".join(files)))

        # Exercise-specific advice written in the pack, which is the good stuff.
        for hint in exercise.get("hints", []):
            if hint not in hints:
                hints.append(hint)

        hints.append(t(lang, "hint.byte_compare"))
        if name.startswith("ft_") and "malloc" in allowed:
            hints.append(t(lang, "hint.check_malloc"))
        return hints

    @staticmethod
    def get_compilation_hint(log, lang="en"):
        lowered = log.lower()
        keys = []

        if "multiple definition of" in lowered and "main" in lowered:
            keys.append("hint.compile.multiple_main")
        if "undefined reference to" in lowered:
            keys.append("hint.compile.undefined_ref")
        if "implicit declaration" in lowered or "undeclared" in lowered:
            keys.append("hint.compile.implicit")
        if "unused variable" in lowered or "unused parameter" in lowered:
            keys.append("hint.compile.unused")
        if "conflicting types" in lowered or "incompatible" in lowered:
            keys.append("hint.compile.conflicting")
        if "expected ';'" in lowered or "expected '}'" in lowered:
            keys.append("hint.compile.syntax")
        if "control reaches end of non-void function" in lowered:
            keys.append("hint.compile.no_return")

        if not keys:
            keys.append("hint.compile.read_first")
        return [t(lang, key) for key in keys]

    @staticmethod
    def get_runtime_hint(detail, lang="en"):
        lowered = (detail or "").lower()

        if "sigsegv" in lowered:
            keys = ["hint.run.segv_1", "hint.run.segv_2", "hint.run.segv_3"]
        elif "sigabrt" in lowered:
            keys = ["hint.run.abrt_1", "hint.run.abrt_2"]
        elif "sigfpe" in lowered:
            keys = ["hint.run.fpe"]
        else:
            return [t(lang, "hint.run.other", detail=detail)]
        return [t(lang, key) for key in keys]

    @staticmethod
    def get_mismatch_hint(got, expected, lang="en"):
        if got == "":
            return [t(lang, "hint.diff.empty")]

        if got.rstrip("\n") == expected.rstrip("\n"):
            missing = expected.count("\n") - got.count("\n")
            if missing > 0:
                return [t(lang, "hint.diff.missing_newline", count=missing)]
            return [t(lang, "hint.diff.extra_newline", count=-missing)]

        if got.strip() == expected.strip():
            return [t(lang, "hint.diff.whitespace")]
        if got.lower() == expected.lower():
            return [t(lang, "hint.diff.case")]
        if got.replace(" ", "") == expected.replace(" ", ""):
            return [t(lang, "hint.diff.spacing")]
        return [t(lang, "hint.diff.compare")]
