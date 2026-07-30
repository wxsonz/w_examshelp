import os
import re
import subprocess

CFLAGS = ["-Wall", "-Wextra", "-Werror"]
COMPILE_TIMEOUT = 30

# Libc functions the exam commonly bans. Only these are reported, so an
# unfamiliar symbol emitted by the compiler itself can never fail a submission.
WATCHED_FUNCTIONS = {
    "printf", "fprintf", "sprintf", "snprintf", "vprintf", "dprintf",
    "puts", "putchar", "fputs", "fputc", "putc",
    "scanf", "fscanf", "sscanf", "gets", "fgets", "getchar",
    "read", "write", "open", "close", "lseek",
    "malloc", "calloc", "realloc", "free",
    "strlen", "strcpy", "strncpy", "strcat", "strncat", "strcmp", "strncmp",
    "strchr", "strrchr", "strstr", "strnstr", "strdup", "strndup",
    "strlcpy", "strlcat", "strspn", "strcspn", "strpbrk", "strtok",
    "atoi", "atol", "atoll", "strtol", "strtoul", "abs", "labs",
    "qsort", "bsearch", "exit", "abort",
    "toupper", "tolower", "isalpha", "isdigit", "isalnum", "isspace",
    "isprint", "isupper", "islower",
    "memchr", "memcmp",
}

# The compiler may emit these on its own (aggregate copies, struct init), so a
# match is reported as advice rather than treated as a violation.
ADVISORY_FUNCTIONS = {"memcpy", "memset", "memmove", "bzero"}

# gcc rewrites calls to cheaper equivalents even at -O0: printf("\n") becomes
# putchar, and printf("some literal\n") becomes puts. The symbol table therefore
# names functions the source never mentioned, so allowing one has to allow the
# substitutions the compiler may pick for it.
COMPILER_SUBSTITUTIONS = {
    "printf": {"puts", "putchar", "fputs", "fputc", "putc", "fwrite"},
    "fprintf": {"fputs", "fputc", "putc", "fwrite"},
}


class Compiler:
    def __init__(self, gcc_path="gcc"):
        self.gcc_path = gcc_path

    def compile(self, c_files, output_binary, include_dirs=None, extra_flags=None):
        """Link c_files into output_binary. Returns (ok, stderr).

        include_dirs matters: the ft_list_* exercises are graded against a
        harness that does `#include "ft_list.h"`, and that header is written by
        the student, so their directory has to be on the include path.
        """
        cmd = [self.gcc_path] + (extra_flags if extra_flags is not None else CFLAGS)
        for directory in include_dirs or []:
            cmd += ["-I", directory]
        cmd += ["-o", output_binary] + list(c_files)
        return self._run(cmd)

    def compile_object(self, c_file, output_object, include_dirs=None):
        """Compile a single translation unit to an object file, without linking."""
        cmd = [self.gcc_path] + CFLAGS
        for directory in include_dirs or []:
            cmd += ["-I", directory]
        cmd += ["-c", c_file, "-o", output_object]
        return self._run(cmd)

    def _run(self, cmd):
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=COMPILE_TIMEOUT
            )
        except subprocess.TimeoutExpired:
            return False, f"Compilation timed out after {COMPILE_TIMEOUT} seconds."
        except OSError as err:
            return False, f"Could not run {self.gcc_path}: {err}"
        if result.returncode != 0:
            return False, result.stderr.strip()
        return True, result.stderr.strip()

    def undefined_symbols(self, object_path):
        """External functions an object file calls, via `nm -u`."""
        try:
            result = subprocess.run(
                ["nm", "-u", object_path], capture_output=True, text=True, timeout=15
            )
        except (subprocess.TimeoutExpired, OSError):
            return None  # nm unavailable: skip the check rather than guess.
        if result.returncode != 0:
            return None

        symbols = set()
        for line in result.stdout.splitlines():
            parts = line.split()
            if not parts:
                continue
            name = parts[-1]
            # Strip the versioning suffix glibc adds, e.g. printf@@GLIBC_2.2.5
            name = name.split("@")[0]
            # glibc redirects some calls; __isoc99_scanf is really scanf.
            name = re.sub(r"^__isoc99_", "", name)
            if name.startswith("_") or name in ("main",):
                continue
            symbols.add(name)
        return symbols


def check_allowed_functions(symbols, allowed):
    """Split the symbols a submission calls into violations and advisories.

    `allowed` is the exercise's allowed-functions list. Returns
    (violations, advisories), both sorted lists of names.
    """
    if symbols is None:
        return [], []

    permitted = {a.strip().lower() for a in allowed if a and a.strip()}
    permitted.discard("none")
    for name, substitutes in COMPILER_SUBSTITUTIONS.items():
        if name in permitted:
            permitted |= substitutes

    violations = sorted(
        name
        for name in symbols
        if name in WATCHED_FUNCTIONS and name.lower() not in permitted
    )
    advisories = sorted(
        name
        for name in symbols
        if name in ADVISORY_FUNCTIONS and name.lower() not in permitted
    )
    return violations, advisories


_BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.S)
_LINE_COMMENT = re.compile(r"//[^\n]*")
_STRING_LITERAL = re.compile(r'"(?:\\.|[^"\\])*"')
_CHAR_LITERAL = re.compile(r"'(?:\\.|[^'\\])*'")
_MAIN_DEFINITION = re.compile(r"\bmain\s*\(")


def defines_main(source):
    """True if the source appears to define main(), ignoring comments and strings."""
    stripped = _BLOCK_COMMENT.sub(" ", source)
    stripped = _LINE_COMMENT.sub(" ", stripped)
    stripped = _STRING_LITERAL.sub('""', stripped)
    stripped = _CHAR_LITERAL.sub("''", stripped)
    return bool(_MAIN_DEFINITION.search(stripped))
