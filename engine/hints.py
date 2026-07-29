class HintEngine:
    @staticmethod
    def get_exercise_hints(exercise_info):
        """
        Generates detailed advice on what to look out for in the current question.
        """
        if not exercise_info:
            return ["No active exercise selected."]
            
        hints = []
        name = exercise_info["name"]
        is_func = exercise_info.get("is_function", False)
        proto = exercise_info.get("prototype")
        allowed_fns = exercise_info.get("allowed_functions", "write")
        content = exercise_info.get("subject", "").lower()

        # 1. Structure & Interface Checklist
        if is_func:
            if proto:
                hints.append(f"Function Prototype: `{proto}`")
                hints.append("Match exact parameter types and return type. Do NOT include a `main()` function in your submitted file!")
            else:
                hints.append(f"Function Exercise: Ensure your function `{name}` matches required signature.")
        else:
            hints.append("Program Exercise: Must include a standard `int main(int argc, char **argv)` function.")
            hints.append("CLI Arguments: Check `argc`! If argc != expected count, handle it gracefully (e.g. write a newline `\\n` or return 0).")

        # 2. Allowed Functions & Constraints
        hints.append(f"Allowed Functions: `{allowed_fns}`. Do not use unallowed standard library functions.")

        # 3. Edge Cases & Specific Mechanics
        if "string" in content or "char *" in content or "s1" in content or "str" in content:
            hints.append("String Mechanics: Always check for `NULL` pointers before reading. Watch out for missing `\\0` null terminators.")
        if "malloc" in content or "allowed functions: malloc" in content or "ft_split" in name or "strdup" in name:
            hints.append("Memory Safety: Always check if `malloc()` returned `NULL` before dereferencing allocated memory.")
        if "bit" in name or "bits" in content or "octet" in content:
            hints.append("Bitwise Operations: Use bitwise operators (`&`, `|`, `^`, `<<`, `>>`). Remember 1 byte = 8 bits (`0xFF`).")
        if "list" in name or "t_list" in content or "node" in content:
            hints.append("Linked Lists: Always check if `head` or `*begin_list` is `NULL`. Be careful when updating `next` pointers.")
        if "tree" in name or "bst" in content:
            hints.append("Binary Search Trees: Use recursion or stack for tree traversal. Check for `NULL` child nodes (`left`, `right`).")
        if "number" in content or "digit" in content or "int" in content or "atoi" in name or "itoa" in name:
            hints.append("Numeric Edge Cases: Handle 0, negative numbers (`INT_MIN = -2147483648`), and potential integer overflows.")

        # 4. Output Formatting Rules
        if not is_func:
            hints.append("Output Formatting: Make sure lines end with `\\n` exactly as shown in example outputs.")

        # Include custom hints stored in exercise_info if present
        custom_hints = exercise_info.get("hints", [])
        for ch in custom_hints:
            if ch not in hints and not ch.startswith("Ensure your function") and not ch.startswith("Check argc!"):
                hints.append(ch)

        return hints

    @staticmethod
    def get_compilation_hint(error_log):
        log_lower = error_log.lower()
        hints = []
        
        if "undeclared" in log_lower or "implicit declaration" in log_lower:
            hints.append("Check header inclusions (`#include <unistd.h>`, `#include <stdlib.h>`, `#include <stdio.h>`) or prototype declarations.")
        if "expected ';'" in log_lower or "expected '}'" in log_lower:
            hints.append("Look out for missing semicolons `;` or unclosed curly braces `}`.")
        if "type" in log_lower or "incompatible" in log_lower:
            hints.append("Type mismatch detected. Verify function arguments and return types.")
        if "unused variable" in log_lower or "unused parameter" in log_lower:
            hints.append("Unused variables trigger `-Werror`. Cast unused parameters with `(void)param;` or remove unused variables.")
            
        if not hints:
            hints.append("Read compiler log carefully to locate line numbers and syntax issues.")
            
        return hints

    @staticmethod
    def get_runtime_hint(returncode, stderr, exercise_info):
        hints = []
        
        if returncode in [-11, 139] or "segmentation fault" in stderr.lower():
            hints.append("CRITICAL: Segmentation Fault detected!")
            hints.append("1. Are you checking if pointers (e.g., `str`, `s1`, `s2`, or `malloc` output) are `NULL` before accessing?")
            hints.append("2. Are you reading or writing array indices beyond allocated memory bounds?")
            hints.append("3. Make sure string loops terminate at `\\0`.")
            return hints
            
        if returncode in [-6, 134]:
            hints.append("Abort signal received! Indicates double-free or memory corruption.")
            return hints

        if returncode == 124:
            hints.append("Time Limit Exceeded (>5s infinite loop)! Check loop conditions and increments.")
            return hints

        return hints

    @staticmethod
    def get_mismatch_hint(actual_stdout, expected_stdout, test_case):
        hints = []
        
        if not actual_stdout and expected_stdout:
            hints.append("Your program produced NO output when output was expected. Verify logic execution path.")
        elif actual_stdout.strip() == expected_stdout.strip() and actual_stdout != expected_stdout:
            hints.append("Whitespace / Newline Mismatch! Text matches, but check trailing spaces or missing `\\n`.")
        elif actual_stdout.lower() == expected_stdout.lower() and actual_stdout != expected_stdout:
            hints.append("Letter Case Mismatch! Check uppercase vs lowercase requirements.")
        else:
            hints.append(f"Output mismatch.\n  Expected: {repr(expected_stdout)}\n  Got:      {repr(actual_stdout)}")
            
        return hints
