EXTENDED_SUBJECTS = {
    "ft_is_digit": {
        "en": "Write a function that checks if a passed character (represented as an int) is a decimal digit ('0' to '9').\nIt must return 1 if the character is a digit, and 0 otherwise.",
        "th": "เขียนฟังก์ชันเพื่อตรวจสอบว่าตัวอักษรที่ส่งเข้ามา (ในรูปแบบ int) เป็นตัวเลข ('0' ถึง '9') หรือไม่\nฟังก์ชันต้องคืนค่า 1 หากเป็นตัวเลข และคืนค่า 0 หากไม่ใช่"
    },
    "ft_isspace": {
        "en": "Write a function that checks whether a passed character is a standard whitespace character.\nThis includes space (' '), form-feed ('\\f'), newline ('\\n'), carriage return ('\\r'), horizontal tab ('\\t'), and vertical tab ('\\v').\nReturn 1 if it is a whitespace, 0 otherwise.",
        "th": "เขียนฟังก์ชันตรวจสอบว่าตัวอักษรเป็นช่องว่างมาตรฐานหรือไม่ (เช่น ' ', '\\n', '\\t', '\\r', '\\v', '\\f')\nให้คืนค่า 1 หากเป็นช่องว่าง และ 0 หากไม่ใช่"
    },
    "swap_case_char": {
        "en": "Write a program or function that takes a single character and swaps its case.\nIf it's an uppercase letter, convert it to lowercase. If it's a lowercase letter, convert it to uppercase.\nIf it's not a letter, return it unchanged.",
        "th": "เขียนโปรแกรมหรือฟังก์ชันที่รับตัวอักษร 1 ตัวและสลับตัวพิมพ์\nหากเป็นตัวพิมพ์ใหญ่ให้เปลี่ยนเป็นพิมพ์เล็ก หากเป็นพิมพ์เล็กให้เปลี่ยนเป็นพิมพ์ใหญ่ หากไม่ใช่ตัวอักษรภาษาอังกฤษให้คงเดิมไว้"
    },
    "aff_first_vowel": {
        "en": "Write a program that takes a string as an argument and displays the FIRST vowel it encounters ('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'), followed by a newline.\nIf no vowel is found, or if the number of arguments is not 1, just display a newline.",
        "th": "เขียนโปรแกรมที่รับสตริงและแสดงผล 'สระ' ตัวแรกที่พบ (a, e, i, o, u ทั้งพิมพ์เล็กและพิมพ์ใหญ่) ตามด้วยบรรทัดใหม่\nหากไม่พบสระเลย หรือส่งอาร์กิวเมนต์ผิดจำนวน ให้แสดงแค่บรรทัดใหม่"
    },
    "ft_strchr": {
        "en": "Write a function that locates the first occurrence of the character 'c' (converted to a char) in the string 's'.\nThe terminating null byte is considered part of the string.\nIt returns a pointer to the matched character or NULL if the character is not found.",
        "th": "เขียนฟังก์ชันเพื่อหาตำแหน่งแรกของตัวอักษร 'c' ในสตริง 's'\nให้นับรวม null terminator ('\\0') เป็นส่วนหนึ่งของสตริงด้วย\nฟังก์ชันต้องคืนค่า pointer ที่ชี้ไปยังตัวอักษรที่พบ หรือคืนค่า NULL หากไม่พบ"
    },
    "ft_strrchr": {
        "en": "Write a function that locates the LAST occurrence of the character 'c' (converted to a char) in the string 's'.\nThe terminating null byte is considered part of the string.\nIt returns a pointer to the matched character or NULL if the character is not found.",
        "th": "เขียนฟังก์ชันเพื่อหาตำแหน่ง *สุดท้าย* ของตัวอักษร 'c' ในสตริง 's'\nฟังก์ชันต้องคืนค่า pointer ที่ชี้ไปยังตัวอักษรที่พบ หรือคืนค่า NULL หากไม่พบ"
    },
    "ft_is_palindrome": {
        "en": "Write a program that takes a string as an argument and checks if it is a palindrome (reads the same backwards and forwards).\nIf it is, print '1' followed by a newline. If it is not, print '0' followed by a newline.\nIf the number of arguments is not 1, print a newline.",
        "th": "เขียนโปรแกรมตรวจสอบว่าสตริงเป็นพาลินโดรมหรือไม่ (อ่านจากหน้าไปหลังและหลังไปหน้าได้เหมือนกัน)\nหากใช่ให้พิมพ์ '1' ตามด้วยบรรทัดใหม่ หากไม่ใช่ให้พิมพ์ '0'\nหากอาร์กิวเมนต์ไม่ใช่ 1 ตัว ให้พิมพ์แค่บรรทัดใหม่"
    },
    "rot_n": {
        "en": "Write a program that takes a string and rotates all alphabetical characters by N positions in the alphabet.\nUppercase letters remain uppercase, and lowercase letters remain lowercase. Non-alphabetical characters remain unchanged.",
        "th": "เขียนโปรแกรมที่รับสตริงและหมุนตัวอักษรภาษาอังกฤษไป N ตำแหน่ง (แบบ Caesar Cipher)\nตัวพิมพ์เล็ก/ใหญ่ต้องคงสถานะเดิม ตัวอักษรที่ไม่ใช่ภาษาอังกฤษห้ามเปลี่ยนแปลง"
    },
    "clean_spaces": {
        "en": "Write a program that takes a string and displays it with exactly one space between words, with no leading or trailing spaces.\nA word is a section of characters delimited by spaces or tabs.",
        "th": "เขียนโปรแกรมที่รับสตริงและลบช่องว่างส่วนเกินออก ให้เหลือช่องว่างแค่ 1 เคาะระหว่างคำ และห้ามมีช่องว่างที่หัวหรือท้ายประโยค"
    },
    "ft_isupper": {
        "en": "Write a function that checks if a character is an uppercase letter ('A' to 'Z').\nReturn 1 if true, 0 if false.",
        "th": "เขียนฟังก์ชันตรวจสอบว่าตัวอักษรเป็นตัวพิมพ์ใหญ่ ('A' ถึง 'Z') หรือไม่ คืนค่า 1 หากใช่ คืน 0 หากไม่ใช่"
    },
    "ft_islower": {
        "en": "Write a function that checks if a character is a lowercase letter ('a' to 'z').\nReturn 1 if true, 0 if false.",
        "th": "เขียนฟังก์ชันตรวจสอบว่าตัวอักษรเป็นตัวพิมพ์เล็ก ('a' ถึง 'z') หรือไม่ คืนค่า 1 หากใช่ คืน 0 หากไม่ใช่"
    },
    "ft_isalpha": {
        "en": "Write a function that checks if a character is an alphabetic letter (either upper or lowercase).\nReturn 1 if true, 0 if false.",
        "th": "เขียนฟังก์ชันตรวจสอบว่าตัวอักษรเป็นภาษาอังกฤษหรือไม่ คืนค่า 1 หากใช่ คืน 0 หากไม่ใช่"
    },
    "ft_isalnum": {
        "en": "Write a function that checks if a character is alphanumeric (a letter or a digit).\nReturn 1 if true, 0 if false.",
        "th": "เขียนฟังก์ชันตรวจสอบว่าตัวอักษรเป็นตัวอักษรภาษาอังกฤษหรือตัวเลขหรือไม่ คืนค่า 1 หากใช่ คืน 0 หากไม่ใช่"
    },
    "ft_isprint": {
        "en": "Write a function that checks if a character is printable (including space).\nReturn 1 if true, 0 if false.",
        "th": "เขียนฟังก์ชันตรวจสอบว่าตัวอักษรสามารถพิมพ์ออกมาให้เห็นได้หรือไม่ (รวมถึง space) คืนค่า 1 หากใช่ คืน 0 หากไม่ใช่"
    },
    "count_vowels": {
        "en": "Write a program that takes a string and counts the total number of vowels in it.\nIt should print the integer count followed by a newline.",
        "th": "เขียนโปรแกรมนับจำนวนสระทั้งหมดในสตริง (a,e,i,o,u) และพิมพ์ตัวเลขจำนวนรวมออกมาตามด้วยบรรทัดใหม่"
    }
}
