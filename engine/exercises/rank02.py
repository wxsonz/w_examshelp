"""Exam Rank 02 pool -- levels 0 to 2.

Each entry states its output format exactly, because the grader compares bytes.
Where the circulating versions of a subject disagree (aff_a is the classic case),
this pack picks one reading and states it unambiguously; the reference solution
implements that reading, and the tests are generated from it.
"""

from engine.exercises.spec import ex, ADDED, PROGRAM, FUNCTION

EXERCISES = [
    # ------------------------------------------------------------------ level 0
    ex(
        name="hello",
        exams={"exam_01": 1},
        kind=PROGRAM,
        allowed=["write"],
        subject="""
Write a program that displays

  Hello World!

followed by a newline.

Your program takes no arguments; any it receives are ignored.
""",
        subject_th="""
เขียนโปรแกรมที่แสดงข้อความ

  Hello World!

แล้วขึ้นบรรทัดใหม่

โปรแกรมนี้ไม่รับอาร์กิวเมนต์ หากมีอาร์กิวเมนต์ส่งเข้ามาให้ละเว้นทั้งหมด
""",
        reference="""
#include <unistd.h>

int	main(void)
{
	write(1, "Hello World!\\n", 13);
	return (0);
}
""",
        tests=[[], ["ignored"]],
        hints=[
            "write(1, s, n) sends n bytes of s to standard output.",
            "Count the bytes including the '\\n' -- \"Hello World!\\n\" is 13.",
        ],
    ),
    ex(
        name="aff_a",
        exams={"exam_01": 0},
        kind=PROGRAM,
        allowed=["write"],
        subject="""
Write a program that takes a string and displays the first 'a' character it
encounters in it, followed by a newline.

If there are no 'a' characters in the string, the program just writes a newline.
If the number of parameters is not 1, the program displays 'a' followed by a
newline.

Examples:

  $> ./aff_a "abc" | cat -e
  a$
  $> ./aff_a "dubO a POIL" | cat -e
  a$
  $> ./aff_a "zz sent le poney" | cat -e
  $
  $> ./aff_a | cat -e
  a$
""",
        subject_th="""
เขียนโปรแกรมที่รับข้อความหนึ่งชุด แล้วแสดงตัวอักษร 'a' ตัวแรกที่พบในข้อความนั้น
ตามด้วยการขึ้นบรรทัดใหม่

ถ้าในข้อความไม่มีตัวอักษร 'a' ให้แสดงเฉพาะการขึ้นบรรทัดใหม่
แต่ถ้าจำนวนอาร์กิวเมนต์ไม่เท่ากับ 1 ให้แสดงตัวอักษร 'a' ตามด้วยการขึ้นบรรทัดใหม่

ตัวอย่าง:

  $> ./aff_a "abc" | cat -e
  a$
  $> ./aff_a "dubO a POIL" | cat -e
  a$
  $> ./aff_a "zz sent le poney" | cat -e
  $
  $> ./aff_a | cat -e
  a$
""",
        reference="""
#include <unistd.h>

int	main(int argc, char **argv)
{
	int	i;

	if (argc != 2)
	{
		write(1, "a\\n", 2);
		return (0);
	}
	i = 0;
	while (argv[1][i])
	{
		if (argv[1][i] == 'a')
		{
			write(1, "a\\n", 2);
			return (0);
		}
		i++;
	}
	write(1, "\\n", 1);
	return (0);
}
""",
        tests=[
            ["abc"],
            ["dubO a POIL"],
            ["zz sent le poney"],
            [],
            ["banana"],
            [""],
            ["one", "two"],
            ["ZZZaZZ"],
        ],
        hints=[
            "Read the two failure cases carefully: they do NOT behave the same.",
            "No 'a' in the string writes only a newline, but a wrong argument count "
            "writes 'a' first.",
            "Stop at the FIRST 'a' -- do not keep scanning once you have written it.",
        ],
    ),
    ex(
        name="aff_z",
        exams={"exam_01": 2},
        kind=PROGRAM,
        allowed=["write"],
        subject="""
Write a program that takes a string and displays the first 'z' character it
encounters in it, followed by a newline.

If there are no 'z' characters in the string, the program writes 'z' followed by
a newline. If the number of parameters is not 1, the program displays 'z'
followed by a newline.

Examples:

  $> ./aff_z "abc" | cat -e
  z$
  $> ./aff_z "dubO a POIL" | cat -e
  z$
  $> ./aff_z "zaz sent le poney" | cat -e
  z$
  $> ./aff_z | cat -e
  z$
""",
        subject_th="""
เขียนโปรแกรมที่รับข้อความหนึ่งชุด แล้วแสดงตัวอักษร 'z' ตัวแรกที่พบในข้อความนั้น
ตามด้วยการขึ้นบรรทัดใหม่

ถ้าในข้อความไม่มีตัวอักษร 'z' ให้แสดงตัวอักษร 'z' ตามด้วยการขึ้นบรรทัดใหม่
และถ้าจำนวนอาร์กิวเมนต์ไม่เท่ากับ 1 ก็ให้แสดงตัวอักษร 'z'
ตามด้วยการขึ้นบรรทัดใหม่เช่นกัน

ตัวอย่าง:

  $> ./aff_z "abc" | cat -e
  z$
  $> ./aff_z "dubO a POIL" | cat -e
  z$
  $> ./aff_z "zaz sent le poney" | cat -e
  z$
  $> ./aff_z | cat -e
  z$
""",
        reference="""
#include <unistd.h>

int	main(int argc, char **argv)
{
	int	i;

	if (argc == 2)
	{
		i = 0;
		while (argv[1][i])
		{
			if (argv[1][i] == 'z')
			{
				write(1, "z\\n", 2);
				return (0);
			}
			i++;
		}
	}
	write(1, "z\\n", 2);
	return (0);
}
""",
        tests=[
            ["abc"],
            ["dubO a POIL"],
            ["zaz sent le poney"],
            [],
            ["zzz"],
            [""],
            ["a", "b"],
        ],
        hints=[
            "Read every branch before you write code: the character printed is 'z' "
            "in all three of them.",
            "That means the output never actually varies -- which is the joke of "
            "this exercise, and it is easy to over-think.",
            "It looks like aff_a but it is NOT: aff_a's no-match case prints only a "
            "newline.",
        ],
    ),
    ex(
        name="ft_countdown",
        exams={"exam_01": 0},
        kind=PROGRAM,
        allowed=["write"],
        subject="""
Write a program that displays all digits in descending order, followed by a
newline.

Example:

  $> ./ft_countdown | cat -e
  9876543210$
""",
        subject_th="""
เขียนโปรแกรมที่แสดงตัวเลขทั้งหมดเรียงจากมากไปน้อย ตามด้วยการขึ้นบรรทัดใหม่

ตัวอย่าง:

  $> ./ft_countdown | cat -e
  9876543210$
""",
        reference="""
#include <unistd.h>

int	main(void)
{
	char	c;

	c = '9';
	while (c >= '0')
	{
		write(1, &c, 1);
		c--;
	}
	write(1, "\\n", 1);
	return (0);
}
""",
        tests=[[]],
        hints=[
            "write() sends characters, not integers: '9' is the character, 9 is the number.",
            "You can add '0' to a digit to get its character, or just loop over char values.",
        ],
    ),
    ex(
        name="ft_print_numbers",
        exams={"exam_01": 0},
        kind=FUNCTION,
        allowed=["write"],
        prototype="void ft_print_numbers(void);",
        subject="""
Write a function that displays all digits from 0 to 9 in ascending order, with no
separator between them, followed by a newline.

Expected output:

  $> ./a.out | cat -e
  0123456789$
""",
        subject_th="""
เขียนฟังก์ชันที่แสดงตัวเลขทั้งหมดจาก 0 ถึง 9 เรียงจากน้อยไปมาก
โดยไม่มีตัวคั่นระหว่างตัวเลข แล้วขึ้นบรรทัดใหม่

ผลลัพธ์ที่ต้องได้:

  $> ./a.out | cat -e
  0123456789$
""",
        reference="""
#include <unistd.h>

void	ft_print_numbers(void)
{
	char	c;

	c = '0';
	while (c <= '9')
	{
		write(1, &c, 1);
		c++;
	}
	write(1, "\\n", 1);
}
""",
        harness="""
void	ft_print_numbers(void);

int	main(void)
{
	ft_print_numbers();
	return (0);
}
""",
        tests=[[]],
        hints=["The mirror image of ft_countdown."],
    ),
    ex(
        name="ft_putchar",
        exams={"exam_01": 0},
        source=ADDED,
        kind=FUNCTION,
        allowed=["write"],
        prototype="void ft_putchar(char c);",
        subject="""
Write a function that displays the character passed as argument. It writes
exactly one byte and adds no newline.
""",
        subject_th="""
เขียนฟังก์ชันที่แสดงตัวอักษรที่รับเข้ามาเป็นอาร์กิวเมนต์
โดยเขียนออกเพียง 1 ไบต์ และไม่ต้องขึ้นบรรทัดใหม่
""",
        reference="""
#include <unistd.h>

void	ft_putchar(char c)
{
	write(1, &c, 1);
}
""",
        harness="""
#include <unistd.h>

void	ft_putchar(char c);

int	main(int argc, char **argv)
{
	int	i;

	i = 1;
	while (i < argc)
	{
		if (argv[i][0])
			ft_putchar(argv[i][0]);
		i++;
	}
	write(1, "\\n", 1);
	return (0);
}
""",
        tests=[["A"], ["z"], ["4"], ["a", "b", "c"], ["!"]],
        hints=[
            "write() needs an ADDRESS, so pass &c, not c.",
            "One byte only -- no newline of your own.",
        ],
    ),
    ex(
        name="is_negative",
        exams={"exam_01": 1},
        source=ADDED,
        kind=FUNCTION,
        allowed=["write"],
        prototype="void is_negative(int n);",
        subject="""
Write a function that displays 'N' if the integer passed as argument is negative,
and 'P' if it is positive or zero. The character is followed by a newline.

Examples:

  is_negative(-42)  ->  N
  is_negative(0)    ->  P
  is_negative(42)   ->  P
""",
        subject_th="""
เขียนฟังก์ชันที่แสดงตัวอักษร 'N' ถ้าจำนวนเต็มที่รับเข้ามาเป็นค่าลบ
และแสดง 'P' ถ้าเป็นค่าบวกหรือศูนย์ ตามด้วยการขึ้นบรรทัดใหม่

ตัวอย่าง:

  is_negative(-42)  ->  N
  is_negative(0)    ->  P
  is_negative(42)   ->  P
""",
        reference="""
#include <unistd.h>

void	is_negative(int n)
{
	if (n < 0)
		write(1, "N\\n", 2);
	else
		write(1, "P\\n", 2);
}
""",
        harness="""
#include <stdlib.h>

void	is_negative(int n);

int	main(int argc, char **argv)
{
	int	i;

	i = 1;
	while (i < argc)
	{
		is_negative(atoi(argv[i]));
		i++;
	}
	return (0);
}
""",
        tests=[["-42"], ["0"], ["42"], ["-1", "0", "1"], ["-2147483648"]],
        hints=["Zero counts as positive here -- test n < 0, not n <= 0."],
    ),
    ex(
        name="ft_swap",
        exams={"exam_01": 6, "exam_02": 2},
        kind=FUNCTION,
        allowed=[],
        prototype="void ft_swap(int *a, int *b);",
        subject="""
Write a function that swaps the values of the two integers pointed to by its
arguments.
""",
        subject_th="""
เขียนฟังก์ชันที่สลับค่าของจำนวนเต็มสองตัวที่พอยน์เตอร์ทั้งสองชี้อยู่
""",
        reference="""
void	ft_swap(int *a, int *b)
{
	int	tmp;

	tmp = *a;
	*a = *b;
	*b = tmp;
}
""",
        harness="""
#include <stdio.h>
#include <stdlib.h>

void	ft_swap(int *a, int *b);

int	main(int argc, char **argv)
{
	int	a;
	int	b;

	if (argc != 3)
		return (0);
	a = atoi(argv[1]);
	b = atoi(argv[2]);
	ft_swap(&a, &b);
	printf("%d %d\\n", a, b);
	return (0);
}
""",
        tests=[["1", "2"], ["-5", "5"], ["0", "0"], ["42", "-42"]],
        hints=[
            "You need a third variable to hold one value while you overwrite it.",
            "Dereference with * to read and write through the pointers.",
        ],
    ),
    ex(
        name="ft_strlen",
        exams={"exam_01": 4, "exam_02": 0},
        kind=FUNCTION,
        allowed=[],
        prototype="int ft_strlen(char *str);",
        subject="""
Write a function that counts and returns the number of characters in a string,
not counting the terminating null byte.
""",
        subject_th="""
เขียนฟังก์ชันที่นับและคืนค่าจำนวนตัวอักษรในข้อความ
โดยไม่นับไบต์ null ที่ปิดท้ายข้อความ
""",
        reference="""
int	ft_strlen(char *str)
{
	int	i;

	i = 0;
	while (str[i])
		i++;
	return (i);
}
""",
        harness="""
#include <stdio.h>

int	ft_strlen(char *str);

int	main(int argc, char **argv)
{
	int	i;

	i = 1;
	while (i < argc)
	{
		printf("%d\\n", ft_strlen(argv[i]));
		i++;
	}
	return (0);
}
""",
        tests=[["hello"], [""], ["a"], ["hello world"], ["42born2code"]],
        hints=[
            "Stop when you reach '\\0'. Do not count it.",
            "An empty string has length 0.",
        ],
    ),
    # ------------------------------------------------------------------ level 1
    ex(
        name="ft_strcpy",
        exams={"exam_01": 4, "exam_02": 0},
        kind=FUNCTION,
        allowed=[],
        prototype="char *ft_strcpy(char *s1, char *s2);",
        subject="""
Reproduce the behaviour of strcpy: copy the string s2, including its terminating
null byte, into the buffer s1. Return s1.

You may assume s1 is large enough to hold s2.
""",
        subject_th="""
เขียนฟังก์ชันที่ทำงานเหมือน strcpy: คัดลอกข้อความ s2 รวมไบต์ null ที่ปิดท้าย
ไปไว้ในบัฟเฟอร์ s1 แล้วคืนค่า s1

สามารถสมมติได้ว่า s1 มีขนาดใหญ่พอที่จะเก็บ s2 ได้
""",
        reference="""
char	*ft_strcpy(char *s1, char *s2)
{
	int	i;

	i = 0;
	while (s2[i])
	{
		s1[i] = s2[i];
		i++;
	}
	s1[i] = '\\0';
	return (s1);
}
""",
        harness="""
#include <stdio.h>

char	*ft_strcpy(char *s1, char *s2);

int	main(int argc, char **argv)
{
	char	buffer[1024];
	int		i;

	i = 1;
	while (i < argc)
	{
		buffer[0] = 'X';
		printf("[%s]\\n", ft_strcpy(buffer, argv[i]));
		i++;
	}
	return (0);
}
""",
        tests=[["hello"], [""], ["42"], ["a longer string here"]],
        hints=[
            "Do not forget to write the terminating '\\0' -- the loop condition skips it.",
            "Return s1, the destination, not s2.",
        ],
    ),
    ex(
        name="first_word",
        exams={"exam_01": 6, "exam_02": 2},
        kind=PROGRAM,
        allowed=["write"],
        subject="""
Write a program that takes a string and displays its first word, followed by a
newline.

A word is a sequence of characters that are neither spaces nor tabs. Leading
whitespace is skipped.

If the number of arguments is not 1, or if the string contains no word, the
program writes only a newline.

Examples:

  $> ./first_word "hello world" | cat -e
  hello$
  $> ./first_word "   lorem,ipsum  " | cat -e
  lorem,ipsum$
  $> ./first_word "   " | cat -e
  $
""",
        subject_th="""
เขียนโปรแกรมที่รับข้อความหนึ่งชุด แล้วแสดงคำแรกของข้อความนั้น ตามด้วยการขึ้นบรรทัดใหม่

คำ หมายถึงลำดับของตัวอักษรที่ไม่ใช่ช่องว่างและไม่ใช่แท็บ โดยข้ามช่องว่างที่นำหน้าไป

ถ้าจำนวนอาร์กิวเมนต์ไม่เท่ากับ 1 หรือในข้อความไม่มีคำใดเลย
ให้แสดงเฉพาะการขึ้นบรรทัดใหม่

ตัวอย่าง:

  $> ./first_word "hello world" | cat -e
  hello$
  $> ./first_word "   lorem,ipsum  " | cat -e
  lorem,ipsum$
  $> ./first_word "   " | cat -e
  $
""",
        reference="""
#include <unistd.h>

int	main(int argc, char **argv)
{
	int	i;

	if (argc == 2)
	{
		i = 0;
		while (argv[1][i] == ' ' || argv[1][i] == '\\t')
			i++;
		while (argv[1][i] && argv[1][i] != ' ' && argv[1][i] != '\\t')
		{
			write(1, &argv[1][i], 1);
			i++;
		}
	}
	write(1, "\\n", 1);
	return (0);
}
""",
        tests=[
            ["hello world"],
            ["   lorem,ipsum  "],
            ["   "],
            [""],
            ["single"],
            ["\ttabbed word"],
            [],
            ["a", "b"],
        ],
        hints=[
            "Two loops: one to skip the leading whitespace, one to print the word.",
            "Tabs count as whitespace, not just spaces.",
        ],
    ),
    ex(
        name="last_word",
        exams={"exam_02": 5, "exam_03": 0},
        kind=PROGRAM,
        allowed=["write"],
        subject="""
Write a program that takes a string and displays its last word, followed by a
newline.

A word is a sequence of characters that are neither spaces nor tabs. Trailing
whitespace is ignored.

If the number of arguments is not 1, or if the string contains no word, the
program writes only a newline.

Examples:

  $> ./last_word "hello world" | cat -e
  world$
  $> ./last_word "   lorem,ipsum  " | cat -e
  lorem,ipsum$
""",
        subject_th="""
เขียนโปรแกรมที่รับข้อความหนึ่งชุด แล้วแสดงคำสุดท้ายของข้อความนั้น
ตามด้วยการขึ้นบรรทัดใหม่

คำ หมายถึงลำดับของตัวอักษรที่ไม่ใช่ช่องว่างและไม่ใช่แท็บ โดยละเว้นช่องว่างที่ต่อท้าย

ถ้าจำนวนอาร์กิวเมนต์ไม่เท่ากับ 1 หรือในข้อความไม่มีคำใดเลย
ให้แสดงเฉพาะการขึ้นบรรทัดใหม่

ตัวอย่าง:

  $> ./last_word "hello world" | cat -e
  world$
  $> ./last_word "   lorem,ipsum  " | cat -e
  lorem,ipsum$
""",
        reference="""
#include <unistd.h>

int	main(int argc, char **argv)
{
	int	i;
	int	end;

	if (argc == 2)
	{
		i = 0;
		while (argv[1][i])
			i++;
		i--;
		while (i >= 0 && (argv[1][i] == ' ' || argv[1][i] == '\\t'))
			i--;
		end = i;
		while (i >= 0 && argv[1][i] != ' ' && argv[1][i] != '\\t')
			i--;
		i++;
		while (i <= end)
		{
			write(1, &argv[1][i], 1);
			i++;
		}
	}
	write(1, "\\n", 1);
	return (0);
}
""",
        tests=[
            ["hello world"],
            ["   lorem,ipsum  "],
            ["   "],
            [""],
            ["single"],
            ["a b\tc"],
            [],
        ],
        hints=[
            "Walk backwards from the end: skip trailing whitespace first, then find the start of the word.",
            "Guard your index against going below 0 on an all-whitespace string.",
        ],
    ),
    ex(
        name="rev_print",
        exams={"exam_01": 7, "exam_02": 3},
        kind=PROGRAM,
        allowed=["write"],
        subject="""
Write a program that takes a string and displays it in reverse, followed by a
newline.

If the number of arguments is not 1, the program writes only a newline.

Examples:

  $> ./rev_print "zonx" | cat -e
  xnoz$
  $> ./rev_print | cat -e
  $
""",
        subject_th="""
เขียนโปรแกรมที่รับข้อความหนึ่งชุด แล้วแสดงข้อความนั้นกลับหลัง
ตามด้วยการขึ้นบรรทัดใหม่

ถ้าจำนวนอาร์กิวเมนต์ไม่เท่ากับ 1 ให้แสดงเฉพาะการขึ้นบรรทัดใหม่

ตัวอย่าง:

  $> ./rev_print "zonx" | cat -e
  xnoz$
  $> ./rev_print | cat -e
  $
""",
        reference="""
#include <unistd.h>

int	main(int argc, char **argv)
{
	int	i;

	if (argc == 2)
	{
		i = 0;
		while (argv[1][i])
			i++;
		i--;
		while (i >= 0)
		{
			write(1, &argv[1][i], 1);
			i--;
		}
	}
	write(1, "\\n", 1);
	return (0);
}
""",
        tests=[["zonx"], ["hello world"], [""], ["a"], []],
        hints=[
            "Find the length first, then walk the index back down to 0.",
            "The last character sits at index len - 1, not len.",
        ],
    ),
    ex(
        name="repeat_alpha",
        exams={"exam_01": 5, "exam_02": 0},
        kind=PROGRAM,
        allowed=["write"],
        subject="""
Write a program that takes a string and repeats each alphabetical character as
many times as its position in the alphabet. Other characters are printed once,
unchanged. The result is followed by a newline.

Case is preserved: 'b' becomes "bb", 'C' becomes "CCC".

If the number of arguments is not 1, the program writes only a newline.

Examples:

  $> ./repeat_alpha "abc" | cat -e
  abbccc$
  $> ./repeat_alpha "Alex." | cat -e
  Alllllllllllleeeeexxxxxxxxxxxxxxxxxxxxxxxx.$
""",
        subject_th="""
เขียนโปรแกรมที่รับข้อความหนึ่งชุด แล้วแสดงตัวอักษรภาษาอังกฤษแต่ละตัวซ้ำ
เท่ากับลำดับของตัวอักษรนั้นในผังตัวอักษร ตัวอักษรอื่นให้แสดงหนึ่งครั้งตามเดิม
จากนั้นขึ้นบรรทัดใหม่

ตัวพิมพ์เล็กพิมพ์ใหญ่คงเดิม: 'b' กลายเป็น "bb" และ 'C' กลายเป็น "CCC"

ถ้าจำนวนอาร์กิวเมนต์ไม่เท่ากับ 1 ให้แสดงเฉพาะการขึ้นบรรทัดใหม่

ตัวอย่าง:

  $> ./repeat_alpha "abc" | cat -e
  abbccc$
  $> ./repeat_alpha "Alex." | cat -e
  Alllllllllllleeeeexxxxxxxxxxxxxxxxxxxxxxxx.$
""",
        reference="""
#include <unistd.h>

static int	alpha_rank(char c)
{
	if (c >= 'a' && c <= 'z')
		return (c - 'a' + 1);
	if (c >= 'A' && c <= 'Z')
		return (c - 'A' + 1);
	return (1);
}

int	main(int argc, char **argv)
{
	int	i;
	int	n;

	if (argc == 2)
	{
		i = 0;
		while (argv[1][i])
		{
			n = alpha_rank(argv[1][i]);
			while (n-- > 0)
				write(1, &argv[1][i], 1);
			i++;
		}
	}
	write(1, "\\n", 1);
	return (0);
}
""",
        tests=[["abc"], ["Alex."], [""], ["a"], ["Zz"], ["42!"], []],
        hints=[
            "c - 'a' + 1 gives the position of a lowercase letter in the alphabet.",
            "Non-alphabetical characters are printed exactly once, not zero times.",
        ],
    ),
    ex(
        name="rotone",
        exams={"exam_01": 7, "exam_02": 3},
        kind=PROGRAM,
        allowed=["write"],
        subject="""
Write a program that takes a string and displays it with each alphabetical
character shifted forward by one letter, followed by a newline.

'z' wraps around to 'a' and 'Z' to 'A'. Non-alphabetical characters are left
unchanged.

If the number of arguments is not 1, the program writes only a newline.

Examples:

  $> ./rotone "abc" | cat -e
  bcd$
  $> ./rotone "Zz!" | cat -e
  Aa!$
""",
        subject_th="""
เขียนโปรแกรมที่รับข้อความหนึ่งชุด แล้วแสดงข้อความนั้นโดยเลื่อนตัวอักษรภาษาอังกฤษ
ไปข้างหน้าหนึ่งตำแหน่ง ตามด้วยการขึ้นบรรทัดใหม่

ตัวอักษร 'z' จะวนกลับไปเป็น 'a' และ 'Z' วนกลับไปเป็น 'A'
ตัวอักษรที่ไม่ใช่ตัวอักษรภาษาอังกฤษให้คงไว้ตามเดิม

ถ้าจำนวนอาร์กิวเมนต์ไม่เท่ากับ 1 ให้แสดงเฉพาะการขึ้นบรรทัดใหม่

ตัวอย่าง:

  $> ./rotone "abc" | cat -e
  bcd$
  $> ./rotone "Zz!" | cat -e
  Aa!$
""",
        reference="""
#include <unistd.h>

int	main(int argc, char **argv)
{
	int		i;
	char	c;

	if (argc == 2)
	{
		i = 0;
		while (argv[1][i])
		{
			c = argv[1][i];
			if (c == 'z')
				c = 'a';
			else if (c == 'Z')
				c = 'A';
			else if ((c >= 'a' && c < 'z') || (c >= 'A' && c < 'Z'))
				c = c + 1;
			write(1, &c, 1);
			i++;
		}
	}
	write(1, "\\n", 1);
	return (0);
}
""",
        tests=[["abc"], ["Zz!"], [""], ["Hello World"], ["42"], []],
        hints=[
            "Handle the wrap cases 'z' and 'Z' before the generic +1 case.",
            "Digits, spaces and punctuation pass through untouched.",
        ],
    ),
    ex(
        name="rot_13",
        exams={"exam_01": 7, "exam_02": 3},
        kind=PROGRAM,
        allowed=["write"],
        subject="""
Write a program that takes a string and displays it with each alphabetical
character shifted forward by 13 letters, wrapping around within its own case,
followed by a newline.

Non-alphabetical characters are left unchanged.

If the number of arguments is not 1, the program writes only a newline.

Examples:

  $> ./rot_13 "abc" | cat -e
  nop$
  $> ./rot_13 "My horse is Amazing." | cat -e
  Zl ubefr vf Nznmvat.$
""",
        subject_th="""
เขียนโปรแกรมที่รับข้อความหนึ่งชุด แล้วแสดงข้อความนั้นโดยเลื่อนตัวอักษรภาษาอังกฤษ
ไปข้างหน้า 13 ตำแหน่ง และวนกลับภายในกลุ่มตัวพิมพ์เดียวกัน
ตามด้วยการขึ้นบรรทัดใหม่

ตัวอักษรที่ไม่ใช่ตัวอักษรภาษาอังกฤษให้คงไว้ตามเดิม

ถ้าจำนวนอาร์กิวเมนต์ไม่เท่ากับ 1 ให้แสดงเฉพาะการขึ้นบรรทัดใหม่

ตัวอย่าง:

  $> ./rot_13 "abc" | cat -e
  nop$
  $> ./rot_13 "My horse is Amazing." | cat -e
  Zl ubefr vf Nznmvat.$
""",
        reference="""
#include <unistd.h>

int	main(int argc, char **argv)
{
	int		i;
	char	c;

	if (argc == 2)
	{
		i = 0;
		while (argv[1][i])
		{
			c = argv[1][i];
			if (c >= 'a' && c <= 'z')
				c = 'a' + (c - 'a' + 13) % 26;
			else if (c >= 'A' && c <= 'Z')
				c = 'A' + (c - 'A' + 13) % 26;
			write(1, &c, 1);
			i++;
		}
	}
	write(1, "\\n", 1);
	return (0);
}
""",
        tests=[["abc"], ["My horse is Amazing."], [""], ["nop"], ["Zz"], []],
        hints=[
            "The modulo trick: 'a' + (c - 'a' + 13) % 26 keeps you inside the alphabet.",
            "Uppercase and lowercase wrap separately.",
        ],
    ),
    ex(
        name="ulstr",
        exams={"exam_01": 5, "exam_02": 1},
        kind=PROGRAM,
        allowed=["write"],
        subject="""
Write a program that takes a string and displays it with the case of every
alphabetical character inverted, followed by a newline.

Non-alphabetical characters are left unchanged.

If the number of arguments is not 1, the program writes only a newline.

Example:

  $> ./ulstr "Hello World! 42" | cat -e
  hELLO wORLD! 42$
""",
        subject_th="""
เขียนโปรแกรมที่รับข้อความหนึ่งชุด แล้วแสดงข้อความนั้นโดยสลับตัวพิมพ์เล็กพิมพ์ใหญ่
ของตัวอักษรภาษาอังกฤษทุกตัว ตามด้วยการขึ้นบรรทัดใหม่

ตัวอักษรที่ไม่ใช่ตัวอักษรภาษาอังกฤษให้คงไว้ตามเดิม

ถ้าจำนวนอาร์กิวเมนต์ไม่เท่ากับ 1 ให้แสดงเฉพาะการขึ้นบรรทัดใหม่

ตัวอย่าง:

  $> ./ulstr "Hello World! 42" | cat -e
  hELLO wORLD! 42$
""",
        reference="""
#include <unistd.h>

int	main(int argc, char **argv)
{
	int		i;
	char	c;

	if (argc == 2)
	{
		i = 0;
		while (argv[1][i])
		{
			c = argv[1][i];
			if (c >= 'a' && c <= 'z')
				c = c - 32;
			else if (c >= 'A' && c <= 'Z')
				c = c + 32;
			write(1, &c, 1);
			i++;
		}
	}
	write(1, "\\n", 1);
	return (0);
}
""",
        tests=[["Hello World! 42"], [""], ["abc"], ["ABC"], ["123"], []],
        hints=[
            "'a' - 'A' is 32, so adding or subtracting 32 flips the case.",
            "Check the range before flipping, or you will corrupt digits and punctuation.",
        ],
    ),
    ex(
        name="alpha_mirror",
        exams={"exam_02": 6, "exam_03": 1},
        kind=PROGRAM,
        allowed=["write"],
        subject="""
Write a program that takes a string and displays it with every alphabetical
character replaced by its mirror image in the alphabet, followed by a newline.

'a' becomes 'z', 'b' becomes 'y', 'A' becomes 'Z', and so on. Case is preserved
and non-alphabetical characters are left unchanged.

If the number of arguments is not 1, the program writes only a newline.

Example:

  $> ./alpha_mirror "abc xyz." | cat -e
  zyx cba.$
""",
        subject_th="""
เขียนโปรแกรมที่รับข้อความหนึ่งชุด แล้วแสดงข้อความนั้นโดยแทนตัวอักษรภาษาอังกฤษ
ทุกตัวด้วยตัวอักษรที่อยู่ตรงข้ามกันในผังตัวอักษร ตามด้วยการขึ้นบรรทัดใหม่

'a' กลายเป็น 'z', 'b' กลายเป็น 'y', 'A' กลายเป็น 'Z' และเป็นเช่นนี้ต่อไป
โดยคงตัวพิมพ์เล็กพิมพ์ใหญ่ไว้ และตัวอักษรอื่นคงไว้ตามเดิม

ถ้าจำนวนอาร์กิวเมนต์ไม่เท่ากับ 1 ให้แสดงเฉพาะการขึ้นบรรทัดใหม่

ตัวอย่าง:

  $> ./alpha_mirror "abc xyz." | cat -e
  zyx cba.$
""",
        reference="""
#include <unistd.h>

int	main(int argc, char **argv)
{
	int		i;
	char	c;

	if (argc == 2)
	{
		i = 0;
		while (argv[1][i])
		{
			c = argv[1][i];
			if (c >= 'a' && c <= 'z')
				c = 'z' - (c - 'a');
			else if (c >= 'A' && c <= 'Z')
				c = 'Z' - (c - 'A');
			write(1, &c, 1);
			i++;
		}
	}
	write(1, "\\n", 1);
	return (0);
}
""",
        tests=[["abc xyz."], [""], ["aAzZ"], ["Hello"], []],
        hints=["'z' - (c - 'a') mirrors a lowercase letter."],
    ),
    ex(
        name="max",
        exams={"exam_02": 7, "exam_03": 1},
        kind=FUNCTION,
        allowed=[],
        prototype="int max(int *tab, unsigned int len);",
        subject="""
Write a function that returns the largest value in the array tab of len integers.

If len is 0, the function returns 0.
""",
        subject_th="""
เขียนฟังก์ชันที่คืนค่าจำนวนเต็มที่มีค่ามากที่สุดในอาเรย์ tab ซึ่งมีสมาชิก len ตัว

ถ้า len เท่ากับ 0 ให้คืนค่า 0
""",
        reference="""
int	max(int *tab, unsigned int len)
{
	unsigned int	i;
	int				best;

	if (len == 0)
		return (0);
	best = tab[0];
	i = 1;
	while (i < len)
	{
		if (tab[i] > best)
			best = tab[i];
		i++;
	}
	return (best);
}
""",
        harness="""
#include <stdio.h>
#include <stdlib.h>

int	max(int *tab, unsigned int len);

int	main(int argc, char **argv)
{
	int				tab[256];
	unsigned int	i;

	i = 0;
	while (i + 1 < (unsigned int)argc && i < 256)
	{
		tab[i] = atoi(argv[i + 1]);
		i++;
	}
	printf("%d\\n", max(tab, i));
	return (0);
}
""",
        tests=[
            ["1", "5", "3"],
            ["-10", "-2", "-7"],
            ["42"],
            [],
            ["0", "0", "0"],
            ["2147483647", "-2147483648"],
        ],
        hints=[
            "Start from tab[0], not from 0 -- otherwise an all-negative array returns 0.",
            "Handle len == 0 before you read tab[0].",
        ],
    ),
    ex(
        name="sort_int_tab",
        exams={"exam_04": 2},
        kind=FUNCTION,
        allowed=[],
        prototype="void sort_int_tab(int *tab, unsigned int size);",
        subject="""
Write a function that sorts the array tab of size integers into ascending order,
in place.
""",
        subject_th="""
เขียนฟังก์ชันที่เรียงลำดับสมาชิกในอาเรย์ tab ซึ่งมีสมาชิก size ตัว
จากน้อยไปมาก โดยเรียงในตัวอาเรย์เดิม
""",
        reference="""
void	sort_int_tab(int *tab, unsigned int size)
{
	unsigned int	i;
	int				tmp;

	if (size < 2)
		return ;
	i = 0;
	while (i + 1 < size)
	{
		if (tab[i] > tab[i + 1])
		{
			tmp = tab[i];
			tab[i] = tab[i + 1];
			tab[i + 1] = tmp;
			i = 0;
		}
		else
			i++;
	}
}
""",
        harness="""
#include <stdio.h>
#include <stdlib.h>

void	sort_int_tab(int *tab, unsigned int size);

int	main(int argc, char **argv)
{
	int				tab[256];
	unsigned int	i;
	unsigned int	size;

	size = 0;
	while (size + 1 < (unsigned int)argc && size < 256)
	{
		tab[size] = atoi(argv[size + 1]);
		size++;
	}
	sort_int_tab(tab, size);
	i = 0;
	while (i < size)
	{
		printf("%d", tab[i]);
		if (i + 1 < size)
			printf(" ");
		i++;
	}
	printf("\\n");
	return (0);
}
""",
        tests=[
            ["3", "1", "2"],
            ["5", "4", "3", "2", "1"],
            ["1"],
            [],
            ["-1", "5", "-10", "0"],
            ["2", "2", "1"],
        ],
        hints=[
            "size is unsigned: `i - 1` underflows to a huge number. Compare i + 1 < size instead.",
            "Any correct sort is fine -- bubble sort is plenty for the exam.",
        ],
    ),
    ex(
        name="print_bits",
        exams={"exam_02": 7, "exam_03": 1},
        kind=FUNCTION,
        allowed=["write"],
        prototype="void print_bits(unsigned char octet);",
        subject="""
Write a function that takes a byte and prints it in binary, most significant bit
first. It always prints exactly 8 characters and adds NO newline.

Example:

  print_bits(2)  ->  00000010
""",
        subject_th="""
เขียนฟังก์ชันที่รับข้อมูลขนาดหนึ่งไบต์ แล้วแสดงค่าในระบบเลขฐานสอง
เริ่มจากบิตที่มีนัยสำคัญมากที่สุด โดยแสดงครบ 8 ตัวอักษรเสมอ
และไม่ต้องขึ้นบรรทัดใหม่

ตัวอย่าง:

  print_bits(2)  ->  00000010
""",
        reference="""
#include <unistd.h>

void	print_bits(unsigned char octet)
{
	int		i;
	char	c;

	i = 7;
	while (i >= 0)
	{
		c = ((octet >> i) & 1) + '0';
		write(1, &c, 1);
		i--;
	}
}
""",
        harness="""
#include <stdio.h>
#include <stdlib.h>

void	print_bits(unsigned char octet);

int	main(int argc, char **argv)
{
	int	i;

	i = 1;
	while (i < argc)
	{
		print_bits((unsigned char)atoi(argv[i]));
		printf("\\n");
		i++;
	}
	return (0);
}
""",
        tests=[["2"], ["0"], ["255"], ["1"], ["128"], ["42"]],
        hints=[
            "Shift right by i and mask with & 1 to isolate one bit.",
            "Count i down from 7 to 0 so the most significant bit comes first.",
            "Add '0' to turn the bit into a printable character.",
        ],
    ),
    ex(
        name="reverse_bits",
        exams={"exam_02": 5, "exam_03": 0},
        kind=FUNCTION,
        allowed=[],
        prototype="unsigned char reverse_bits(unsigned char octet);",
        subject="""
Write a function that takes a byte and returns it with its bits in reverse order.

Example:

  reverse_bits(1)  ->  128   (00000001 becomes 10000000)
""",
        subject_th="""
เขียนฟังก์ชันที่รับข้อมูลขนาดหนึ่งไบต์ แล้วคืนค่าไบต์นั้นโดยกลับลำดับบิตทั้งหมด

ตัวอย่าง:

  reverse_bits(1)  ->  128   (00000001 กลายเป็น 10000000)
""",
        reference="""
unsigned char	reverse_bits(unsigned char octet)
{
	unsigned char	out;
	int				i;

	out = 0;
	i = 0;
	while (i < 8)
	{
		out = (out << 1) | ((octet >> i) & 1);
		i++;
	}
	return (out);
}
""",
        harness="""
#include <stdio.h>
#include <stdlib.h>

unsigned char	reverse_bits(unsigned char octet);

int	main(int argc, char **argv)
{
	int	i;

	i = 1;
	while (i < argc)
	{
		printf("%d\\n", reverse_bits((unsigned char)atoi(argv[i])));
		i++;
	}
	return (0);
}
""",
        tests=[["1"], ["0"], ["255"], ["2"], ["42"], ["128"]],
        hints=[
            "Build the result by shifting it left and pulling bits off the input right.",
            "Exactly 8 iterations -- one per bit.",
        ],
    ),
    ex(
        name="swap_bits",
        exams={"exam_02": 5, "exam_03": 0},
        kind=FUNCTION,
        allowed=[],
        prototype="unsigned char swap_bits(unsigned char octet);",
        subject="""
Write a function that takes a byte and returns it with its two halves (its two
nibbles of 4 bits) swapped.

Example:

  swap_bits(1)  ->  16   (00000001 becomes 00010000)
""",
        subject_th="""
เขียนฟังก์ชันที่รับข้อมูลขนาดหนึ่งไบต์ แล้วคืนค่าไบต์นั้นโดยสลับครึ่งบน
กับครึ่งล่าง (นิบเบิลขนาด 4 บิตทั้งสองส่วน)

ตัวอย่าง:

  swap_bits(1)  ->  16   (00000001 กลายเป็น 00010000)
""",
        reference="""
unsigned char	swap_bits(unsigned char octet)
{
	return ((octet >> 4) | (octet << 4));
}
""",
        harness="""
#include <stdio.h>
#include <stdlib.h>

unsigned char	swap_bits(unsigned char octet);

int	main(int argc, char **argv)
{
	int	i;

	i = 1;
	while (i < argc)
	{
		printf("%d\\n", swap_bits((unsigned char)atoi(argv[i])));
		i++;
	}
	return (0);
}
""",
        tests=[["1"], ["0"], ["255"], ["16"], ["170"], ["42"]],
        hints=[
            "One shift each way, then OR them together.",
            "Returning unsigned char truncates for you, so no mask is strictly needed.",
        ],
    ),
    ex(
        name="do_op",
        exams={"exam_02": 6, "exam_03": 1},
        kind=PROGRAM,
        allowed=["atoi", "printf", "write"],
        subject="""
Write a program that takes three arguments -- a number, an operator, and another
number -- and displays the result of the operation, followed by a newline.

The operators to handle are +, -, *, / and %.

If the number of arguments is not 3, the program writes only a newline.
You may assume the operator is always one of the five listed, and that division
and modulo by zero will not be tested.

Examples:

  $> ./do_op 42 "+" 21 | cat -e
  63$
  $> ./do_op 42 "/" 21 | cat -e
  2$
""",
        subject_th="""
เขียนโปรแกรมที่รับอาร์กิวเมนต์สามตัว คือ ตัวเลข ตัวดำเนินการ และตัวเลขอีกตัว
แล้วแสดงผลลัพธ์ของการดำเนินการนั้น ตามด้วยการขึ้นบรรทัดใหม่

ตัวดำเนินการที่ต้องรองรับคือ +, -, *, / และ %

ถ้าจำนวนอาร์กิวเมนต์ไม่เท่ากับ 3 ให้แสดงเฉพาะการขึ้นบรรทัดใหม่
สามารถสมมติได้ว่าตัวดำเนินการจะเป็นหนึ่งในห้าตัวนี้เสมอ
และจะไม่มีการทดสอบการหารหรือมอดุโลด้วยศูนย์

ตัวอย่าง:

  $> ./do_op 42 "+" 21 | cat -e
  63$
  $> ./do_op 42 "/" 21 | cat -e
  2$
""",
        reference="""
#include <stdio.h>
#include <stdlib.h>

int	main(int argc, char **argv)
{
	int		a;
	int		b;
	char	op;

	if (argc != 4)
	{
		printf("\\n");
		return (0);
	}
	a = atoi(argv[1]);
	b = atoi(argv[3]);
	op = argv[2][0];
	if (op == '+')
		printf("%d\\n", a + b);
	else if (op == '-')
		printf("%d\\n", a - b);
	else if (op == '*')
		printf("%d\\n", a * b);
	else if (op == '/')
		printf("%d\\n", a / b);
	else if (op == '%')
		printf("%d\\n", a % b);
	return (0);
}
""",
        tests=[
            ["42", "+", "21"],
            ["42", "-", "21"],
            ["42", "*", "21"],
            ["42", "/", "21"],
            ["42", "%", "21"],
            ["-3", "+", "8"],
            [],
            ["1", "+"],
        ],
        hints=[
            "argc is 4 when you receive 3 arguments -- argv[0] is the program name.",
            "The operator is a single character: use argv[2][0].",
        ],
    ),
    ex(
        name="fizzbuzz",
        exams={"exam_01": 7, "exam_02": 3},
        source=ADDED,
        kind=PROGRAM,
        allowed=["write"],
        subject="""
Write a program that prints the numbers from 1 to 100, each separated by a
newline.

If the number is a multiple of 3, it prints 'fizz' instead.

If the number is a multiple of 5, it prints 'buzz' instead.

If the number is both a multiple of 3 and a multiple of 5, it prints 'fizzbuzz'
instead.
""",
        subject_th="""
เขียนโปรแกรมที่แสดงตัวเลขจาก 1 ถึง 100 โดยคั่นแต่ละตัวด้วยการขึ้นบรรทัดใหม่

ถ้าตัวเลขเป็นพหุคูณของ 3 ให้แสดงคำว่า 'fizz' แทน

ถ้าตัวเลขเป็นพหุคูณของ 5 ให้แสดงคำว่า 'buzz' แทน

ถ้าตัวเลขเป็นพหุคูณของทั้ง 3 และ 5 ให้แสดงคำว่า 'fizzbuzz' แทน
""",
        reference="""
#include <unistd.h>

static void	put_nbr(int n)
{
	char	c;

	if (n >= 10)
		put_nbr(n / 10);
	c = (n % 10) + '0';
	write(1, &c, 1);
}

int	main(void)
{
	int	i;

	i = 1;
	while (i <= 100)
	{
		if (i % 15 == 0)
			write(1, "fizzbuzz", 8);
		else if (i % 3 == 0)
			write(1, "fizz", 4);
		else if (i % 5 == 0)
			write(1, "buzz", 4);
		else
			put_nbr(i);
		write(1, "\\n", 1);
		i++;
	}
	return (0);
}
""",
        tests=[[]],
        hints=[
            "Test the divisible-by-both case FIRST, or 15 prints 'fizz'.",
            "Divisible by both 3 and 5 means divisible by 15.",
            "Only write is allowed, so you need your own number printer -- printf "
            "is not available here.",
        ],
    ),
    # ------------------------------------------------------------------ level 2
    ex(
        name="ft_strcmp",
        exams={"exam_02": 6, "exam_03": 1},
        kind=FUNCTION,
        allowed=[],
        prototype="int ft_strcmp(char *s1, char *s2);",
        subject="""
Reproduce the behaviour of strcmp: compare the two strings and return the
difference between the first pair of bytes that differ, or 0 if the strings are
equal.

The comparison must treat the bytes as unsigned char values.
""",
        subject_th="""
เขียนฟังก์ชันที่ทำงานเหมือน strcmp: เปรียบเทียบข้อความสองชุด แล้วคืนค่าผลต่าง
ของไบต์คู่แรกที่ต่างกัน หรือคืนค่า 0 ถ้าข้อความทั้งสองเหมือนกัน

การเปรียบเทียบต้องมองไบต์เป็นค่าแบบ unsigned char
""",
        reference="""
int	ft_strcmp(char *s1, char *s2)
{
	int	i;

	i = 0;
	while (s1[i] && s1[i] == s2[i])
		i++;
	return ((unsigned char)s1[i] - (unsigned char)s2[i]);
}
""",
        harness="""
#include <stdio.h>

int	ft_strcmp(char *s1, char *s2);

int	main(int argc, char **argv)
{
	if (argc != 3)
		return (0);
	printf("%d\\n", ft_strcmp(argv[1], argv[2]));
	return (0);
}
""",
        tests=[
            ["abc", "abc"],
            ["abc", "abd"],
            ["abd", "abc"],
            ["", ""],
            ["a", ""],
            ["", "a"],
            ["abc", "abcd"],
        ],
        hints=[
            "The loop stops on the first difference OR at the end of s1.",
            "Cast to unsigned char before subtracting, or high bytes give the wrong sign.",
        ],
    ),
    ex(
        name="ft_atoi",
        exams={"exam_02": 4, "exam_03": 0},
        kind=FUNCTION,
        allowed=[],
        prototype="int ft_atoi(const char *str);",
        subject="""
Reproduce the behaviour of atoi: convert the initial numeric portion of the
string to an int.

Skip leading whitespace (spaces and tabs), then accept an optional run of '+'
and '-' signs, then read decimal digits until a non-digit is found. If there is
no digit, return 0.

Overflow behaviour is not tested.

Examples:

  ft_atoi("42")        ->  42
  ft_atoi("  -42abc")  ->  -42
  ft_atoi("+-3")       ->  -3
  ft_atoi("abc")       ->  0
""",
        subject_th="""
เขียนฟังก์ชันที่ทำงานเหมือน atoi: แปลงส่วนที่เป็นตัวเลขตอนต้นของข้อความ
ให้เป็นค่า int

ให้ข้ามช่องว่างที่นำหน้า (ช่องว่างและแท็บ) จากนั้นรับเครื่องหมาย '+' และ '-'
ที่อาจมีติดกันหลายตัว แล้วอ่านตัวเลขฐานสิบไปจนพบตัวอักษรที่ไม่ใช่ตัวเลข
ถ้าไม่มีตัวเลขเลย ให้คืนค่า 0

ไม่มีการทดสอบกรณีค่าเกินขอบเขตของ int

ตัวอย่าง:

  ft_atoi("42")        ->  42
  ft_atoi("  -42abc")  ->  -42
  ft_atoi("+-3")       ->  -3
  ft_atoi("abc")       ->  0
""",
        reference="""
int	ft_atoi(const char *str)
{
	int	i;
	int	sign;
	int	out;

	i = 0;
	sign = 1;
	out = 0;
	while (str[i] == ' ' || str[i] == '\\t' || str[i] == '\\n'
		|| str[i] == '\\v' || str[i] == '\\f' || str[i] == '\\r')
		i++;
	while (str[i] == '+' || str[i] == '-')
	{
		if (str[i] == '-')
			sign = -sign;
		i++;
	}
	while (str[i] >= '0' && str[i] <= '9')
	{
		out = out * 10 + (str[i] - '0');
		i++;
	}
	return (out * sign);
}
""",
        harness="""
#include <stdio.h>

int	ft_atoi(const char *str);

int	main(int argc, char **argv)
{
	int	i;

	i = 1;
	while (i < argc)
	{
		printf("%d\\n", ft_atoi(argv[i]));
		i++;
	}
	return (0);
}
""",
        tests=[
            ["42"],
            ["  -42abc"],
            ["+-3"],
            ["abc"],
            [""],
            ["0"],
            ["   +42"],
            ["--5"],
            ["12a34"],
        ],
        hints=[
            "Three phases in order: whitespace, signs, digits.",
            "Multiple signs multiply together: \"+-3\" is -3 and \"--5\" is 5.",
            "str[i] - '0' converts a digit character to its value.",
        ],
    ),
    ex(
        name="epur_str",
        exams={"exam_03": 2, "exam_04": 0},
        kind=PROGRAM,
        allowed=["write"],
        subject="""
Write a program that takes a string and displays it with exactly one space
between words, and no leading or trailing whitespace, followed by a newline.

A word is a sequence of characters that are neither spaces nor tabs.

If the number of arguments is not 1, the program writes only a newline.

Examples:

  $> ./epur_str "  lorem   ipsum  dolor  " | cat -e
  lorem ipsum dolor$
  $> ./epur_str "  " | cat -e
  $
""",
        subject_th="""
เขียนโปรแกรมที่รับข้อความหนึ่งชุด แล้วแสดงข้อความนั้นโดยให้มีช่องว่างระหว่างคำ
เพียงหนึ่งช่องเท่านั้น และไม่มีช่องว่างนำหน้าหรือต่อท้าย
ตามด้วยการขึ้นบรรทัดใหม่

คำ หมายถึงลำดับของตัวอักษรที่ไม่ใช่ช่องว่างและไม่ใช่แท็บ

ถ้าจำนวนอาร์กิวเมนต์ไม่เท่ากับ 1 ให้แสดงเฉพาะการขึ้นบรรทัดใหม่

ตัวอย่าง:

  $> ./epur_str "  lorem   ipsum  dolor  " | cat -e
  lorem ipsum dolor$
  $> ./epur_str "  " | cat -e
  $
""",
        reference="""
#include <unistd.h>

static int	is_space(char c)
{
	return (c == ' ' || c == '\\t');
}

int	main(int argc, char **argv)
{
	int	i;
	int	written;

	if (argc == 2)
	{
		i = 0;
		written = 0;
		while (argv[1][i])
		{
			while (is_space(argv[1][i]))
				i++;
			if (!argv[1][i])
				break ;
			if (written)
				write(1, " ", 1);
			while (argv[1][i] && !is_space(argv[1][i]))
			{
				write(1, &argv[1][i], 1);
				i++;
			}
			written = 1;
		}
	}
	write(1, "\\n", 1);
	return (0);
}
""",
        tests=[
            ["  lorem   ipsum  dolor  "],
            ["  "],
            [""],
            ["single"],
            ["a\t\tb"],
            ["   leading"],
            ["trailing   "],
            [],
        ],
        hints=[
            "Write the separating space BEFORE a word, but only if a word came before it.",
            "That flag is what keeps the leading space from being printed.",
        ],
    ),
    ex(
        name="wdmatch",
        exams={"exam_02": 7, "exam_03": 1},
        kind=PROGRAM,
        allowed=["write"],
        subject="""
Write a program that takes two strings and checks whether it is possible to
write the first string using the characters of the second, taking them in order
and using each at most once.

If it is possible, display the first string followed by a newline. Otherwise
display only a newline.

If the number of arguments is not 2, the program writes only a newline.

Examples:

  $> ./wdmatch "faya" "fgvvfdxcacpolhyaghbn" | cat -e
  faya$
  $> ./wdmatch "faya" "fgvvfdxcacpolhy" | cat -e
  $
""",
        subject_th="""
เขียนโปรแกรมที่รับข้อความสองชุด แล้วตรวจสอบว่าสามารถสร้างข้อความชุดแรก
จากตัวอักษรในข้อความชุดที่สองได้หรือไม่ โดยต้องเลือกตัวอักษรตามลำดับที่ปรากฏ
และใช้แต่ละตัวได้ไม่เกินหนึ่งครั้ง

ถ้าทำได้ ให้แสดงข้อความชุดแรก ตามด้วยการขึ้นบรรทัดใหม่
ถ้าทำไม่ได้ ให้แสดงเฉพาะการขึ้นบรรทัดใหม่

ถ้าจำนวนอาร์กิวเมนต์ไม่เท่ากับ 2 ให้แสดงเฉพาะการขึ้นบรรทัดใหม่

ตัวอย่าง:

  $> ./wdmatch "faya" "fgvvfdxcacpolhyaghbn" | cat -e
  faya$
  $> ./wdmatch "faya" "fgvvfdxcacpolhy" | cat -e
  $
""",
        reference="""
#include <unistd.h>

int	main(int argc, char **argv)
{
	int	i;
	int	j;

	if (argc == 3)
	{
		i = 0;
		j = 0;
		while (argv[1][i] && argv[2][j])
		{
			if (argv[1][i] == argv[2][j])
				i++;
			j++;
		}
		if (!argv[1][i])
		{
			i = 0;
			while (argv[1][i])
				write(1, &argv[1][i++], 1);
		}
	}
	write(1, "\\n", 1);
	return (0);
}
""",
        tests=[
            ["faya", "fgvvfdxcacpolhyaghbn"],
            ["faya", "fgvvfdxcacpolhy"],
            ["", "abc"],
            ["abc", ""],
            ["abc", "abc"],
            ["aaa", "aa"],
            [],
        ],
        hints=[
            "One index per string: advance the second always, the first only on a match.",
            "You succeeded if you reached the end of the FIRST string.",
        ],
    ),
    ex(
        name="inter",
        exams={"exam_02": 4, "exam_03": 0},
        kind=PROGRAM,
        allowed=["write"],
        subject="""
Write a program that takes two strings and displays, without duplicates, the
characters that appear in both, in the order they appear in the first string.
The output is followed by a newline.

If the number of arguments is not 2, the program writes only a newline.

Example:

  $> ./inter "padinton" "paqefwtdjetyiytjneytjoeyjnejeyj" | cat -e
  padinto$
""",
        subject_th="""
เขียนโปรแกรมที่รับข้อความสองชุด แล้วแสดงตัวอักษรที่ปรากฏอยู่ในทั้งสองข้อความ
โดยไม่แสดงซ้ำ และเรียงตามลำดับที่ปรากฏในข้อความชุดแรก
ตามด้วยการขึ้นบรรทัดใหม่

ถ้าจำนวนอาร์กิวเมนต์ไม่เท่ากับ 2 ให้แสดงเฉพาะการขึ้นบรรทัดใหม่

ตัวอย่าง:

  $> ./inter "padinton" "paqefwtdjetyiytjneytjoeyjnejeyj" | cat -e
  padinto$
""",
        reference="""
#include <unistd.h>

int	main(int argc, char **argv)
{
	char	seen[256];
	int		i;
	int		j;

	if (argc == 3)
	{
		i = 0;
		while (i < 256)
			seen[i++] = 0;
		i = 0;
		while (argv[1][i])
		{
			j = 0;
			while (argv[2][j] && argv[2][j] != argv[1][i])
				j++;
			if (argv[2][j] && !seen[(unsigned char)argv[1][i]])
			{
				write(1, &argv[1][i], 1);
				seen[(unsigned char)argv[1][i]] = 1;
			}
			i++;
		}
	}
	write(1, "\\n", 1);
	return (0);
}
""",
        tests=[
            ["padinton", "paqefwtdjetyiytjneytjoeyjnejeyj"],
            ["ddf6vewg64f", "gtwdb"],
            ["", "abc"],
            ["abc", ""],
            ["aaa", "a"],
            [],
        ],
        hints=[
            "A 256-entry flag array is the easy way to suppress duplicates.",
            "Index that array with (unsigned char) so negative bytes cannot escape it.",
        ],
    ),
    ex(
        name="union",
        exams={"exam_02": 5, "exam_03": 0},
        kind=PROGRAM,
        allowed=["write"],
        subject="""
Write a program that takes two strings and displays, without duplicates, every
character that appears in either of them, in order of first appearance -- all of
the first string, then the second. The output is followed by a newline.

If the number of arguments is not 2, the program writes only a newline.

Example:

  $> ./union zpadinton "pathe" | cat -e
  zpadintohe$
""",
        subject_th="""
เขียนโปรแกรมที่รับข้อความสองชุด แล้วแสดงตัวอักษรทุกตัวที่ปรากฏในข้อความใดก็ได้
โดยไม่แสดงซ้ำ เรียงตามลำดับที่พบครั้งแรก คือไล่จากข้อความชุดแรกทั้งชุด
แล้วต่อด้วยข้อความชุดที่สอง ตามด้วยการขึ้นบรรทัดใหม่

ถ้าจำนวนอาร์กิวเมนต์ไม่เท่ากับ 2 ให้แสดงเฉพาะการขึ้นบรรทัดใหม่

ตัวอย่าง:

  $> ./union zpadinton "pathe" | cat -e
  zpadintohe$
""",
        reference="""
#include <unistd.h>

static void	emit(char *s, char *seen)
{
	int	i;

	i = 0;
	while (s[i])
	{
		if (!seen[(unsigned char)s[i]])
		{
			write(1, &s[i], 1);
			seen[(unsigned char)s[i]] = 1;
		}
		i++;
	}
}

int	main(int argc, char **argv)
{
	char	seen[256];
	int		i;

	if (argc == 3)
	{
		i = 0;
		while (i < 256)
			seen[i++] = 0;
		emit(argv[1], seen);
		emit(argv[2], seen);
	}
	write(1, "\\n", 1);
	return (0);
}
""",
        tests=[
            ["zpadinton", "pathe"],
            ["ddf6vewg64f", "gtwdb"],
            ["", "abc"],
            ["abc", ""],
            ["aaa", "aaa"],
            [],
        ],
        hints=[
            "The same seen[] array carries over from the first string to the second.",
            "That single shared array is what makes the union work in one pass each.",
        ],
    ),
    ex(
        name="str_capitalizer",
        exams={"exam_03": 3, "exam_04": 1},
        kind=PROGRAM,
        allowed=["write"],
        subject="""
Write a program that takes one or several strings and, for each argument,
capitalizes the first character of each word (if it is a letter, obviously), puts
the rest in lowercase, and displays the result, followed by a newline.

A "word" is defined as a part of a string delimited either by spaces/tabs, or by
the start/end of the string. If a word only has one letter, it must be
capitalized.

If there are no arguments, the program must display a newline.

Examples:

  $> ./str_capitalizer "Premier PETIT TesT" | cat -e
  Premier Petit Test$
  $> ./str_capitalizer "   attention C'EST pas dur QUAND mEmE" | cat -e
     Attention C'est Pas Dur Quand Meme$
  $> ./str_capitalizer "ALLer UN DeRNier 0123456789pour LA rouTE    E " | cat -e
  Aller Un Dernier 0123456789pour La Route    E $
  $> ./str_capitalizer | cat -e
  $
""",
        subject_th="""
เขียนโปรแกรมที่รับข้อความหนึ่งชุดหรือมากกว่า แล้วสำหรับแต่ละอาร์กิวเมนต์
ให้เปลี่ยนตัวอักษรตัวแรกของแต่ละคำเป็นตัวพิมพ์ใหญ่ (เฉพาะกรณีที่เป็นตัวอักษร)
และเปลี่ยนตัวที่เหลือเป็นตัวพิมพ์เล็ก แล้วแสดงผลตามด้วยการขึ้นบรรทัดใหม่

"คำ" หมายถึงส่วนของข้อความที่คั่นด้วยช่องว่างหรือแท็บ หรือคั่นด้วยจุดเริ่มต้น
และจุดสิ้นสุดของข้อความ ถ้าคำหนึ่งมีตัวอักษรเพียงตัวเดียว ก็ต้องเปลี่ยนเป็นตัวพิมพ์ใหญ่

ถ้าไม่มีอาร์กิวเมนต์เลย ให้แสดงเฉพาะการขึ้นบรรทัดใหม่

ตัวอย่าง:

  $> ./str_capitalizer "Premier PETIT TesT" | cat -e
  Premier Petit Test$
  $> ./str_capitalizer "   attention C'EST pas dur QUAND mEmE" | cat -e
     Attention C'est Pas Dur Quand Meme$
  $> ./str_capitalizer "ALLer UN DeRNier 0123456789pour LA rouTE    E " | cat -e
  Aller Un Dernier 0123456789pour La Route    E $
  $> ./str_capitalizer | cat -e
  $
""",
        reference="""
#include <unistd.h>

static int	is_space(char c)
{
	return (c == ' ' || c == '\\t');
}

int	main(int argc, char **argv)
{
	int		i;
	int		j;
	int		start;
	char	c;

	if (argc < 2)
	{
		write(1, "\\n", 1);
		return (0);
	}
	i = 1;
	while (i < argc)
	{
		j = 0;
		start = 1;
		while (argv[i][j])
		{
			c = argv[i][j];
			if (is_space(c))
				start = 1;
			else
			{
				if (start && c >= 'a' && c <= 'z')
					c = c - 32;
				else if (!start && c >= 'A' && c <= 'Z')
					c = c + 32;
				start = 0;
			}
			write(1, &c, 1);
			j++;
		}
		write(1, "\\n", 1);
		i++;
	}
	return (0);
}
""",
        tests=[
            ["Premier PETIT TesT"],
            ["   attention C'EST pas dur QUAND mEmE"],
            ["ALLer UN DeRNier 0123456789pour LA rouTE    E "],
            ["DeuxiEmE tEST uN PEU moinS  facile", "second ARG"],
            [],
            [""],
            ["a"],
            ["HELLO"],
        ],
        hints=[
            "Only spaces and tabs separate words. An apostrophe does NOT, so "
            "\"C'EST\" becomes \"C'est\" and not \"C'Est\".",
            "A word starting with a digit has nothing to capitalize, but the "
            "letters after it are still lowercased.",
            "Track whether you are at the start of a word with a single flag.",
            "One newline per argument.",
        ],
    ),
    ex(
        name="tab_mult",
        exams={"exam_03": 3, "exam_04": 1},
        kind=PROGRAM,
        allowed=["write"],
        subject="""
Write a program that takes a positive integer and displays its multiplication
table from 1 to 9, one line per row, in the form:

  1 x n = n
  2 x n = 2n
  ...
  9 x n = 9n

If the number of arguments is not 1, the program writes only a newline.
You may assume the argument is a valid positive integer.

Example:

  $> ./tab_mult 9 | cat -e
  1 x 9 = 9$
  2 x 9 = 18$
  3 x 9 = 27$
  4 x 9 = 36$
  5 x 9 = 45$
  6 x 9 = 54$
  7 x 9 = 63$
  8 x 9 = 72$
  9 x 9 = 81$
""",
        subject_th="""
เขียนโปรแกรมที่รับจำนวนเต็มบวกหนึ่งจำนวน แล้วแสดงสูตรคูณของจำนวนนั้น
จาก 1 ถึง 9 บรรทัดละหนึ่งแถว ในรูปแบบ:

  1 x n = n
  2 x n = 2n
  ...
  9 x n = 9n

ถ้าจำนวนอาร์กิวเมนต์ไม่เท่ากับ 1 ให้แสดงเฉพาะการขึ้นบรรทัดใหม่
สามารถสมมติได้ว่าอาร์กิวเมนต์เป็นจำนวนเต็มบวกที่ถูกต้อง

ตัวอย่าง:

  $> ./tab_mult 9 | cat -e
  1 x 9 = 9$
  2 x 9 = 18$
  3 x 9 = 27$
  4 x 9 = 36$
  5 x 9 = 45$
  6 x 9 = 54$
  7 x 9 = 63$
  8 x 9 = 72$
  9 x 9 = 81$
""",
        reference="""
#include <unistd.h>

static void	put_nbr(int n)
{
	char	c;

	if (n >= 10)
		put_nbr(n / 10);
	c = (n % 10) + '0';
	write(1, &c, 1);
}

static int	str_to_int(char *s)
{
	int	out;

	out = 0;
	while (*s >= '0' && *s <= '9')
		out = out * 10 + (*s++ - '0');
	return (out);
}

int	main(int argc, char **argv)
{
	int	n;
	int	i;

	if (argc != 2)
	{
		write(1, "\\n", 1);
		return (0);
	}
	n = str_to_int(argv[1]);
	i = 1;
	while (i <= 9)
	{
		put_nbr(i);
		write(1, " x ", 3);
		put_nbr(n);
		write(1, " = ", 3);
		put_nbr(i * n);
		write(1, "\\n", 1);
		i++;
	}
	return (0);
}
""",
        tests=[["9"], ["1"], ["0"], ["42"], [], ["1", "2"]],
        hints=[
            "Only write is allowed, so you need your own number printer.",
            "Recursion is the shortest route: print n / 10 first, then the last digit.",
        ],
    ),
    ex(
        name="paramsum",
        exams={"exam_03": 3, "exam_04": 1},
        kind=PROGRAM,
        allowed=["write"],
        subject="""
Write a program that displays the number of arguments it received, followed by a
newline. The program name itself does not count.

Examples:

  $> ./paramsum 1 2 3 | cat -e
  3$
  $> ./paramsum | cat -e
  0$
""",
        subject_th="""
เขียนโปรแกรมที่แสดงจำนวนอาร์กิวเมนต์ที่ได้รับ ตามด้วยการขึ้นบรรทัดใหม่
โดยไม่นับชื่อโปรแกรมเอง

ตัวอย่าง:

  $> ./paramsum 1 2 3 | cat -e
  3$
  $> ./paramsum | cat -e
  0$
""",
        reference="""
#include <unistd.h>

static void	put_nbr(int n)
{
	char	c;

	if (n >= 10)
		put_nbr(n / 10);
	c = (n % 10) + '0';
	write(1, &c, 1);
}

int	main(int argc, char **argv)
{
	(void)argv;
	put_nbr(argc - 1);
	write(1, "\\n", 1);
	return (0);
}
""",
        tests=[["1", "2", "3"], [], ["a"], ["a", "b", "c", "d", "e"]],
        hints=[
            "argc counts the program name, so the answer is argc - 1.",
            "Cast argv to (void) if you never use it, or -Werror will stop you.",
        ],
    ),
    ex(
        name="pgcd",
        exams={"exam_03": 2, "exam_04": 0},
        kind=PROGRAM,
        allowed=["atoi", "free", "malloc", "printf"],
        subject="""
Write a program that takes two strictly positive integers and displays their
greatest common divisor, followed by a newline.

If the number of arguments is not 2, the program writes only a newline.
You may assume both arguments are valid strictly positive integers.

Example:

  $> ./pgcd 42 10 | cat -e
  2$
""",
        subject_th="""
เขียนโปรแกรมที่รับจำนวนเต็มบวกสองจำนวน แล้วแสดงตัวหารร่วมมากของสองจำนวนนั้น
ตามด้วยการขึ้นบรรทัดใหม่

ถ้าจำนวนอาร์กิวเมนต์ไม่เท่ากับ 2 ให้แสดงเฉพาะการขึ้นบรรทัดใหม่
สามารถสมมติได้ว่าอาร์กิวเมนต์ทั้งสองเป็นจำนวนเต็มบวกที่ถูกต้อง

ตัวอย่าง:

  $> ./pgcd 42 10 | cat -e
  2$
""",
        reference="""
#include <stdio.h>
#include <stdlib.h>

int	main(int argc, char **argv)
{
	int	a;
	int	b;
	int	tmp;

	if (argc != 3)
	{
		printf("\\n");
		return (0);
	}
	a = atoi(argv[1]);
	b = atoi(argv[2]);
	while (b != 0)
	{
		tmp = b;
		b = a % b;
		a = tmp;
	}
	printf("%d\\n", a);
	return (0);
}
""",
        tests=[["42", "10"], ["7", "3"], ["42", "42"], ["100", "10"], ["1", "1"], []],
        hints=[
            "Euclid's algorithm: replace (a, b) with (b, a % b) until b is 0.",
            "The answer is whatever is left in a.",
        ],
    ),
    ex(
        name="is_power_of_2",
        exams={"exam_02": 7, "exam_03": 1},
        kind=FUNCTION,
        allowed=[],
        prototype="int is_power_of_2(unsigned int n);",
        subject="""
Write a function that returns 1 if the given number is a power of 2, and 0
otherwise.

0 is not a power of 2.
""",
        subject_th="""
เขียนฟังก์ชันที่คืนค่า 1 ถ้าจำนวนที่รับเข้ามาเป็นเลขยกกำลังของ 2
และคืนค่า 0 ถ้าไม่ใช่

โดยที่ 0 ไม่ถือว่าเป็นเลขยกกำลังของ 2
""",
        reference="""
int	is_power_of_2(unsigned int n)
{
	if (n == 0)
		return (0);
	return ((n & (n - 1)) == 0);
}
""",
        harness="""
#include <stdio.h>
#include <stdlib.h>

int	is_power_of_2(unsigned int n);

int	main(int argc, char **argv)
{
	int	i;

	i = 1;
	while (i < argc)
	{
		printf("%d\\n", is_power_of_2((unsigned int)atoi(argv[i])));
		i++;
	}
	return (0);
}
""",
        tests=[["1"], ["2"], ["3"], ["0"], ["1024"], ["1023"], ["16"], ["42"]],
        hints=[
            "A power of 2 has exactly one bit set.",
            "n & (n - 1) clears the lowest set bit -- if nothing is left, there was only one.",
            "Handle 0 first: it would otherwise pass the bit test.",
        ],
    ),
    ex(
        name="print_hex",
        exams={"exam_03": 2, "exam_04": 0},
        kind=PROGRAM,
        allowed=["write"],
        subject="""
Write a program that takes a positive decimal number and displays it in
lowercase hexadecimal, followed by a newline.

If the number of arguments is not 1, the program writes only a newline.
You may assume the argument is a valid positive integer.

Examples:

  $> ./print_hex "255" | cat -e
  ff$
  $> ./print_hex "0" | cat -e
  0$
""",
        subject_th="""
เขียนโปรแกรมที่รับจำนวนเต็มบวกในระบบฐานสิบ แล้วแสดงค่าในระบบเลขฐานสิบหก
แบบตัวพิมพ์เล็ก ตามด้วยการขึ้นบรรทัดใหม่

ถ้าจำนวนอาร์กิวเมนต์ไม่เท่ากับ 1 ให้แสดงเฉพาะการขึ้นบรรทัดใหม่
สามารถสมมติได้ว่าอาร์กิวเมนต์เป็นจำนวนเต็มบวกที่ถูกต้อง

ตัวอย่าง:

  $> ./print_hex "255" | cat -e
  ff$
  $> ./print_hex "0" | cat -e
  0$
""",
        reference="""
#include <unistd.h>

static void	put_hex(unsigned int n)
{
	char	*digits = "0123456789abcdef";

	if (n >= 16)
		put_hex(n / 16);
	write(1, &digits[n % 16], 1);
}

int	main(int argc, char **argv)
{
	unsigned int	n;
	int				i;

	if (argc != 2)
	{
		write(1, "\\n", 1);
		return (0);
	}
	n = 0;
	i = 0;
	while (argv[1][i] >= '0' && argv[1][i] <= '9')
		n = n * 10 + (argv[1][i++] - '0');
	put_hex(n);
	write(1, "\\n", 1);
	return (0);
}
""",
        tests=[["255"], ["0"], ["1"], ["16"], ["4294967295"], [], ["1", "2"]],
        hints=[
            "A lookup string \"0123456789abcdef\" saves you a branch.",
            "Recurse on n / 16 first so the digits come out in the right order.",
        ],
    ),
]
