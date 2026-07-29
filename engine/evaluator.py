import os
import sys
import shutil
import tempfile
import subprocess
from engine.compiler import Compiler
from engine.hints import HintEngine

class Evaluator:
    def __init__(self, workspace_rendu="rendu"):
        self.workspace_rendu = workspace_rendu
        self.compiler = Compiler()

    def evaluate(self, exercise_info):
        """
        Runs complete non-punitive evaluation pipeline for an exercise.
        Returns dict with status, logs, test details, and friendly hints.
        """
        ex_name = exercise_info["name"]
        exp_files_str = exercise_info.get("expected_files", f"{ex_name}.c")
        expected_files = [f.strip() for f in exp_files_str.replace(',', ' ').split() if f.strip()]
        
        # 1. File existence check
        missing_files = []
        c_files_found = []
        for ef in expected_files:
            file_path = os.path.join(self.workspace_rendu, ef)
            if not os.path.exists(file_path):
                missing_files.append(ef)
            elif ef.endswith('.c'):
                c_files_found.append(file_path)
                
        if missing_files:
            return {
                "success": False,
                "stage": "file_check",
                "message": f"Missing expected file(s) in `{self.workspace_rendu}/`: {', '.join(missing_files)}",
                "hints": [
                    f"Please place your C source code file `{expected_files[0]}` inside the `{self.workspace_rendu}/` directory.",
                    f"Current directory path: `{os.path.abspath(self.workspace_rendu)}`"
                ]
            }

        # 2. Forbidden functions check (optional warning)
        allowed_fns = exercise_info.get("allowed_functions", "").lower()

        # Create temporary build dir
        with tempfile.TemporaryDirectory() as temp_dir:
            binary_path = os.path.join(temp_dir, "test_exec")
            
            is_func = exercise_info.get("is_function", False)
            proto = exercise_info.get("prototype")
            
            # 3. Compilation stage
            if is_func:
                # Generate wrapper main for function testing
                wrapper_c = self._generate_wrapper_c(exercise_info, temp_dir)
                compile_sources = c_files_found + [wrapper_c]
            else:
                compile_sources = c_files_found
                
            success, err_log = self.compiler.compile(compile_sources, binary_path)
            if not success:
                hints = HintEngine.get_compilation_hint(err_log)
                return {
                    "success": False,
                    "stage": "compilation",
                    "message": "Compilation Failed!",
                    "log": err_log,
                    "hints": hints
                }

            # 4. Test execution stage
            test_cases = exercise_info.get("test_cases", [])
            if not test_cases:
                # Default edge case test if no examples extracted
                test_cases = [
                    {"args": [], "expected_stdout": None},
                    {"args": ["test_input"], "expected_stdout": None}
                ]

            passed_count = 0
            total_count = len(test_cases)
            
            for idx, tc in enumerate(test_cases, 1):
                args = tc.get("args", [])
                expected_stdout = tc.get("expected_stdout")
                
                cmd = [binary_path] + [str(a) for a in args]
                try:
                    res = subprocess.run(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        timeout=5
                    )
                    
                    if res.returncode != 0:
                        hints = HintEngine.get_runtime_hint(res.returncode, res.stderr, exercise_info)
                        return {
                            "success": False,
                            "stage": "runtime",
                            "test_number": idx,
                            "args": args,
                            "returncode": res.returncode,
                            "message": f"Runtime error on Test #{idx} (Signal / Code {res.returncode})",
                            "stderr": res.stderr,
                            "hints": hints + exercise_info.get("hints", [])
                        }
                        
                    if expected_stdout is not None:
                        actual_stdout = res.stdout
                        if actual_stdout != expected_stdout:
                            hints = HintEngine.get_mismatch_hint(actual_stdout, expected_stdout, tc)
                            return {
                                "success": False,
                                "stage": "output_mismatch",
                                "test_number": idx,
                                "args": args,
                                "expected": expected_stdout,
                                "got": actual_stdout,
                                "message": f"Output mismatch on Test #{idx}",
                                "hints": hints + exercise_info.get("hints", [])
                            }
                            
                    passed_count += 1

                except subprocess.TimeoutExpired:
                    return {
                        "success": False,
                        "stage": "timeout",
                        "test_number": idx,
                        "args": args,
                        "message": f"Test #{idx} timed out (> 5s infinite loop detected).",
                        "hints": ["Check your loop exit conditions and array bounds!"]
                    }

            return {
                "success": True,
                "stage": "passed",
                "message": f"All {passed_count}/{total_count} tests passed successfully! 🎉",
                "passed_tests": passed_count
            }

    def _generate_wrapper_c(self, exercise_info, temp_dir):
        ex_name = exercise_info["name"]
        proto = exercise_info.get("prototype", "")
        
        wrapper_path = os.path.join(temp_dir, "wrapper_main.c")
        
        # Build headers
        code = "#include <stdio.h>\n#include <stdlib.h>\n#include <string.h>\n#include <unistd.h>\n\n"
        
        # Add prototype
        if proto:
            code += f"// Function prototype under test\n{proto}\n\n"
        else:
            code += f"// Generic declaration\nextern void {ex_name}();\n\n"

        # Generate generic test runner main
        code += "int main(int argc, char **argv) {\n"
        code += "    (void)argc;\n    (void)argv;\n"
        
        if ex_name == "ft_countdown":
            code += "    ft_countdown();\n"
        elif ex_name == "ft_print_numbers":
            code += "    ft_print_numbers();\n"
        elif ex_name == "ft_strlen":
            code += "    if (argc > 1) printf(\"%d\\n\", ft_strlen(argv[1]));\n"
        elif ex_name == "ft_strcpy":
            code += "    if (argc > 2) {\n"
            code += "        char buf[1024] = {0};\n"
            code += "        ft_strcpy(buf, argv[2]);\n"
            code += "        printf(\"%s\\n\", buf);\n"
            code += "    }\n"
        elif ex_name == "count_of_2":
            code += "    if (argc > 1) printf(\"%d\\n\", count_of_2(atoi(argv[1])));\n"
        elif ex_name == "ft_atoi":
            code += "    if (argc > 1) printf(\"%d\\n\", ft_atoi(argv[1]));\n"
        elif ex_name == "is_power_of_2":
            code += "    if (argc > 1) printf(\"%d\\n\", is_power_of_2(atoi(argv[1])));\n"
        else:
            # Fallback wrapper caller
            code += "    // Fallback execution\n"
            code += "    return 0;\n"

        code += "    return 0;\n}\n"

        with open(wrapper_path, "w") as f:
            f.write(code)
            
        return wrapper_path
