"""Exam Rank 02 hard / Rank 03 pool -- levels 3 to 5.

From here on the exercises allocate. Output formats that the standard subjects
leave implicit (print_memory in particular) are pinned down exactly here, because
the grader compares bytes and a learner cannot guess a format.
"""

from engine.exercises.spec import ex, ADDED, PROGRAM, FUNCTION

EXERCISES = [
    # ------------------------------------------------------------------ level 3
    ex(
        name="ft_strdup",
        exams={"exam_02": 4, "exam_03": 0},
        kind=FUNCTION,
        allowed=["malloc"],
        prototype="char *ft_strdup(char *src);",
        subject="""
Reproduce the behaviour of strdup: allocate a new string with malloc, copy src
into it, and return it.

The returned string must be null-terminated. Return NULL if the allocation
fails.
""",
        subject_th="""
เขียนฟังก์ชันที่ทำงานเหมือน strdup: จองหน่วยความจำใหม่ด้วย malloc
คัดลอกข้อความ src ลงไป แล้วคืนค่าพอยน์เตอร์ที่ได้

ข้อความที่คืนค่าต้องปิดท้ายด้วยไบต์ null และถ้าจองหน่วยความจำไม่สำเร็จให้คืนค่า NULL
""",
        reference="""
#include <stdlib.h>

char	*ft_strdup(char *src)
{
	char	*out;
	int		len;
	int		i;

	len = 0;
	while (src[len])
		len++;
	out = malloc(sizeof(char) * (len + 1));
	if (!out)
		return (0);
	i = 0;
	while (i < len)
	{
		out[i] = src[i];
		i++;
	}
	out[i] = '\\0';
	return (out);
}
""",
        harness="""
#include <stdio.h>
#include <stdlib.h>

char	*ft_strdup(char *src);

int	main(int argc, char **argv)
{
	char	*copy;
	int		i;

	i = 1;
	while (i < argc)
	{
		copy = ft_strdup(argv[i]);
		if (!copy)
			return (1);
		/* A different address proves it really allocated. */
		printf("[%s] copied=%d\\n", copy, copy != argv[i]);
		free(copy);
		i++;
	}
	return (0);
}
""",
        tests=[["hello"], [""], ["a"], ["42born2code"], ["with spaces here"]],
        hints=[
            "Count the length first, then malloc len + 1 for the '\\0'.",
            "Returning src itself is not duplicating -- you must allocate.",
        ],
    ),
    ex(
        name="ft_range",
        exams={"exam_03": 3, "exam_04": 1},
        kind=FUNCTION,
        allowed=["malloc"],
        prototype="int *ft_range(int start, int end);",
        subject="""
Write a function that allocates and returns an array of integers containing every
value from start to end, inclusive.

If start is greater than end, the values run downwards. The array therefore
always holds |end - start| + 1 elements.

Return NULL if the allocation fails.

Examples:

  ft_range(1, 3)   ->  [1, 2, 3]
  ft_range(3, 1)   ->  [3, 2, 1]
  ft_range(5, 5)   ->  [5]
""",
        subject_th="""
เขียนฟังก์ชันที่จองหน่วยความจำและคืนค่าอาเรย์ของจำนวนเต็ม ซึ่งบรรจุค่าทุกค่า
จาก start ถึง end โดยนับปลายทั้งสองข้างด้วย

ถ้า start มากกว่า end ให้ไล่ค่าจากมากไปน้อย ดังนั้นอาเรย์จะมีสมาชิก
|end - start| + 1 ตัวเสมอ

ถ้าจองหน่วยความจำไม่สำเร็จให้คืนค่า NULL

ตัวอย่าง:

  ft_range(1, 3)   ->  [1, 2, 3]
  ft_range(3, 1)   ->  [3, 2, 1]
  ft_range(5, 5)   ->  [5]
""",
        reference="""
#include <stdlib.h>

int	*ft_range(int start, int end)
{
	int	*out;
	int	len;
	int	i;
	int	step;

	if (start <= end)
	{
		len = end - start + 1;
		step = 1;
	}
	else
	{
		len = start - end + 1;
		step = -1;
	}
	out = malloc(sizeof(int) * len);
	if (!out)
		return (0);
	i = 0;
	while (i < len)
	{
		out[i] = start + i * step;
		i++;
	}
	return (out);
}
""",
        harness="""
#include <stdio.h>
#include <stdlib.h>

int	*ft_range(int start, int end);

int	main(int argc, char **argv)
{
	int	*tab;
	int	start;
	int	end;
	int	len;
	int	i;

	if (argc != 3)
		return (0);
	start = atoi(argv[1]);
	end = atoi(argv[2]);
	if (start <= end)
		len = end - start + 1;
	else
		len = start - end + 1;
	tab = ft_range(start, end);
	if (!tab)
		return (1);
	i = 0;
	while (i < len)
	{
		printf("%d", tab[i]);
		if (i + 1 < len)
			printf(" ");
		i++;
	}
	printf("\\n");
	free(tab);
	return (0);
}
""",
        tests=[
            ["1", "3"],
            ["3", "1"],
            ["5", "5"],
            ["-2", "2"],
            ["2", "-2"],
            ["0", "0"],
        ],
        hints=[
            "The length is |end - start| + 1 in both directions -- never 0.",
            "A step of +1 or -1 lets one loop handle both cases.",
        ],
    ),
    ex(
        name="ft_rrange",
        exams={"exam_03": 2, "exam_04": 0},
        kind=FUNCTION,
        allowed=["malloc"],
        prototype="int *ft_rrange(int start, int end);",
        subject="""
Write a function that allocates and returns an array of integers containing every
value from start to end, inclusive, in REVERSE order.

The array always holds |end - start| + 1 elements. Return NULL if the allocation
fails.

Examples:

  ft_rrange(1, 3)   ->  [3, 2, 1]
  ft_rrange(3, 1)   ->  [1, 2, 3]
""",
        subject_th="""
เขียนฟังก์ชันที่จองหน่วยความจำและคืนค่าอาเรย์ของจำนวนเต็ม ซึ่งบรรจุค่าทุกค่า
จาก start ถึง end โดยนับปลายทั้งสองข้างด้วย แต่เรียงลำดับกลับหลัง

อาเรย์จะมีสมาชิก |end - start| + 1 ตัวเสมอ
ถ้าจองหน่วยความจำไม่สำเร็จให้คืนค่า NULL

ตัวอย่าง:

  ft_rrange(1, 3)   ->  [3, 2, 1]
  ft_rrange(3, 1)   ->  [1, 2, 3]
""",
        reference="""
#include <stdlib.h>

int	*ft_rrange(int start, int end)
{
	int	*out;
	int	len;
	int	i;
	int	step;

	if (start <= end)
	{
		len = end - start + 1;
		step = 1;
	}
	else
	{
		len = start - end + 1;
		step = -1;
	}
	out = malloc(sizeof(int) * len);
	if (!out)
		return (0);
	i = 0;
	while (i < len)
	{
		out[len - 1 - i] = start + i * step;
		i++;
	}
	return (out);
}
""",
        harness="""
#include <stdio.h>
#include <stdlib.h>

int	*ft_rrange(int start, int end);

int	main(int argc, char **argv)
{
	int	*tab;
	int	start;
	int	end;
	int	len;
	int	i;

	if (argc != 3)
		return (0);
	start = atoi(argv[1]);
	end = atoi(argv[2]);
	if (start <= end)
		len = end - start + 1;
	else
		len = start - end + 1;
	tab = ft_rrange(start, end);
	if (!tab)
		return (1);
	i = 0;
	while (i < len)
	{
		printf("%d", tab[i]);
		if (i + 1 < len)
			printf(" ");
		i++;
	}
	printf("\\n");
	free(tab);
	return (0);
}
""",
        tests=[["1", "3"], ["3", "1"], ["5", "5"], ["-2", "2"], ["0", "0"]],
        hints=[
            "Same length calculation as ft_range -- only the write index changes.",
            "Fill out[len - 1 - i] instead of out[i].",
        ],
    ),
    ex(
        name="ft_itoa",
        exams={"exam_04": 2},
        kind=FUNCTION,
        allowed=["malloc"],
        prototype="char *ft_itoa(int nbr);",
        subject="""
Write a function that allocates and returns the decimal representation of nbr as
a null-terminated string.

Negative numbers are prefixed with '-'. The function must handle INT_MIN
(-2147483648) correctly. Return NULL if the allocation fails.

Examples:

  ft_itoa(42)     ->  "42"
  ft_itoa(0)      ->  "0"
  ft_itoa(-42)    ->  "-42"
""",
        subject_th="""
เขียนฟังก์ชันที่จองหน่วยความจำและคืนค่าข้อความที่แทนค่า nbr ในระบบฐานสิบ
โดยปิดท้ายด้วยไบต์ null

จำนวนลบให้นำหน้าด้วยเครื่องหมาย '-' และฟังก์ชันต้องรองรับค่า INT_MIN
(-2147483648) ได้อย่างถูกต้อง ถ้าจองหน่วยความจำไม่สำเร็จให้คืนค่า NULL

ตัวอย่าง:

  ft_itoa(42)     ->  "42"
  ft_itoa(0)      ->  "0"
  ft_itoa(-42)    ->  "-42"
""",
        reference="""
#include <stdlib.h>

static int	digit_count(long n)
{
	int	count;

	count = 1;
	while (n >= 10 || n <= -10)
	{
		n /= 10;
		count++;
	}
	return (count);
}

char	*ft_itoa(int nbr)
{
	char	*out;
	long	n;
	int		len;
	int		neg;

	n = nbr;
	neg = (n < 0);
	len = digit_count(n) + neg;
	out = malloc(sizeof(char) * (len + 1));
	if (!out)
		return (0);
	out[len] = '\\0';
	if (neg)
	{
		out[0] = '-';
		n = -n;
	}
	while (len-- > neg)
	{
		out[len] = (n % 10) + '0';
		n /= 10;
	}
	return (out);
}
""",
        harness="""
#include <stdio.h>
#include <stdlib.h>

char	*ft_itoa(int nbr);

int	main(int argc, char **argv)
{
	char	*s;
	int		i;

	i = 1;
	while (i < argc)
	{
		s = ft_itoa(atoi(argv[i]));
		if (!s)
			return (1);
		printf("[%s]\\n", s);
		free(s);
		i++;
	}
	return (0);
}
""",
        tests=[
            ["42"],
            ["0"],
            ["-42"],
            ["2147483647"],
            ["-2147483648"],
            ["1"],
            ["-1"],
            ["100"],
        ],
        hints=[
            "Negating INT_MIN overflows an int -- do the arithmetic in a long.",
            "Count the digits before you malloc, and remember the '-' and the '\\0'.",
            "0 has one digit, so a count starting at 1 handles it.",
        ],
    ),
    ex(
        name="rostring",
        exams={"exam_04": 2},
        kind=PROGRAM,
        allowed=["free", "malloc", "write"],
        subject="""
Write a program that takes a string and displays it with the first word moved to
the end, followed by a newline.

Words in the output are separated by exactly one space, with no leading or
trailing whitespace. A word is a sequence of characters that are neither spaces
nor tabs.

If the number of arguments is not 1, or if the string contains no word, the
program writes only a newline.

Examples:

  $> ./rostring "abc def ghi" | cat -e
  def ghi abc$
  $> ./rostring "  hello   world  " | cat -e
  world hello$
  $> ./rostring "solo" | cat -e
  solo$
""",
        subject_th="""
เขียนโปรแกรมที่รับข้อความหนึ่งชุด แล้วแสดงข้อความนั้นโดยย้ายคำแรกไปไว้ท้ายสุด
ตามด้วยการขึ้นบรรทัดใหม่

คำในผลลัพธ์ให้คั่นด้วยช่องว่างหนึ่งช่องเท่านั้น และไม่มีช่องว่างนำหน้าหรือต่อท้าย
คำ หมายถึงลำดับของตัวอักษรที่ไม่ใช่ช่องว่างและไม่ใช่แท็บ

ถ้าจำนวนอาร์กิวเมนต์ไม่เท่ากับ 1 หรือในข้อความไม่มีคำใดเลย
ให้แสดงเฉพาะการขึ้นบรรทัดใหม่

ตัวอย่าง:

  $> ./rostring "abc def ghi" | cat -e
  def ghi abc$
  $> ./rostring "  hello   world  " | cat -e
  world hello$
  $> ./rostring "solo" | cat -e
  solo$
""",
        reference="""
#include <unistd.h>

static int	is_space(char c)
{
	return (c == ' ' || c == '\\t');
}

static int	put_word(char *s, int i, int need_space)
{
	if (need_space)
		write(1, " ", 1);
	while (s[i] && !is_space(s[i]))
	{
		write(1, &s[i], 1);
		i++;
	}
	return (i);
}

int	main(int argc, char **argv)
{
	int	i;
	int	first;
	int	written;

	if (argc == 2)
	{
		i = 0;
		while (is_space(argv[1][i]))
			i++;
		first = i;
		while (argv[1][i] && !is_space(argv[1][i]))
			i++;
		written = 0;
		while (argv[1][i])
		{
			while (is_space(argv[1][i]))
				i++;
			if (!argv[1][i])
				break ;
			i = put_word(argv[1], i, written);
			written = 1;
		}
		if (argv[1][first])
			put_word(argv[1], first, written);
	}
	write(1, "\\n", 1);
	return (0);
}
""",
        tests=[
            ["abc def ghi"],
            ["  hello   world  "],
            ["solo"],
            [""],
            ["   "],
            ["a b"],
            [],
        ],
        hints=[
            "Remember where the first word starts, print everything after it, then print it last.",
            "The separator logic is the same as epur_str: one space before a word, but not the first.",
        ],
    ),
    ex(
        name="hidenp",
        exams={"exam_03": 2, "exam_04": 0},
        kind=PROGRAM,
        allowed=["write"],
        subject="""
Write a program that takes two strings and displays 1 if the first is a hidden
subsequence of the second, and 0 otherwise, followed by a newline.

A string s1 is hidden in s2 if its characters can be found in s2 in the same
order, not necessarily adjacent. The empty string is hidden in any string.

If the number of arguments is not 2, the program writes only a newline.

Examples:

  $> ./hidenp "fgex.;" "tyf34gdgex.;.;" | cat -e
  1$
  $> ./hidenp "abc" "acb" | cat -e
  0$
""",
        subject_th="""
เขียนโปรแกรมที่รับข้อความสองชุด แล้วแสดงเลข 1 ถ้าข้อความชุดแรกซ่อนอยู่ใน
ข้อความชุดที่สอง และแสดงเลข 0 ถ้าไม่ใช่ ตามด้วยการขึ้นบรรทัดใหม่

ข้อความ s1 ถือว่าซ่อนอยู่ใน s2 ถ้าสามารถหาตัวอักษรของ s1 ได้ใน s2
โดยเรียงตามลำดับเดิม แต่ไม่จำเป็นต้องอยู่ติดกัน
ข้อความว่างถือว่าซ่อนอยู่ในทุกข้อความ

ถ้าจำนวนอาร์กิวเมนต์ไม่เท่ากับ 2 ให้แสดงเฉพาะการขึ้นบรรทัดใหม่

ตัวอย่าง:

  $> ./hidenp "fgex.;" "tyf34gdgex.;.;" | cat -e
  1$
  $> ./hidenp "abc" "acb" | cat -e
  0$
""",
        reference="""
#include <unistd.h>

int	main(int argc, char **argv)
{
	int	i;
	int	j;

	if (argc != 3)
	{
		write(1, "\\n", 1);
		return (0);
	}
	i = 0;
	j = 0;
	while (argv[1][i] && argv[2][j])
	{
		if (argv[1][i] == argv[2][j])
			i++;
		j++;
	}
	if (argv[1][i])
		write(1, "0\\n", 2);
	else
		write(1, "1\\n", 2);
	return (0);
}
""",
        tests=[
            ["fgex.;", "tyf34gdgex.;.;"],
            ["abc", "acb"],
            ["", "anything"],
            ["abc", ""],
            ["abc", "abc"],
            ["aaa", "aa"],
            [],
        ],
        hints=[
            "Same two-index walk as wdmatch -- only the output differs.",
            "Reaching the end of s1 means success, so test argv[1][i] afterwards.",
        ],
    ),
    # ------------------------------------------------------------------ level 4
    ex(
        name="ft_strjoin",
        exams={"exam_03": 3, "exam_04": 1},
        source=ADDED,
        kind=FUNCTION,
        allowed=["malloc"],
        prototype="char *ft_strjoin(int size, char **strs, char *sep);",
        subject="""
Write a function that concatenates the `size` strings of the array strs,
separating each pair with sep, and returns the result as a freshly allocated
null-terminated string.

If size is 0, return an empty allocated string. Return NULL if the allocation
fails.

Example:

  strs = {"Hello", "world"}, sep = ", "  ->  "Hello, world"
""",
        subject_th="""
เขียนฟังก์ชันที่ต่อข้อความจำนวน size ชุดในอาเรย์ strs เข้าด้วยกัน
โดยคั่นระหว่างแต่ละคู่ด้วย sep แล้วคืนค่าผลลัพธ์เป็นข้อความที่จองหน่วยความจำใหม่
และปิดท้ายด้วยไบต์ null

ถ้า size เท่ากับ 0 ให้คืนค่าข้อความว่างที่จองหน่วยความจำแล้ว
ถ้าจองหน่วยความจำไม่สำเร็จให้คืนค่า NULL

ตัวอย่าง:

  strs = {"Hello", "world"}, sep = ", "  ->  "Hello, world"
""",
        reference="""
#include <stdlib.h>

static int	len_of(char *s)
{
	int	i;

	i = 0;
	while (s[i])
		i++;
	return (i);
}

static int	copy_into(char *dst, int at, char *src)
{
	int	i;

	i = 0;
	while (src[i])
		dst[at++] = src[i++];
	return (at);
}

char	*ft_strjoin(int size, char **strs, char *sep)
{
	char	*out;
	int		total;
	int		at;
	int		i;

	total = 0;
	i = 0;
	while (i < size)
		total += len_of(strs[i++]);
	if (size > 1)
		total += len_of(sep) * (size - 1);
	out = malloc(sizeof(char) * (total + 1));
	if (!out)
		return (0);
	at = 0;
	i = 0;
	while (i < size)
	{
		at = copy_into(out, at, strs[i]);
		if (i + 1 < size)
			at = copy_into(out, at, sep);
		i++;
	}
	out[at] = '\\0';
	return (out);
}
""",
        harness="""
#include <stdio.h>
#include <stdlib.h>

char	*ft_strjoin(int size, char **strs, char *sep);

int	main(int argc, char **argv)
{
	char	*joined;

	if (argc < 2)
		return (0);
	joined = ft_strjoin(argc - 2, argv + 2, argv[1]);
	if (!joined)
		return (1);
	printf("[%s]\\n", joined);
	free(joined);
	return (0);
}
""",
        tests=[
            [", ", "Hello", "world"],
            ["-", "a", "b", "c"],
            [""],
            ["sep"],
            ["", "ab", "cd"],
            ["--", "single"],
        ],
        hints=[
            "Compute the exact total length first: all the strings plus (size - 1) separators.",
            "With size == 0 you still malloc one byte for the '\\0'.",
            "There is no separator after the last string.",
        ],
    ),
    ex(
        name="ft_split",
        exams={"exam_04": 2},
        kind=FUNCTION,
        allowed=["malloc"],
        prototype="char **ft_split(char *str);",
        subject="""
Write a function that splits str into words and returns them as a
NULL-terminated array of freshly allocated strings.

A word is a sequence of characters that are neither spaces, tabs, nor newlines.
An input with no words yields an array whose first element is NULL.

Return NULL if an allocation fails.
""",
        subject_th="""
เขียนฟังก์ชันที่แยกข้อความ str ออกเป็นคำ แล้วคืนค่าเป็นอาเรย์ของข้อความ
ที่จองหน่วยความจำใหม่ และปิดท้ายอาเรย์ด้วย NULL

คำ หมายถึงลำดับของตัวอักษรที่ไม่ใช่ช่องว่าง ไม่ใช่แท็บ และไม่ใช่การขึ้นบรรทัดใหม่
ถ้าข้อความไม่มีคำใดเลย ให้คืนค่าอาเรย์ที่สมาชิกตัวแรกเป็น NULL

ถ้าจองหน่วยความจำไม่สำเร็จให้คืนค่า NULL
""",
        reference="""
#include <stdlib.h>

static int	is_sep(char c)
{
	return (c == ' ' || c == '\\t' || c == '\\n');
}

static int	count_words(char *str)
{
	int	count;
	int	i;

	count = 0;
	i = 0;
	while (str[i])
	{
		while (str[i] && is_sep(str[i]))
			i++;
		if (str[i])
			count++;
		while (str[i] && !is_sep(str[i]))
			i++;
	}
	return (count);
}

static char	*dup_word(char *start, int len)
{
	char	*word;
	int		i;

	word = malloc(sizeof(char) * (len + 1));
	if (!word)
		return (0);
	i = 0;
	while (i < len)
	{
		word[i] = start[i];
		i++;
	}
	word[i] = '\\0';
	return (word);
}

char	**ft_split(char *str)
{
	char	**out;
	int		i;
	int		start;
	int		w;

	out = malloc(sizeof(char *) * (count_words(str) + 1));
	if (!out)
		return (0);
	i = 0;
	w = 0;
	while (str[i])
	{
		while (str[i] && is_sep(str[i]))
			i++;
		if (!str[i])
			break ;
		start = i;
		while (str[i] && !is_sep(str[i]))
			i++;
		out[w] = dup_word(str + start, i - start);
		if (!out[w])
			return (0);
		w++;
	}
	out[w] = 0;
	return (out);
}
""",
        harness="""
#include <stdio.h>
#include <stdlib.h>

char	**ft_split(char *str);

int	main(int argc, char **argv)
{
	char	**words;
	int		i;

	if (argc != 2)
		return (0);
	words = ft_split(argv[1]);
	if (!words)
		return (1);
	i = 0;
	while (words[i])
	{
		printf("[%s]\\n", words[i]);
		free(words[i]);
		i++;
	}
	printf("count=%d\\n", i);
	free(words);
	return (0);
}
""",
        tests=[
            ["hello world"],
            ["  leading and trailing  "],
            [""],
            ["   "],
            ["one"],
            ["a\tb\nc d"],
            ["multiple   spaces   between"],
        ],
        hints=[
            "Count the words in a first pass so you know how big the char** must be.",
            "Allocate count + 1 pointers -- the last one holds the NULL terminator.",
            "Newlines and tabs are separators here, not just spaces.",
        ],
    ),
    ex(
        name="ft_strrev",
        exams={"exam_02": 6, "exam_03": 1},
        kind=FUNCTION,
        allowed=[],
        prototype="char *ft_strrev(char *str);",
        subject="""
Write a function that reverses a string in place and returns a pointer to it.

The function must not allocate: it swaps the characters of the buffer it was
given.
""",
        subject_th="""
เขียนฟังก์ชันที่กลับลำดับตัวอักษรในข้อความโดยแก้ในบัฟเฟอร์เดิม
แล้วคืนค่าพอยน์เตอร์ที่ชี้ไปยังข้อความนั้น

ฟังก์ชันนี้ต้องไม่จองหน่วยความจำใหม่ ให้สลับตัวอักษรภายในบัฟเฟอร์ที่รับเข้ามา
""",
        reference="""
char	*ft_strrev(char *str)
{
	int		i;
	int		j;
	char	tmp;

	j = 0;
	while (str[j])
		j++;
	j--;
	i = 0;
	while (i < j)
	{
		tmp = str[i];
		str[i] = str[j];
		str[j] = tmp;
		i++;
		j--;
	}
	return (str);
}
""",
        harness="""
#include <stdio.h>

char	*ft_strrev(char *str);

int	main(int argc, char **argv)
{
	int	i;

	i = 1;
	while (i < argc)
	{
		printf("[%s]\\n", ft_strrev(argv[i]));
		i++;
	}
	return (0);
}
""",
        tests=[["hello"], [""], ["a"], ["ab"], ["racecar"], ["42born2code"]],
        hints=[
            "Two indices walking towards each other, swapping as they go.",
            "Stop when they meet -- swapping past the middle undoes your work.",
        ],
    ),
    ex(
        name="expand_str",
        exams={"exam_03": 3, "exam_04": 1},
        kind=PROGRAM,
        allowed=["write"],
        subject="""
Write a program that takes a string and displays it with exactly three spaces
between words, and no leading or trailing whitespace, followed by a newline.

A word is a sequence of characters that are neither spaces nor tabs.

If the number of arguments is not 1, or if the string contains no word, the
program writes only a newline.

Examples:

  $> ./expand_str "  lorem   ipsum  dolor  " | cat -e
  lorem   ipsum   dolor$
  $> ./expand_str "solo" | cat -e
  solo$
""",
        subject_th="""
เขียนโปรแกรมที่รับข้อความหนึ่งชุด แล้วแสดงข้อความนั้นโดยให้มีช่องว่างระหว่างคำ
สามช่องพอดี และไม่มีช่องว่างนำหน้าหรือต่อท้าย ตามด้วยการขึ้นบรรทัดใหม่

คำ หมายถึงลำดับของตัวอักษรที่ไม่ใช่ช่องว่างและไม่ใช่แท็บ

ถ้าจำนวนอาร์กิวเมนต์ไม่เท่ากับ 1 หรือในข้อความไม่มีคำใดเลย
ให้แสดงเฉพาะการขึ้นบรรทัดใหม่

ตัวอย่าง:

  $> ./expand_str "  lorem   ipsum  dolor  " | cat -e
  lorem   ipsum   dolor$
  $> ./expand_str "solo" | cat -e
  solo$
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
				write(1, "   ", 3);
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
            ["solo"],
            [""],
            ["   "],
            ["a\tb"],
            [],
        ],
        hints=[
            "This is epur_str with a 3-byte separator instead of a 1-byte one.",
            "Still no separator before the first word or after the last.",
        ],
    ),
    ex(
        name="add_prime_sum",
        exams={"exam_03": 2, "exam_04": 0},
        kind=PROGRAM,
        allowed=["exit", "write"],
        subject="""
Write a program that takes a positive integer and displays the sum of all prime
numbers less than or equal to it, followed by a newline.

If the number of arguments is not 1, or if the argument is not a valid positive
integer, the program displays 0 followed by a newline.

Examples:

  $> ./add_prime_sum 5 | cat -e
  10$
  $> ./add_prime_sum 7 | cat -e
  17$
""",
        subject_th="""
เขียนโปรแกรมที่รับจำนวนเต็มบวกหนึ่งจำนวน แล้วแสดงผลรวมของจำนวนเฉพาะทุกจำนวน
ที่น้อยกว่าหรือเท่ากับจำนวนนั้น ตามด้วยการขึ้นบรรทัดใหม่

ถ้าจำนวนอาร์กิวเมนต์ไม่เท่ากับ 1 หรืออาร์กิวเมนต์ไม่ใช่จำนวนเต็มบวกที่ถูกต้อง
ให้แสดงเลข 0 ตามด้วยการขึ้นบรรทัดใหม่

ตัวอย่าง:

  $> ./add_prime_sum 5 | cat -e
  10$
  $> ./add_prime_sum 7 | cat -e
  17$
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

static int	is_prime(int n)
{
	int	d;

	if (n < 2)
		return (0);
	d = 2;
	while (d * d <= n)
	{
		if (n % d == 0)
			return (0);
		d++;
	}
	return (1);
}

int	main(int argc, char **argv)
{
	int	limit;
	int	sum;
	int	i;

	limit = 0;
	if (argc == 2)
	{
		i = 0;
		while (argv[1][i] >= '0' && argv[1][i] <= '9')
			limit = limit * 10 + (argv[1][i++] - '0');
		if (argv[1][i] || i == 0)
			limit = 0;
	}
	sum = 0;
	i = 2;
	while (i <= limit)
	{
		if (is_prime(i))
			sum += i;
		i++;
	}
	put_nbr(sum);
	write(1, "\\n", 1);
	return (0);
}
""",
        tests=[["5"], ["7"], ["1"], ["2"], ["0"], ["100"], ["abc"], []],
        hints=[
            "Trial division up to d * d <= n is fast enough and avoids needing sqrt.",
            "1 is not prime, and neither is 0 or any negative number.",
            "Only write is allowed, so you need your own number printer.",
        ],
    ),
    ex(
        name="ft_strspn",
        exams={"exam_02": 7, "exam_03": 1},
        source=ADDED,
        kind=FUNCTION,
        allowed=[],
        prototype="size_t ft_strspn(const char *s, const char *accept);",
        subject="""
Reproduce the behaviour of strspn: return the length of the initial segment of s
that consists entirely of characters from accept.

Examples:

  ft_strspn("42abc", "0123456789")   ->  2
  ft_strspn("abc", "xyz")            ->  0
""",
        subject_th="""
เขียนฟังก์ชันที่ทำงานเหมือน strspn: คืนค่าความยาวของส่วนต้นของข้อความ s
ที่ประกอบด้วยตัวอักษรที่อยู่ใน accept ทั้งหมด

ตัวอย่าง:

  ft_strspn("42abc", "0123456789")   ->  2
  ft_strspn("abc", "xyz")            ->  0
""",
        reference="""
#include <stddef.h>

static int	in_set(char c, const char *set)
{
	int	i;

	i = 0;
	while (set[i])
	{
		if (set[i] == c)
			return (1);
		i++;
	}
	return (0);
}

size_t	ft_strspn(const char *s, const char *accept)
{
	size_t	n;

	n = 0;
	while (s[n] && in_set(s[n], accept))
		n++;
	return (n);
}
""",
        harness="""
#include <stdio.h>

size_t	ft_strspn(const char *s, const char *accept);

int	main(int argc, char **argv)
{
	if (argc != 3)
		return (0);
	printf("%zu\\n", ft_strspn(argv[1], argv[2]));
	return (0);
}
""",
        tests=[
            ["42abc", "0123456789"],
            ["abc", "xyz"],
            ["", "abc"],
            ["abc", ""],
            ["aaabbb", "ab"],
            ["hello", "hel"],
        ],
        hints=[
            "Stop at the first character of s that is NOT in accept.",
            "An empty accept set means the answer is always 0.",
        ],
    ),
    # ------------------------------------------------------------------ level 5
    ex(
        name="ft_atoi_base",
        exams={"exam_03": 3, "exam_04": 1},
        kind=FUNCTION,
        allowed=[],
        prototype="int ft_atoi_base(const char *str, int str_base);",
        subject="""
Write a function that converts the string argument str (base N <= 16) to an
integer (base 10) and returns it.

The characters recognized in the input are: 0123456789abcdef
Those are, of course, to be trimmed according to the requested base. For example,
base 4 recognizes "0123" and base 16 recognizes "0123456789abcdef".

Uppercase letters must also be recognized: "12fdb3" is the same as "12FDB3".

Minus signs ('-') are interpreted only if they are the first character of the
string.

Reading stops at the first character that is not valid for the requested base.
If str_base is less than 2 or greater than 16, the function returns 0.

Examples:

  ft_atoi_base("101", 2)      ->  5
  ft_atoi_base("FF", 16)      ->  255
  ft_atoi_base("-42", 10)     ->  -42
  ft_atoi_base("123", 4)      ->  27
""",
        subject_th="""
เขียนฟังก์ชันที่แปลงข้อความ str ซึ่งเขียนอยู่ในระบบเลขฐาน N (โดย N <= 16)
ให้เป็นจำนวนเต็มฐานสิบ แล้วคืนค่านั้น

อักขระที่รับรู้ในข้อความคือ 0123456789abcdef
โดยตัดให้เหลือเท่าที่ฐานนั้นใช้ ตัวอย่างเช่น ฐาน 4 รับรู้เฉพาะ "0123"
และฐาน 16 รับรู้ "0123456789abcdef"

ต้องรับรู้ตัวพิมพ์ใหญ่ด้วย โดย "12fdb3" มีค่าเท่ากับ "12FDB3"

เครื่องหมายลบ ('-') จะมีผลเฉพาะเมื่ออยู่เป็นอักขระตัวแรกของข้อความเท่านั้น

การอ่านจะหยุดที่อักขระตัวแรกที่ไม่ถูกต้องสำหรับฐานที่กำหนด
และถ้า str_base น้อยกว่า 2 หรือมากกว่า 16 ให้คืนค่า 0

ตัวอย่าง:

  ft_atoi_base("101", 2)      ->  5
  ft_atoi_base("FF", 16)      ->  255
  ft_atoi_base("-42", 10)     ->  -42
  ft_atoi_base("123", 4)      ->  27
""",
        reference="""
static int	digit_value(char c)
{
	if (c >= '0' && c <= '9')
		return (c - '0');
	if (c >= 'a' && c <= 'f')
		return (c - 'a' + 10);
	if (c >= 'A' && c <= 'F')
		return (c - 'A' + 10);
	return (-1);
}

int	ft_atoi_base(const char *str, int str_base)
{
	int	i;
	int	sign;
	int	out;
	int	value;

	if (str_base < 2 || str_base > 16)
		return (0);
	i = 0;
	sign = 1;
	if (str[0] == '-')
	{
		sign = -1;
		i = 1;
	}
	out = 0;
	value = digit_value(str[i]);
	while (value >= 0 && value < str_base)
	{
		out = out * str_base + value;
		i++;
		value = digit_value(str[i]);
	}
	return (out * sign);
}
""",
        harness="""
#include <stdio.h>
#include <stdlib.h>

int	ft_atoi_base(const char *str, int str_base);

int	main(int argc, char **argv)
{
	if (argc != 3)
		return (0);
	printf("%d\\n", ft_atoi_base(argv[1], atoi(argv[2])));
	return (0);
}
""",
        tests=[
            ["101", "2"],
            ["FF", "16"],
            ["ff", "16"],
            ["12fdb3", "16"],
            ["12FDB3", "16"],
            ["-42", "10"],
            ["123", "4"],
            ["0", "10"],
            ["", "10"],
            ["-", "10"],
            ["12a34", "10"],
            ["zzz", "16"],
            ["101", "1"],
            ["101", "17"],
            ["-ff", "16"],
        ],
        hints=[
            "Validate the base first: outside 2..16 the answer is 0.",
            "One digit-value helper handles digits, lowercase and uppercase in one place.",
            "A digit is only valid if its value is LESS than the base -- 'f' is "
            "invalid in base 10.",
            "The minus sign counts only at index 0, so do not loop over signs.",
        ],
    ),
    ex(
        name="ft_sort_string_tab",
        exams={"exam_04": 2},
        source=ADDED,
        kind=FUNCTION,
        allowed=[],
        prototype="void ft_sort_string_tab(char **tab);",
        subject="""
Write a function that sorts a NULL-terminated array of strings into ascending
order, in place, comparing them as strcmp does.

Only the pointers move -- the strings themselves are not modified.
""",
        subject_th="""
เขียนฟังก์ชันที่เรียงลำดับอาเรย์ของข้อความที่ปิดท้ายด้วย NULL
จากน้อยไปมากในตัวอาเรย์เดิม โดยเปรียบเทียบแบบเดียวกับ strcmp

ให้สลับเฉพาะพอยน์เตอร์ ไม่ต้องแก้ไขตัวข้อความ
""",
        reference="""
static int	cmp(char *a, char *b)
{
	int	i;

	i = 0;
	while (a[i] && a[i] == b[i])
		i++;
	return ((unsigned char)a[i] - (unsigned char)b[i]);
}

void	ft_sort_string_tab(char **tab)
{
	int		i;
	char	*tmp;

	if (!tab || !tab[0])
		return ;
	i = 0;
	while (tab[i + 1])
	{
		if (cmp(tab[i], tab[i + 1]) > 0)
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

void	ft_sort_string_tab(char **tab);

int	main(int argc, char **argv)
{
	int	i;

	(void)argc;
	ft_sort_string_tab(argv + 1);
	i = 1;
	while (argv[i])
	{
		printf("%s\\n", argv[i]);
		i++;
	}
	return (0);
}
""",
        tests=[
            ["c", "a", "b"],
            ["banana", "apple", "cherry"],
            ["one"],
            [],
            ["b", "B", "a"],
            ["", "a", ""],
            ["ab", "a"],
        ],
        hints=[
            "argv is already NULL-terminated, which is why it makes a convenient test subject.",
            "Guard against an empty array before you read tab[0].",
            "Swap the pointers, not the string contents.",
        ],
    ),
    ex(
        name="print_memory",
        exams={"exam_04": 3},
        kind=FUNCTION,
        allowed=["write"],
        prototype="void print_memory(const void *addr, size_t size);",
        subject="""
Write a function that dumps `size` bytes starting at addr, 16 bytes per line.

Each line has exactly this shape:

  - the hex column: for each of the 16 bytes, two lowercase hex digits, with a
    single space after every second byte (so eight groups of four hex digits,
    each group followed by a space -- 40 characters in total),
  - the character column: one character per byte, the byte itself if it is
    printable (32 to 126 inclusive), otherwise a dot,
  - a newline.

On a final, incomplete line the hex column is still padded to its full 40
characters, and the character column shows only the bytes that exist.

If size is 0, the function prints nothing.

Example, dumping the 20 bytes of "Bonjour les amin" plus "ches":

  $> ./a.out "Bonjour les aminches" | cat -e
  426f 6e6a 6f75 7220 6c65 7320 616d 696e Bonjour les amin$
  6368 6573                               ches$
""",
        subject_th="""
เขียนฟังก์ชันที่แสดงข้อมูลในหน่วยความจำจำนวน size ไบต์ เริ่มจากตำแหน่ง addr
บรรทัดละ 16 ไบต์

แต่ละบรรทัดมีรูปแบบดังนี้:

  - คอลัมน์เลขฐานสิบหก: แต่ละไบต์ใน 16 ไบต์แสดงด้วยเลขฐานสิบหกตัวพิมพ์เล็ก 2 ตัว
    และเว้นวรรคหนึ่งช่องหลังทุก 2 ไบต์ (ได้ 8 กลุ่ม กลุ่มละ 4 ตัวอักษร
    แต่ละกลุ่มตามด้วยช่องว่าง รวมทั้งหมด 40 ตัวอักษร)
  - คอลัมน์ตัวอักษร: หนึ่งตัวอักษรต่อหนึ่งไบต์ ถ้าไบต์นั้นแสดงผลได้
    (ค่า 32 ถึง 126) ให้แสดงตัวอักษรนั้น ถ้าไม่ได้ให้แสดงจุด
  - แล้วขึ้นบรรทัดใหม่

บรรทัดสุดท้ายที่ไม่ครบ 16 ไบต์ ยังต้องเว้นคอลัมน์เลขฐานสิบหกให้ครบ 40 ตัวอักษร
และคอลัมน์ตัวอักษรแสดงเฉพาะไบต์ที่มีอยู่จริง

ถ้า size เท่ากับ 0 ฟังก์ชันไม่ต้องแสดงอะไรเลย

ตัวอย่าง การแสดงข้อมูล 20 ไบต์ของ "Bonjour les aminches":

  $> ./a.out "Bonjour les aminches" | cat -e
  426f 6e6a 6f75 7220 6c65 7320 616d 696e Bonjour les amin$
  6368 6573                               ches$
""",
        reference="""
#include <unistd.h>

static void	put_hex_byte(unsigned char b)
{
	char	*digits = "0123456789abcdef";

	write(1, &digits[b >> 4], 1);
	write(1, &digits[b & 15], 1);
}

static void	dump_line(const unsigned char *p, size_t count)
{
	size_t	i;
	char	c;

	i = 0;
	while (i < 16)
	{
		if (i < count)
			put_hex_byte(p[i]);
		else
			write(1, "  ", 2);
		if (i % 2 == 1)
			write(1, " ", 1);
		i++;
	}
	i = 0;
	while (i < count)
	{
		c = '.';
		if (p[i] >= 32 && p[i] <= 126)
			c = (char)p[i];
		write(1, &c, 1);
		i++;
	}
	write(1, "\\n", 1);
}

void	print_memory(const void *addr, size_t size)
{
	const unsigned char	*p;
	size_t				done;
	size_t				count;

	p = (const unsigned char *)addr;
	done = 0;
	while (done < size)
	{
		count = size - done;
		if (count > 16)
			count = 16;
		dump_line(p + done, count);
		done += count;
	}
}
""",
        harness="""
#include <stdlib.h>
#include <string.h>

void	print_memory(const void *addr, size_t size);

int	main(int argc, char **argv)
{
	size_t	size;

	if (argc < 2)
		return (0);
	size = strlen(argv[1]);
	if (argc > 2)
		size = (size_t)atoi(argv[2]);
	print_memory(argv[1], size);
	return (0);
}
""",
        tests=[
            ["Bonjour les aminches"],
            ["A"],
            [""],
            ["0123456789abcdef"],
            ["0123456789abcdefg"],
            ["tab\there", "8"],
            ["Bonjour les aminches", "0"],
        ],
        hints=[
            "Work one 16-byte line at a time; the last line is the only special case.",
            "The hex column is always 40 characters: 16 bytes * 2 digits + 8 spaces.",
            "Pad a short line with two spaces per missing byte so the columns still line up.",
            "b >> 4 is the high nibble, b & 15 the low one.",
        ],
    ),
    ex(
        name="lcm",
        exams={"exam_03": 3, "exam_04": 1},
        kind=FUNCTION,
        allowed=[],
        prototype="unsigned int lcm(unsigned int a, unsigned int b);",
        subject="""
Write a function that takes two unsigned int as parameters and returns the
computed LCM of those parameters.

LCM (Lowest Common Multiple) of two non-zero integers is the smallest positive
integer divisible by both integers.

A LCM can be calculated in two ways:

- You can calculate every multiple of each integer until you have a common
  multiple other than 0

- You can use the HCF (Highest Common Factor) of these two integers and
  calculate as follows:

        LCM(x, y) = | x * y | / HCF(x, y)

  | x * y | means "Absolute value of the product of x by y"

If at least one integer is null, LCM is equal to 0.
""",
        subject_th="""
เขียนฟังก์ชันที่รับพารามิเตอร์เป็น unsigned int สองตัว
แล้วคืนค่าตัวคูณร่วมน้อย (LCM) ของสองจำนวนนั้น

ตัวคูณร่วมน้อยของจำนวนเต็มที่ไม่เป็นศูนย์สองจำนวน
คือจำนวนเต็มบวกที่น้อยที่สุดซึ่งหารด้วยทั้งสองจำนวนได้ลงตัว

คำนวณได้สองวิธี:

- ไล่หาพหุคูณของแต่ละจำนวนไปเรื่อย ๆ จนพบพหุคูณร่วมที่ไม่ใช่ 0

- ใช้ตัวหารร่วมมาก (HCF) ของสองจำนวนนั้น แล้วคำนวณตามสูตร:

        LCM(x, y) = | x * y | / HCF(x, y)

  โดย | x * y | หมายถึงค่าสัมบูรณ์ของผลคูณของ x กับ y

ถ้ามีจำนวนใดจำนวนหนึ่งเป็นศูนย์ ค่า LCM จะเท่ากับ 0
""",
        reference="""
unsigned int	lcm(unsigned int a, unsigned int b)
{
	unsigned int	x;
	unsigned int	y;
	unsigned int	tmp;

	if (a == 0 || b == 0)
		return (0);
	x = a;
	y = b;
	while (y != 0)
	{
		tmp = y;
		y = x % y;
		x = tmp;
	}
	return (a / x * b);
}
""",
        harness="""
#include <stdio.h>
#include <stdlib.h>

unsigned int	lcm(unsigned int a, unsigned int b);

int	main(int argc, char **argv)
{
	unsigned int	a;
	unsigned int	b;

	if (argc != 3)
		return (0);
	a = (unsigned int)strtoul(argv[1], 0, 10);
	b = (unsigned int)strtoul(argv[2], 0, 10);
	printf("%u\\n", lcm(a, b));
	return (0);
}
""",
        tests=[
            ["4", "6"],
            ["3", "7"],
            ["10", "10"],
            ["1", "5"],
            ["0", "5"],
            ["5", "0"],
            ["0", "0"],
            ["12", "18"],
        ],
        hints=[
            "Nothing is allowed here -- not even write. Just compute and return.",
            "Divide before you multiply (a / hcf * b) so the value cannot overflow "
            "as easily.",
            "Handle the zero cases first: the answer is 0, not a division by zero.",
        ],
    ),
]
