import os
import json
import re

from build_db import get_official_42_exercises, get_extended_custom_exercises, map_to_10_levels

def generate_function_wrapper(proto, name):
    if not proto:
        return ""
    
    match = re.match(r'^(.*?)\s+([a-zA-Z0-9_]+)\((.*)\);?$', proto.strip())
    if not match:
        return ""
        
    ret_type = match.group(1).strip()
    func_name = match.group(2).strip()
    args_str = match.group(3).strip()
    
    headers = "#include <stdio.h>\n#include <stdlib.h>\n#include <string.h>\n#include <unistd.h>\n\n"
    
    main_body = f"// Prototype\n{proto}\n\nint main(int argc, char **argv) {{\n"
    main_body += "    if (argc == 1) return 0;\n"
    
    if "(*f)" in args_str or "**" in args_str or "struct" in args_str or "t_list" in args_str or "t_node" in args_str:
        main_body += "    printf(\"Complex struct test placeholder\\n\");\n"
        main_body += "    return 0;\n}\n"
        return headers + main_body

    args = [a.strip() for a in args_str.split(',') if a.strip() and a.strip() != 'void']
    
    call_args = []
    for i, arg in enumerate(args):
        arg_idx = i + 1
        if "char *" in arg or "char const *" in arg or "const char *" in arg:
            call_args.append(f"argv[{arg_idx}]")
            main_body += f"    if (argc <= {arg_idx}) return 0;\n"
        elif "int" in arg or "size_t" in arg or "unsigned int" in arg:
            call_args.append(f"atoi(argv[{arg_idx}])")
            main_body += f"    if (argc <= {arg_idx}) return 0;\n"
        elif "char" in arg and "*" not in arg:
            call_args.append(f"argv[{arg_idx}][0]")
            main_body += f"    if (argc <= {arg_idx}) return 0;\n"
        else:
            call_args.append("0")
            
    call_str = f"{func_name}({', '.join(call_args)})"
    
    if ret_type == "void":
        main_body += f"    {call_str};\n"
        main_body += "    printf(\"void\\n\");\n"
    elif "char *" in ret_type:
        main_body += f"    char *res = {call_str};\n"
        main_body += "    if (res) printf(\"%s\\n\", res);\n"
        main_body += "    else printf(\"NULL\\n\");\n"
    elif ret_type == "int" or ret_type == "long" or ret_type == "size_t":
        main_body += f"    printf(\"%ld\\n\", (long){call_str});\n"
    else:
        main_body += f"    {call_str};\n"
        
    main_body += "    return 0;\n}\n"
    return headers + main_body

def inject_official_testcases(ex):
    name = ex["name"]
    
    if name == "ft_print_numbers":
        ex["main_code"] = "#include <unistd.h>\nvoid ft_print_numbers(void);\nint main(void) { ft_print_numbers(); return 0; }\n"
        ex["test_cases"] = [{"args": [], "expected_stdout": "0123456789"}]
    
    elif name == "ft_strcpy":
        ex["main_code"] = "#include <stdio.h>\nchar *ft_strcpy(char *s1, char *s2);\nint main(int argc, char **argv) {\n if (argc>1) { char buf[1024]={0}; ft_strcpy(buf, argv[1]); printf(\"%s\\n\", buf); }\n return 0;\n}\n"
        ex["test_cases"] = [
            {"args": ["hello"], "expected_stdout": "hello\n"},
            {"args": ["world!"], "expected_stdout": "world!\n"},
            {"args": [""], "expected_stdout": "\n"}
        ]
        
    elif name == "ft_strlen":
        ex["main_code"] = "#include <stdio.h>\nint ft_strlen(char *str);\nint main(int argc, char **argv) {\n if (argc>1) { printf(\"%d\\n\", ft_strlen(argv[1])); }\n return 0;\n}\n"
        ex["test_cases"] = [
            {"args": ["hello"], "expected_stdout": "5\n"},
            {"args": ["world!"], "expected_stdout": "6\n"},
            {"args": [""], "expected_stdout": "0\n"}
        ]
        
    elif name == "ft_atoi":
        ex["main_code"] = "#include <stdio.h>\nint ft_atoi(const char *str);\nint main(int argc, char **argv) {\n if (argc>1) { printf(\"%d\\n\", ft_atoi(argv[1])); }\n return 0;\n}\n"
        ex["test_cases"] = [
            {"args": ["42"], "expected_stdout": "42\n"},
            {"args": ["-42"], "expected_stdout": "-42\n"},
            {"args": ["   +42"], "expected_stdout": "42\n"},
            {"args": ["  -0042abc"], "expected_stdout": "-42\n"},
            {"args": ["abc42"], "expected_stdout": "0\n"}
        ]
        
    elif name == "ft_range":
        ex["main_code"] = "#include <stdio.h>\n#include <stdlib.h>\nint *ft_range(int start, int end);\nint main(int argc, char **argv) {\n if (argc>2) { int s = atoi(argv[1]); int e = atoi(argv[2]); int *arr = ft_range(s, e); int len = (e >= s) ? (e - s + 1) : (s - e + 1); for(int i=0; i<len; i++) printf(\"%d \", arr[i]); printf(\"\\n\"); }\n return 0;\n}\n"
        ex["test_cases"] = [
            {"args": ["1", "3"], "expected_stdout": "1 2 3 \n"},
            {"args": ["-1", "2"], "expected_stdout": "-1 0 1 2 \n"},
            {"args": ["3", "1"], "expected_stdout": "3 2 1 \n"},
            {"args": ["0", "0"], "expected_stdout": "0 \n"}
        ]
        
    elif name == "ft_split":
        ex["main_code"] = "#include <stdio.h>\n#include <stdlib.h>\nchar **ft_split(char *str);\nint main(int argc, char **argv) {\n if (argc>1) { char **arr = ft_split(argv[1]); for(int i=0; arr[i]; i++) { printf(\"%s\\n\", arr[i]); } }\n return 0;\n}\n"
        ex["test_cases"] = [
            {"args": ["hello world"], "expected_stdout": "hello\nworld\n"},
            {"args": ["  hello   world  "], "expected_stdout": "hello\nworld\n"},
            {"args": ["single"], "expected_stdout": "single\n"},
            {"args": ["   "], "expected_stdout": ""}
        ]
        
    elif name == "count_of_2":
        ex["main_code"] = "#include <stdio.h>\n#include <stdlib.h>\nint count_of_2(int n);\nint main(int argc, char **argv) {\n if (argc>1) { printf(\"%d\\n\", count_of_2(atoi(argv[1]))); }\n return 0;\n}\n"
        ex["test_cases"] = [
            {"args": ["25"], "expected_stdout": "9\n"},
            {"args": ["2"], "expected_stdout": "1\n"},
            {"args": ["0"], "expected_stdout": "0\n"}
        ]

    elif name == "equation":
        ex["main_code"] = "void equation(int n);\n#include <stdlib.h>\nint main(int argc, char **argv) { if (argc>1) equation(atoi(argv[1])); return 0; }\n"
        ex["test_cases"] = [{"args": ["42"], "expected_stdout": None}]

    elif name == "print_memory":
        ex["main_code"] = "void print_memory(const void *addr, size_t size);\nint main(void) { int tab[10] = {0, 23, 150, 255, 12, 16, 21, 42}; print_memory(tab, sizeof(tab)); return 0; }\n"
        ex["test_cases"] = [{"args": [], "expected_stdout": None}]

    elif name in ["height_tree", "perimeter"]:
        ex["main_code"] = """#include <stdio.h>\n#include <stdlib.h>\n
struct s_node { int value; struct s_node **nodes; };
int height_tree(struct s_node *root);
void perimeter(struct s_node *root);
int main(void) { 
    struct s_node *n = malloc(sizeof(struct s_node)); 
    n->value = 1; n->nodes = malloc(sizeof(struct s_node*) * 2); n->nodes[0] = 0; n->nodes[1] = 0;
    if (1) height_tree(n);
    if (1) perimeter(n);
    return 0; 
}\n"""
        ex["test_cases"] = [{"args": [], "expected_stdout": None}]
        
    elif name == "g_diam":
        ex["test_cases"] = [
            {"args": ["9-12 12-13 13-14 14-9"], "expected_stdout": None}
        ]

def generate_test_cases(is_function, ret_type, name):
    cases = []
    if name == "ft_countdown":
        cases.append({"args": [], "expected_stdout": "9876543210\n"})
    elif name == "hello":
        cases.append({"args": [], "expected_stdout": "Hello World!\n"})
    elif is_function:
        cases.append({"args": ["hello"], "expected_stdout": None})
        cases.append({"args": ["test", "test2"], "expected_stdout": None})
        cases.append({"args": ["123", "456"], "expected_stdout": None})
        cases.append({"args": [""], "expected_stdout": None})
    else:
        cases.append({"args": ["test_arg"], "expected_stdout": None})
        cases.append({"args": ["hello", "world"], "expected_stdout": None})
        cases.append({"args": [], "expected_stdout": None})
    return cases

def process_exercises():
    raw = get_official_42_exercises() + get_extended_custom_exercises()
    
    for ex in raw:
        # Generate Official Testcases
        if ex.get("source_type") == "42_official":
            inject_official_testcases(ex)
            
            # If no custom testcases were injected above, provide fallback edgecases
            if not ex.get("test_cases"):
                ret_type = ""
                proto = ex.get("prototype", "")
                if proto:
                    match = re.match(r'^(.*?)\s+([a-zA-Z0-9_]+)\((.*)\);?$', proto.strip())
                    if match:
                        ret_type = match.group(1).strip()
                ex["test_cases"] = generate_test_cases(ex["is_function"], ret_type, ex["name"])
                
            # Generate C wrappers for functions if not explicitly overridden
            if ex["is_function"] and ex.get("prototype") and not ex.get("main_code"):
                ex["main_code"] = generate_function_wrapper(ex["prototype"], ex["name"])
                
        # Generate Extended Custom Testcases
        elif ex.get("source_type") == "examshelp_extended":
            old_hints = ex.get("hints", [])
            new_hints = old_hints[:]
            new_hints.append("Watch out for edge cases like NULL pointers, empty strings, and negative numbers!")
            new_hints.append("Ensure you only use the allowed functions. Mallocs must be freed appropriately (if applicable).")
            ex["hints"] = new_hints
            
            # Enhance subject for Level 0-2 beginners
            subject = ex["subject"]
            subject += "\n=== EXAMPLES & INSTRUCTIONS ===\n"
            if ex["is_function"]:
                subject += "You must write a C function (not a standalone program).\n"
                subject += f"Your function must be prototyped exactly as: {ex.get('prototype', 'void func();')}\n"
                subject += "Make sure you include the necessary headers if you use allowed functions.\n"
                subject += "Do NOT submit a main() function in your final file, or compilation will fail!\n"
            else:
                subject += "You must write a full C program with a standard `main()` function.\n"
                subject += "Your program must compile and handle command-line arguments (argc, argv).\n"
                subject += "If the number of arguments is unexpected, or if you encounter an error, failing gracefully (e.g. returning 0 or printing a newline) is standard practice.\n"
                subject += f"\nExample compilation and execution:\n$> gcc -Wall -Wextra -Werror {ex['expected_files']} -o {ex['name']}\n$> ./{ex['name']} \"example input\" | cat -e\n...output...$\n$> ./{ex['name']} | cat -e\n$\n$>\n"
            ex["subject"] = subject
            
            if not ex.get("test_cases"):
                ret_type = ""
                proto = ex.get("prototype", "")
                if proto:
                    match = re.match(r'^(.*?)\s+([a-zA-Z0-9_]+)\((.*)\);?$', proto.strip())
                    if match:
                        ret_type = match.group(1).strip()
                ex["test_cases"] = generate_test_cases(ex["is_function"], ret_type, ex["name"])
                
            if ex["is_function"] and ex.get("prototype"):
                ex["main_code"] = generate_function_wrapper(ex["prototype"], ex["name"])

    levels = map_to_10_levels(raw)
    
    official_count = len([e for e in raw if e.get("source_type") == "42_official"])
    extended_count = len([e for e in raw if e.get("source_type") == "examshelp_extended"])
    
    db = {
        'total_exercises': len(raw),
        'official_42_count': official_count,
        'extended_count': extended_count,
        'total_levels': 10,
        'levels': levels
    }
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_path = os.path.join(base_dir, 'config', 'exercises_db.json')
    
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=2)
        
    print(f"Massive Upgrade Complete: {len(raw)} exercises parsed with wrappers & test cases!")

if __name__ == '__main__':
    process_exercises()
