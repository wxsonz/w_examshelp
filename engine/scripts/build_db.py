import os
import json

def get_official_42_exercises():
    """Defines the suite of Official 42 Exam exercises."""
    return [
        # Level 0
        {
            "id": "beg_aff_a", "name": "aff_a", "source": "beginner", "source_type": "42_official", "orig_level": 0,
            "expected_files": "aff_a.c", "allowed_functions": "write", "is_function": False, "prototype": None,
            "subject": """Assignment name  : aff_a\nExpected files   : aff_a.c\nAllowed functions: write\n--------------------------------------------------------------------------------\n\nWrite a program that takes a string, and displays the first 'a' character it\nencounters in it, followed by a newline. If there are no 'a' characters in the\nstring, the program just writes a newline. If the number of parameters is not\n1, the program displays 'a' followed by a newline.\n""",
            "test_cases": [{"cmd": "./aff_a \"abc\" | cat -e", "args": ["abc"], "expected_stdout": "a\n"}, {"cmd": "./aff_a | cat -e", "args": [], "expected_stdout": "a\n"}],
            "hints": ["Check argc != 2 first. Iterate over argv[1] looking for 'a'."]
        },
        {
            "id": "beg_ft_countdown", "name": "ft_countdown", "source": "beginner", "source_type": "42_official", "orig_level": 0,
            "expected_files": "ft_countdown.c", "allowed_functions": "write", "is_function": False, "prototype": None,
            "subject": """Assignment name  : ft_countdown\nExpected files   : ft_countdown.c\nAllowed functions: write\n--------------------------------------------------------------------------------\n\nWrite a program that displays all digits in descending order, followed by a newline.\n""",
            "test_cases": [{"cmd": "./ft_countdown | cat -e", "args": [], "expected_stdout": "9876543210\n"}],
            "hints": ["Write digits '9' down to '0' followed by '\\n'."]
        },
        {
            "id": "beg_ft_print_numbers", "name": "ft_print_numbers", "source": "beginner", "source_type": "42_official", "orig_level": 0,
            "expected_files": "ft_print_numbers.c", "allowed_functions": "write", "is_function": True, "prototype": "void ft_print_numbers(void);",
            "subject": """Assignment name  : ft_print_numbers\nExpected files   : ft_print_numbers.c\nAllowed functions: write\n--------------------------------------------------------------------------------\n\nWrite a function that displays all digits in ascending order.\n""",
            "test_cases": [], "hints": ["Use a loop from '0' to '9' with write(1, &c, 1)."]
        },
        {
            "id": "beg_hello", "name": "hello", "source": "beginner", "source_type": "42_official", "orig_level": 0,
            "expected_files": "hello.c", "allowed_functions": "write", "is_function": False, "prototype": None,
            "subject": """Assignment name  : hello\nExpected files   : hello.c\nAllowed functions: write\n--------------------------------------------------------------------------------\n\nWrite a program that displays "Hello World!" followed by a newline.\n""",
            "test_cases": [{"cmd": "./hello | cat -e", "args": [], "expected_stdout": "Hello World!\n"}], "hints": ["write(1, \"Hello World!\\n\", 13);"]
        },
        {
            "id": "beg_maff_alpha", "name": "maff_alpha", "source": "beginner", "source_type": "42_official", "orig_level": 0,
            "expected_files": "maff_alpha.c", "allowed_functions": "write", "is_function": False, "prototype": None,
            "subject": """Assignment name  : maff_alpha\nExpected files   : maff_alpha.c\nAllowed functions: write\n--------------------------------------------------------------------------------\n\nWrite a program that displays the alphabet in alternating case (aBcDeFg...z) followed by a newline.\n""",
            "test_cases": [{"cmd": "./maff_alpha | cat -e", "args": [], "expected_stdout": "aBcDeFgHiJkLmNoPqRsTuVwXyZ\n"}], "hints": ["Alternating lowercase and uppercase."]
        },

        # Level 1
        {
            "id": "beg_ft_strcpy", "name": "ft_strcpy", "source": "beginner", "source_type": "42_official", "orig_level": 1,
            "expected_files": "ft_strcpy.c", "allowed_functions": "None", "is_function": True, "prototype": "char *ft_strcpy(char *s1, char *s2);",
            "subject": """Assignment name  : ft_strcpy\nExpected files   : ft_strcpy.c\nAllowed functions: None\n--------------------------------------------------------------------------------\n\nReproduce the behavior of strcpy.\n""",
            "test_cases": [], "hints": ["Copy s2 into s1 including null terminator."]
        },
        {
            "id": "beg_ft_strlen", "name": "ft_strlen", "source": "beginner", "source_type": "42_official", "orig_level": 1,
            "expected_files": "ft_strlen.c", "allowed_functions": "None", "is_function": True, "prototype": "int ft_strlen(char *str);",
            "subject": """Assignment name  : ft_strlen\nExpected files   : ft_strlen.c\nAllowed functions: None\n--------------------------------------------------------------------------------\n\nReturns string length.\n""",
            "test_cases": [], "hints": ["Count chars until '\\0'."]
        },
        {
            "id": "beg_first_word", "name": "first_word", "source": "beginner", "source_type": "42_official", "orig_level": 1,
            "expected_files": "first_word.c", "allowed_functions": "write", "is_function": False, "prototype": None,
            "subject": """Assignment name  : first_word\nExpected files   : first_word.c\nAllowed functions: write\n--------------------------------------------------------------------------------\n\nDisplays first word of a string.\n""",
            "test_cases": [{"cmd": "./first_word \"FOR MAXIMUS\" | cat -e", "args": ["FOR MAXIMUS"], "expected_stdout": "FOR\n"}], "hints": ["Skip leading spaces."]
        },

        # Level 2
        {
            "id": "beg_ft_atoi", "name": "ft_atoi", "source": "beginner", "source_type": "42_official", "orig_level": 2,
            "expected_files": "ft_atoi.c", "allowed_functions": "None", "is_function": True, "prototype": "int ft_atoi(const char *str);",
            "subject": """Assignment name  : ft_atoi\nExpected files   : ft_atoi.c\nAllowed functions: None\n--------------------------------------------------------------------------------\n\nConvert string to int.\n""",
            "test_cases": [], "hints": ["Skip whitespace, handle sign, parse digits."]
        },
        {
            "id": "beg_inter", "name": "inter", "source": "beginner", "source_type": "42_official", "orig_level": 2,
            "expected_files": "inter.c", "allowed_functions": "write", "is_function": False, "prototype": None,
            "subject": """Assignment name  : inter\nExpected files   : inter.c\nAllowed functions: write\n--------------------------------------------------------------------------------\n\nDisplays characters appearing in both s1 and s2 without doubles.\n""",
            "test_cases": [{"cmd": "./inter \"padinton\" \"paqefwtdjnty\" | cat -e", "args": ["padinton", "paqefwtdjnty"], "expected_stdout": "padinto\n"}], "hints": ["256 lookup array."]
        },

        # Level 3
        {
            "id": "beg_ft_range", "name": "ft_range", "source": "beginner", "source_type": "42_official", "orig_level": 3,
            "expected_files": "ft_range.c", "allowed_functions": "malloc", "is_function": True, "prototype": "int *ft_range(int start, int end);",
            "subject": """Assignment name  : ft_range\nExpected files   : ft_range.c\nAllowed functions: malloc\n--------------------------------------------------------------------------------\n\nReturns array of ints from start to end.\n""",
            "test_cases": [], "hints": ["Size = abs(end - start) + 1."]
        },

        # Level 4
        {
            "id": "beg_ft_split", "name": "ft_split", "source": "beginner", "source_type": "42_official", "orig_level": 4,
            "expected_files": "ft_split.c", "allowed_functions": "malloc", "is_function": True, "prototype": "char **ft_split(char *str);",
            "subject": """Assignment name  : ft_split\nExpected files   : ft_split.c\nAllowed functions: malloc\n--------------------------------------------------------------------------------\n\nSplits string into array of strings.\n""",
            "test_cases": [], "hints": ["Allocate char** array then allocate each word."]
        },

        # Level 5
        {
            "id": "beg_print_memory", "name": "print_memory", "source": "beginner", "source_type": "42_official", "orig_level": 5,
            "expected_files": "print_memory.c", "allowed_functions": "write", "is_function": True, "prototype": "void print_memory(const void *addr, size_t size);",
            "subject": """Assignment name  : print_memory\nExpected files   : print_memory.c\nAllowed functions: write\n--------------------------------------------------------------------------------\n\nHex dump memory area.\n""",
            "test_cases": [], "hints": ["Process 16 bytes per row."]
        },

        # Level 6
        {
            "id": "inter_count_of_2", "name": "count_of_2", "source": "intermediate", "source_type": "42_official", "orig_level": 0,
            "expected_files": "count_of_2.c", "allowed_functions": "None", "is_function": True, "prototype": "int count_of_2(int n);",
            "subject": """Assignment name  : count_of_2\nExpected files   : count_of_2.c\nAllowed functions: None\n--------------------------------------------------------------------------------\n\nCounts total '2' digits from 0 to n.\n""",
            "test_cases": [], "hints": ["Digit extraction with % 10."]
        },
        {
            "id": "inter_equation", "name": "equation", "source": "intermediate", "source_type": "42_official", "orig_level": 0,
            "expected_files": "equation.c", "allowed_functions": "printf", "is_function": True, "prototype": "void equation(int n);",
            "subject": """Assignment name  : equation\nExpected files   : equation.c\nAllowed functions: printf\n--------------------------------------------------------------------------------\n\nFinds digits A, B, C for AB + CA = n.\n""",
            "test_cases": [], "hints": ["Triple loop for A, B, C [0-9]."]
        },

        # Level 7
        {
            "id": "inter_height_tree", "name": "height_tree", "source": "intermediate", "source_type": "42_official", "orig_level": 1,
            "expected_files": "height_tree.c", "allowed_functions": "None", "is_function": True, "prototype": "int height_tree(struct s_node *root);",
            "subject": """Assignment name  : height_tree\nExpected files   : height_tree.c\nAllowed functions: None\n--------------------------------------------------------------------------------\n\nMax height of binary tree.\n""",
            "test_cases": [], "hints": ["Recursive depth."]
        },

        # Level 8
        {
            "id": "inter_perimeter", "name": "perimeter", "source": "intermediate", "source_type": "42_official", "orig_level": 3,
            "expected_files": "perimeter.c", "allowed_functions": "printf", "is_function": True, "prototype": "void perimeter(struct s_node *root);",
            "subject": """Assignment name  : perimeter\nExpected files   : perimeter.c\nAllowed functions: printf\n--------------------------------------------------------------------------------\n\nPrints boundary of binary tree.\n""",
            "test_cases": [], "hints": ["Left boundary, leaves, right boundary."]
        },

        # Level 9
        {
            "id": "inter_g_diam", "name": "g_diam", "source": "intermediate", "source_type": "42_official", "orig_level": 5,
            "expected_files": "g_diam.c", "allowed_functions": "write, malloc, free", "is_function": False, "prototype": None,
            "subject": """Assignment name  : g_diam\nExpected files   : g_diam.c\nAllowed functions: write, malloc, free\n--------------------------------------------------------------------------------\n\nDiameter of graph.\n""",
            "test_cases": [], "hints": ["DFS with backtracking."]
        }
    ]

def get_extended_custom_exercises():
    customs = []
    
    # Extended Level 0
    l0_defs = [
        ("aff_vowels", "aff_vowels.c", "write", False, None, "Prints all vowels in string."),
        ("ft_isspace", "ft_isspace.c", "None", True, "int ft_isspace(int c);", "Checks if c is whitespace."),
        ("only_even_digits", "only_even_digits.c", "write", False, None, "Prints even digits 02468."),
        ("aff_first_vowel", "aff_first_vowel.c", "write", False, None, "Prints first vowel in string."),
        ("ft_putchar_repeat", "ft_putchar_repeat.c", "write", True, "void ft_putchar_repeat(char c, int n);", "Prints char c n times."),
        ("swap_case_char", "swap_case_char.c", "write", False, None, "Swaps case of single char parameter."),
        ("print_reverse_alphabet", "print_reverse_alphabet.c", "write", False, None, "Prints z-a in lowercase."),
        ("ft_is_digit", "ft_is_digit.c", "None", True, "int ft_is_digit(int c);", "Returns 1 if digit, else 0.")
    ]
    for name, exp, fns, is_func, proto, desc in l0_defs:
        customs.append({
            "id": f"ext_{name}", "name": name, "source": "beginner", "source_type": "examshelp_extended", "orig_level": 0,
            "expected_files": exp, "allowed_functions": fns, "is_function": is_func, "prototype": proto,
            "subject": f"Assignment name  : {name}\nExpected files   : {exp}\nAllowed functions: {fns}\n--------------------------------------------------------------------------------\n\n{desc}\n",
            "test_cases": [], "hints": [desc]
        })

    # Expanded Level 1
    l1_defs = [
        ("ft_strchr", "ft_strchr.c", "None", True, "char *ft_strchr(const char *s, int c);", "Locates first occurrence of c in s."),
        ("ft_strrchr", "ft_strrchr.c", "None", True, "char *ft_strrchr(const char *s, int c);", "Locates last occurrence of c in s."),
        ("ft_is_palindrome", "ft_is_palindrome.c", "write", False, None, "Checks if string is palindrome."),
        ("rot_n", "rot_n.c", "write", False, None, "Rotates alphabetic chars by N positions."),
        ("clean_spaces", "clean_spaces.c", "write", False, None, "Trims extra whitespace from string."),
        ("ft_strncat", "ft_strncat.c", "None", True, "char *ft_strncat(char *s1, const char *s2, size_t n);", "Concatenates n chars of s2 onto s1."),
        ("ft_strncmp", "ft_strncmp.c", "None", True, "int ft_strncmp(const char *s1, const char *s2, size_t n);", "Compares up to n chars."),
        ("ft_strequ", "ft_strequ.c", "None", True, "int ft_strequ(char const *s1, char const *s2);", "Returns 1 if s1 and s2 are equal."),
        ("ft_isupper", "ft_isupper.c", "None", True, "int ft_isupper(int c);", "Returns 1 if uppercase char."),
        ("ft_islower", "ft_islower.c", "None", True, "int ft_islower(int c);", "Returns 1 if lowercase char."),
        ("ft_isalpha", "ft_isalpha.c", "None", True, "int ft_isalpha(int c);", "Returns 1 if alphabetic char."),
        ("ft_isalnum", "ft_isalnum.c", "None", True, "int ft_isalnum(int c);", "Returns 1 if alphanumeric char."),
        ("ft_isprint", "ft_isprint.c", "None", True, "int ft_isprint(int c);", "Returns 1 if printable char."),
        ("ft_toupper", "ft_toupper.c", "None", True, "int ft_toupper(int c);", "Converts char to uppercase."),
        ("ft_tolower", "ft_tolower.c", "None", True, "int ft_tolower(int c);", "Converts char to lowercase."),
        ("ft_strcat", "ft_strcat.c", "None", True, "char *ft_strcat(char *s1, const char *s2);", "Appends s2 to s1."),
        ("ft_strcmp", "ft_strcmp.c", "None", True, "int ft_strcmp(const char *s1, const char *s2);", "Compares two strings lexicographically."),
        ("ft_str_is_alpha", "ft_str_is_alpha.c", "None", True, "int ft_str_is_alpha(char *str);", "Checks if string contains only letters."),
        ("ft_str_is_numeric", "ft_str_is_numeric.c", "None", True, "int ft_str_is_numeric(char *str);", "Checks if string contains only digits."),
        ("ft_str_is_lowercase", "ft_str_is_lowercase.c", "None", True, "int ft_str_is_lowercase(char *str);", "Checks if string contains only lowercase."),
        ("ft_str_is_uppercase", "ft_str_is_uppercase.c", "None", True, "int ft_str_is_uppercase(char *str);", "Checks if string contains only uppercase."),
        ("ft_str_is_printable", "ft_str_is_printable.c", "None", True, "int ft_str_is_printable(char *str);", "Checks if string contains only printable chars."),
        ("ft_strcapitalize", "ft_strcapitalize.c", "None", True, "char *ft_strcapitalize(char *str);", "Capitalizes first letter of every word."),
        ("ft_strlcpy", "ft_strlcpy.c", "None", True, "size_t ft_strlcpy(char *dst, const char *src, size_t dstsize);", "Size-bounded string copy."),
        ("ft_strlcat", "ft_strlcat.c", "None", True, "size_t ft_strlcat(char *dst, const char *src, size_t dstsize);", "Size-bounded string concat."),
        ("aff_last_vowel", "aff_last_vowel.c", "write", False, None, "Displays last vowel in string."),
        ("count_vowels", "count_vowels.c", "write", False, None, "Displays total count of vowels in string."),
        ("count_consonants", "count_consonants.c", "write", False, None, "Displays total count of consonants in string.")
    ]
    for name, exp, fns, is_func, proto, desc in l1_defs:
        customs.append({
            "id": f"ext_{name}", "name": name, "source": "beginner", "source_type": "examshelp_extended", "orig_level": 1,
            "expected_files": exp, "allowed_functions": fns, "is_function": is_func, "prototype": proto,
            "subject": f"Assignment name  : {name}\nExpected files   : {exp}\nAllowed functions: {fns}\n--------------------------------------------------------------------------------\n\n{desc}\n",
            "test_cases": [], "hints": [desc]
        })

    # Expanded Level 2
    l2_defs = [
        ("count_set_bits", "count_set_bits.c", "None", True, "int count_set_bits(unsigned char octet);", "Counts set 1-bits in octet."),
        ("ft_strpbrk", "ft_strpbrk.c", "None", True, "char *ft_strpbrk(const char *s1, const char *s2);", "Finds first match of s2 char in s1."),
        ("ft_strstr", "ft_strstr.c", "None", True, "char *ft_strstr(char *haystack, char *needle);", "Locates substring needle in haystack."),
        ("ft_count_words", "ft_count_words.c", "None", True, "int ft_count_words(const char *str);", "Counts words separated by whitespace."),
        ("ft_reverse_words", "ft_reverse_words.c", "write", False, None, "Reverses order of words in string."),
        ("toggle_bits", "toggle_bits.c", "None", True, "unsigned char toggle_bits(unsigned char octet);", "Inverts all bits in octet."),
        ("ft_strcasestr", "ft_strcasestr.c", "None", True, "char *ft_strcasestr(const char *s1, const char *s2);", "Case-insensitive substring search."),
        ("ft_is_anagram", "ft_is_anagram.c", "None", True, "int ft_is_anagram(char *s1, char *s2);", "Checks if two strings are anagrams."),
        ("ft_strdup", "ft_strdup.c", "malloc", True, "char *ft_strdup(const char *s1);", "Duplicates string with malloc."),
        ("ft_ndup", "ft_ndup.c", "malloc", True, "char *ft_ndup(const char *s1, size_t n);", "Duplicates first n characters with malloc."),
        ("ft_memchr", "ft_memchr.c", "None", True, "void *ft_memchr(const void *s, int c, size_t n);", "Locates byte c in memory area s."),
        ("ft_memset", "ft_memset.c", "None", True, "void *ft_memset(void *b, int c, size_t len);", "Fills len bytes of b with byte c."),
        ("ft_bzero", "ft_bzero.c", "None", True, "void ft_bzero(void *s, size_t n);", "Zeros out n bytes of memory area s."),
        ("ft_memcpy", "ft_memcpy.c", "None", True, "void *ft_memcpy(void *dst, const void *src, size_t n);", "Copies n bytes from src to dst."),
        ("print_hex_byte", "print_hex_byte.c", "write", True, "void print_hex_byte(unsigned char c);", "Prints 2-digit hex representation of byte."),
        ("swap_nibbles", "swap_nibbles.c", "None", True, "unsigned char swap_nibbles(unsigned char octet);", "Swaps high and low 4 bits."),
        ("is_power_of_4", "is_power_of_4.c", "None", True, "int is_power_of_4(unsigned int n);", "Returns 1 if n is power of 4."),
        ("ft_str_replace", "ft_str_replace.c", "None", True, "void ft_str_replace(char *str, char old_c, char new_c);", "Replaces occurrences of old_c with new_c."),
        ("ft_count_char", "ft_count_char.c", "None", True, "int ft_count_char(const char *str, char c);", "Counts occurrences of char c in string."),
        ("ft_str_reverse", "ft_str_reverse.c", "None", True, "char *ft_str_reverse(char *str);", "Reverses string in-place."),
        ("ft_is_sorted", "ft_is_sorted.c", "None", True, "int ft_is_sorted(int *tab, int length, int (*f)(int, int));", "Checks if array is sorted by f."),
        ("ft_find_max", "ft_find_max.c", "None", True, "int ft_find_max(int *arr, int size);", "Returns max element in array."),
        ("ft_find_min", "ft_find_min.c", "None", True, "int ft_find_min(int *arr, int size);", "Returns min element in array."),
        ("ft_array_sum", "ft_array_sum.c", "None", True, "long ft_array_sum(int *arr, int size);", "Returns sum of array elements.")
    ]
    for name, exp, fns, is_func, proto, desc in l2_defs:
        customs.append({
            "id": f"ext_{name}", "name": name, "source": "beginner", "source_type": "examshelp_extended", "orig_level": 2,
            "expected_files": exp, "allowed_functions": fns, "is_function": is_func, "prototype": proto,
            "subject": f"Assignment name  : {name}\nExpected files   : {exp}\nAllowed functions: {fns}\n--------------------------------------------------------------------------------\n\n{desc}\n",
            "test_cases": [], "hints": [desc]
        })

    # Expanded Level 3
    l3_defs = [
        ("ft_strjoin", "ft_strjoin.c", "malloc", True, "char *ft_strjoin(char const *s1, char const *s2);", "Concatenates s1 and s2 with malloc."),
        ("ft_strtrim", "ft_strtrim.c", "malloc", True, "char *ft_strtrim(char const *s1, char const *set);", "Trims characters in set from s1."),
        ("ft_strmapi", "ft_strmapi.c", "malloc", True, "char *ft_strmapi(char const *s, char (*f)(unsigned int, char));", "Applies f to each char in s."),
        ("ft_striteri", "ft_striteri.c", "None", True, "void ft_striteri(char *s, void (*f)(unsigned int, char*));", "Applies in-place f to each char in s."),
        ("fibonacci_seq", "fibonacci_seq.c", "write", False, None, "Prints Nth fibonacci number."),
        ("prime_factors", "prime_factors.c", "write", False, None, "Prints prime factors of integer parameter."),
        ("ft_calloc", "ft_calloc.c", "malloc", True, "void *ft_calloc(size_t count, size_t size);", "Allocates and zeros memory buffer."),
        ("ft_itoa", "ft_itoa.c", "malloc", True, "char *ft_itoa(int n);", "Converts integer to string with malloc."),
        ("ft_atoi_base", "ft_atoi_base.c", "None", True, "int ft_atoi_base(const char *str, int str_base);", "Converts string in base str_base to int."),
        ("ft_itoa_base", "ft_itoa_base.c", "malloc", True, "char *ft_itoa_base(int value, int base);", "Converts int to string in specified base."),
        ("ft_strndup", "ft_strndup.c", "malloc", True, "char *ft_strndup(const char *s1, size_t n);", "Allocates and copies n chars of s1."),
        ("ft_split_whitespaces", "ft_split_whitespaces.c", "malloc", True, "char **ft_split_whitespaces(char *str);", "Splits string by whitespace into char** array."),
        ("ft_range_step", "ft_range_step.c", "malloc", True, "int *ft_range_step(int start, int end, int step);", "Returns array from start to end by step."),
        ("gcd", "gcd.c", "write", False, None, "Prints Greatest Common Divisor of two ints."),
        ("lcm", "lcm.c", "write", False, None, "Prints Least Common Multiple of two ints."),
        ("is_prime", "is_prime.c", "None", True, "int is_prime(int n);", "Returns 1 if n is prime number."),
        ("next_prime", "next_prime.c", "None", True, "int next_prime(int n);", "Returns next prime >= n."),
        ("sqrt_int", "sqrt_int.c", "None", True, "int sqrt_int(int n);", "Returns integer square root of n or 0."),
        ("power_int", "power_int.c", "None", True, "long power_int(int nb, int power);", "Computes nb raised to power."),
        ("factorial", "factorial.c", "None", True, "long factorial(int n);", "Computes factorial of n.")
    ]
    for name, exp, fns, is_func, proto, desc in l3_defs:
        customs.append({
            "id": f"ext_{name}", "name": name, "source": "beginner", "source_type": "examshelp_extended", "orig_level": 3,
            "expected_files": exp, "allowed_functions": fns, "is_function": is_func, "prototype": proto,
            "subject": f"Assignment name  : {name}\nExpected files   : {exp}\nAllowed functions: {fns}\n--------------------------------------------------------------------------------\n\n{desc}\n",
            "test_cases": [], "hints": [desc]
        })

    # Extended Level 4
    l4_defs = [
        ("snake_to_camel", "snake_to_camel.c", "write", False, None, "Converts snake_case to camelCase."),
        ("camel_to_snake", "camel_to_snake.c", "write", False, None, "Converts camelCase to snake_case."),
        ("ft_matrix_transpose", "ft_matrix_transpose.c", "malloc", True, "int **ft_matrix_transpose(int **m, int r, int c);", "Transposes 2D matrix."),
        ("ft_substr", "ft_substr.c", "malloc", True, "char *ft_substr(char const *s, unsigned int start, size_t len);", "Creates substring."),
        ("ft_remove_duplicates", "ft_remove_duplicates.c", "malloc", True, "int *ft_remove_duplicates(int *arr, int size, int *new_size);", "Removes duplicate ints.")
    ]
    for name, exp, fns, is_func, proto, desc in l4_defs:
        customs.append({
            "id": f"ext_{name}", "name": name, "source": "beginner", "source_type": "examshelp_extended", "orig_level": 4,
            "expected_files": exp, "allowed_functions": fns, "is_function": is_func, "prototype": proto,
            "subject": f"Assignment name  : {name}\nExpected files   : {exp}\nAllowed functions: {fns}\n--------------------------------------------------------------------------------\n\n{desc}\n",
            "test_cases": [], "hints": [desc]
        })

    # Extended Level 5
    l5_defs = [
        ("ft_memmove", "ft_memmove.c", "None", True, "void *ft_memmove(void *dest, const void *src, size_t n);", "Copies n bytes with memory overlap safety."),
        ("ft_memcmp", "ft_memcmp.c", "None", True, "int ft_memcmp(const void *s1, const void *s2, size_t n);", "Compares memory byte buffers."),
        ("ft_sort_string_tab", "ft_sort_string_tab.c", "None", True, "void ft_sort_string_tab(char **tab);", "Sorts null-terminated array of strings."),
        ("ft_matrix_rotate", "ft_matrix_rotate.c", "None", True, "void ft_matrix_rotate(int **matrix, int n);", "Rotates square matrix 90 deg clockwise."),
        ("ft_spiral_matrix", "ft_spiral_matrix.c", "printf", True, "void ft_spiral_matrix(int **m, int r, int c);", "Prints matrix in spiral order.")
    ]
    for name, exp, fns, is_func, proto, desc in l5_defs:
        customs.append({
            "id": f"ext_{name}", "name": name, "source": "beginner", "source_type": "examshelp_extended", "orig_level": 5,
            "expected_files": exp, "allowed_functions": fns, "is_function": is_func, "prototype": proto,
            "subject": f"Assignment name  : {name}\nExpected files   : {exp}\nAllowed functions: {fns}\n--------------------------------------------------------------------------------\n\n{desc}\n",
            "test_cases": [], "hints": [desc]
        })

    # Extended Level 6
    l6_defs = [
        ("ft_list_push_back", "ft_list_push_back.c, ft_list.h", "malloc", True, "void ft_list_push_back(t_list **begin_list, void *data);", "Appends node to linked list."),
        ("ft_list_reverse", "ft_list_reverse.c, ft_list.h", "None", True, "void ft_list_reverse(t_list **begin_list);", "Reverses linked list in-place."),
        ("ft_list_find", "ft_list_find.c, ft_list.h", "None", True, "t_list *ft_list_find(t_list *begin_list, void *data_ref, int (*cmp)());", "Finds node in list matching cmp."),
        ("ft_list_at", "ft_list_at.c, ft_list.h", "None", True, "t_list *ft_list_at(t_list *begin_list, unsigned int n);", "Returns Nth node of linked list.")
    ]
    for name, exp, fns, is_func, proto, desc in l6_defs:
        customs.append({
            "id": f"ext_{name}", "name": name, "source": "intermediate", "source_type": "examshelp_extended", "orig_level": 0,
            "expected_files": exp, "allowed_functions": fns, "is_function": is_func, "prototype": proto,
            "subject": f"Assignment name  : {name}\nExpected files   : {exp}\nAllowed functions: {fns}\n--------------------------------------------------------------------------------\n\n{desc}\n",
            "test_cases": [], "hints": [desc]
        })

    # Extended Level 7
    l7_defs = [
        ("ft_tree_depth", "ft_tree_depth.c", "None", True, "int ft_tree_depth(t_node *root);", "Calculates depth of binary tree."),
        ("ft_tree_is_balanced", "ft_tree_is_balanced.c", "None", True, "int ft_tree_is_balanced(t_node *root);", "Checks if binary tree is height balanced."),
        ("ft_parentheses_val", "ft_parentheses_val.c", "write", False, None, "Validates nested parentheses/brackets using stack.")
    ]
    for name, exp, fns, is_func, proto, desc in l7_defs:
        customs.append({
            "id": f"ext_{name}", "name": name, "source": "intermediate", "source_type": "examshelp_extended", "orig_level": 1,
            "expected_files": exp, "allowed_functions": fns, "is_function": is_func, "prototype": proto,
            "subject": f"Assignment name  : {name}\nExpected files   : {exp}\nAllowed functions: {fns}\n--------------------------------------------------------------------------------\n\n{desc}\n",
            "test_cases": [], "hints": [desc]
        })

    # Extended Level 8
    l8_defs = [
        ("eval_expr", "eval_expr.c", "write", False, None, "Evaluates arithmetic expression string."),
        ("sudoku_solver", "sudoku_solver.c", "write", False, None, "Solves 9x9 Sudoku puzzle using backtracking.")
    ]
    for name, exp, fns, is_func, proto, desc in l8_defs:
        customs.append({
            "id": f"ext_{name}", "name": name, "source": "intermediate", "source_type": "examshelp_extended", "orig_level": 3,
            "expected_files": exp, "allowed_functions": fns, "is_function": is_func, "prototype": proto,
            "subject": f"Assignment name  : {name}\nExpected files   : {exp}\nAllowed functions: {fns}\n--------------------------------------------------------------------------------\n\n{desc}\n",
            "test_cases": [], "hints": [desc]
        })

    # Extended Level 9
    l9_defs = [
        ("shortest_path", "shortest_path.c", "malloc, free, write", False, None, "Finds shortest path in weighted graph matrix.")
    ]
    for name, exp, fns, is_func, proto, desc in l9_defs:
        customs.append({
            "id": f"ext_{name}", "name": name, "source": "intermediate", "source_type": "examshelp_extended", "orig_level": 5,
            "expected_files": exp, "allowed_functions": fns, "is_function": is_func, "prototype": proto,
            "subject": f"Assignment name  : {name}\nExpected files   : {exp}\nAllowed functions: {fns}\n--------------------------------------------------------------------------------\n\n{desc}\n",
            "test_cases": [], "hints": [desc]
        })

    return customs

def map_to_10_levels(raw_exercises):
    levels = {str(i): [] for i in range(10)}
    
    for ex in raw_exercises:
        src = ex['source']
        orig = ex['orig_level']
        
        if src == 'beginner':
            if orig == 0:
                target_level = 0
            elif orig == 1:
                target_level = 1
            elif orig == 2:
                target_level = 2
            elif orig == 3:
                target_level = 3
            elif orig == 4:
                target_level = 4
            elif orig == 5:
                target_level = 5
            else:
                target_level = 5
        else: # intermediate
            if orig == 0:
                target_level = 6
            elif orig == 1:
                target_level = 7
            elif orig == 2:
                target_level = 7
            elif orig == 3:
                target_level = 8
            elif orig == 4:
                target_level = 8
            elif orig == 5:
                target_level = 9
            else:
                target_level = 9
                
        levels[str(target_level)].append(ex)
        
    return levels

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_dir = os.path.join(base_dir, 'config')
    os.makedirs(config_dir, exist_ok=True)
    
    raw = get_official_42_exercises() + get_extended_custom_exercises()
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
    
    out_path = os.path.join(config_dir, 'exercises_db.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=2)
        
    print(f"Successfully generated {out_path} with {len(raw)} exercises ({official_count} Official 42 + {extended_count} Extended Custom) across 10 levels.")

if __name__ == '__main__':
    main()
