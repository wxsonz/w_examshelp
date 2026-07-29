import os
import subprocess

class Compiler:
    def __init__(self, gcc_path="gcc"):
        self.gcc_path = gcc_path

    def compile(self, c_files, output_binary, extra_flags=None, include_dirs=None):
        """
        Compiles the given list of C files into output_binary using gcc.
        Returns (success: bool, error_message: str)
        """
        if extra_flags is None:
            extra_flags = ["-Wall", "-Wextra", "-Werror"]
            
        cmd = [self.gcc_path] + extra_flags + ["-o", output_binary] + c_files
        if include_dirs:
            for d in include_dirs:
                cmd.extend(["-I", d])

        try:
            res = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=15
            )
            if res.returncode != 0:
                return False, res.stderr.strip()
            return True, ""
        except subprocess.TimeoutExpired:
            return False, "Compilation timed out after 15 seconds."
        except Exception as e:
            return False, f"Compilation failed: {str(e)}"
