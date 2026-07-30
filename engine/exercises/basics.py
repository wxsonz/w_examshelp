"""The bottom of the exam_01 ladder -- levels 1 to 6 of the first exam.

These eight are where a learner actually starts, and the pack used to skip most
of them: of the eleven easiest exercises in the 2026 pool it shipped five. Every
subject and placement here is taken from references/PISCINE_PART; every
reference solution is written by hand, because the corpus solutions are not
trustworthy (a fifth of them do not survive -Wall -Wextra -Werror).
"""

from engine.exercises.spec import ex, PROGRAM, FUNCTION

EXERCISES = [
    # ------------------------------------------------------------ exam_01 / 1
    ex(
        name="maff_alpha",
        exams={"exam_01": 1},
        kind=PROGRAM,
        allowed=["write"],
        subject="""
Write a program that displays the alphabet, with even letters in uppercase and
odd letters in lowercase, followed by a newline.

Letters are counted from 1, so 'a' is the first letter -- odd, and therefore
lowercase.

Example:

  $> ./maff_alpha | cat -e
  aBcDeFgHiJkLmNoPqRsTuVwXyZ$
""",
        subject_th="""
เขียนโปรแกรมที่แสดงตัวอักษร a ถึง z โดยให้ตัวอักษรลำดับคู่เป็นตัวพิมพ์ใหญ่
และตัวอักษรลำดับคี่เป็นตัวพิมพ์เล็ก แล้วขึ้นบรรทัดใหม่

การนับลำดับเริ่มจาก 1 ดังนั้น a คือตัวที่ 1 ซึ่งเป็นลำดับคี่ จึงเป็นตัวพิมพ์เล็ก

ตัวอย่าง:

  $> ./maff_alpha | cat -e
  aBcDeFgHiJkLmNoPqRsTuVwXyZ$
""",
        reference="""
#include <unistd.h>

int	main(void)
{
	char	c;
	int	i;

	i = 0;
	while (i < 26)
	{
		c = 'a' + i;
		if (i % 2)
			c = c - 32;
		write(1, &c, 1);
		i++;
	}
	write(1, "\\n", 1);
	return (0);
}
""",
        tests=[[], ["ignored"]],
        hints=[
            "'a' + i walks the alphabet; you never need to write the 26 letters out.",
            "Uppercase is lowercase minus 32 in ASCII.",
            "Watch the parity: the FIRST letter stays lowercase, so it is the "
            "odd-numbered ones that are left alone.",
        ],
    ),
    # ------------------------------------------------------------ exam_01 / 2
    ex(
        name="aff_first_param",
        exams={"exam_01": 2},
        kind=PROGRAM,
        allowed=["write"],
        subject="""
Write a program that takes strings as arguments and displays its first argument
followed by a newline.

If it receives no arguments, the program displays only a newline.

Examples:

  $> ./aff_first_param vincent mit "l'ane" dans un pre et "s'en" vint | cat -e
  vincent$
  $> ./aff_first_param "j'aime le fromage de chevre" | cat -e
  j'aime le fromage de chevre$
  $> ./aff_first_param | cat -e
  $
""",
        subject_th="""
เขียนโปรแกรมที่รับข้อความเป็นอาร์กิวเมนต์ แล้วแสดงอาร์กิวเมนต์ตัวแรก
ตามด้วยการขึ้นบรรทัดใหม่

ถ้าไม่ได้รับอาร์กิวเมนต์เลย ให้แสดงเฉพาะการขึ้นบรรทัดใหม่

ตัวอย่าง:

  $> ./aff_first_param vincent mit "l'ane" dans un pre et "s'en" vint | cat -e
  vincent$
  $> ./aff_first_param "j'aime le fromage de chevre" | cat -e
  j'aime le fromage de chevre$
  $> ./aff_first_param | cat -e
  $
""",
        reference="""
#include <unistd.h>

int	main(int argc, char **argv)
{
	int	i;

	if (argc > 1)
	{
		i = 0;
		while (argv[1][i])
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
            ["vincent", "mit", "l'ane", "dans", "un", "pre", "et", "s'en", "vint"],
            ["j'aime le fromage de chevre"],
            [],
            [""],
            ["first", "second"],
        ],
        hints=[
            "The first argument is argv[1] -- argv[0] is the program's own name.",
            "The newline is printed in every case, including the no-argument one, "
            "so write it after the branch rather than inside it.",
        ],
    ),
    ex(
        name="aff_last_param",
        exams={"exam_01": 2},
        kind=PROGRAM,
        allowed=["write"],
        subject="""
Write a program that takes strings as arguments and displays its last argument
followed by a newline.

If it receives no arguments, the program displays only a newline.

Examples:

  $> ./aff_last_param "zaz" "mange" "des" "chats" | cat -e
  chats$
  $> ./aff_last_param "j'aime le savon" | cat -e
  j'aime le savon$
  $> ./aff_last_param | cat -e
  $
""",
        subject_th="""
เขียนโปรแกรมที่รับข้อความเป็นอาร์กิวเมนต์ แล้วแสดงอาร์กิวเมนต์ตัวสุดท้าย
ตามด้วยการขึ้นบรรทัดใหม่

ถ้าไม่ได้รับอาร์กิวเมนต์เลย ให้แสดงเฉพาะการขึ้นบรรทัดใหม่

ตัวอย่าง:

  $> ./aff_last_param "zaz" "mange" "des" "chats" | cat -e
  chats$
  $> ./aff_last_param "j'aime le savon" | cat -e
  j'aime le savon$
  $> ./aff_last_param | cat -e
  $
""",
        reference="""
#include <unistd.h>

int	main(int argc, char **argv)
{
	int	i;

	if (argc > 1)
	{
		i = 0;
		while (argv[argc - 1][i])
		{
			write(1, &argv[argc - 1][i], 1);
			i++;
		}
	}
	write(1, "\\n", 1);
	return (0);
}
""",
        tests=[
            ["zaz", "mange", "des", "chats"],
            ["j'aime le savon"],
            [],
            [""],
            ["first", "second", "third"],
        ],
        hints=[
            "The last argument is argv[argc - 1]; with one argument that is also "
            "argv[1], which is why the single-argument case needs no special code.",
            "argc counts the program name, so argc == 1 means no arguments at all.",
        ],
    ),
    # ------------------------------------------------------------ exam_01 / 3
    ex(
        name="maff_revalpha",
        exams={"exam_01": 3},
        kind=PROGRAM,
        allowed=["write"],
        subject="""
Write a program that displays the alphabet in reverse, with even letters in
uppercase and odd letters in lowercase, followed by a newline.

Letters are counted from 1 in the order they are printed, so 'z' comes first --
odd, and therefore lowercase.

Example:

  $> ./maff_revalpha | cat -e
  zYxWvUtSrQpOnMlKjIhGfEdCbA$
""",
        subject_th="""
เขียนโปรแกรมที่แสดงตัวอักษรจาก z ย้อนกลับไปถึง a โดยให้ตัวอักษรลำดับคู่เป็นตัวพิมพ์ใหญ่
และตัวอักษรลำดับคี่เป็นตัวพิมพ์เล็ก แล้วขึ้นบรรทัดใหม่

การนับลำดับเริ่มจาก 1 ตามลำดับที่แสดงออกมา ดังนั้น z คือตัวที่ 1 ซึ่งเป็นลำดับคี่
จึงเป็นตัวพิมพ์เล็ก

ตัวอย่าง:

  $> ./maff_revalpha | cat -e
  zYxWvUtSrQpOnMlKjIhGfEdCbA$
""",
        reference="""
#include <unistd.h>

int	main(void)
{
	char	c;
	int	i;

	i = 0;
	while (i < 26)
	{
		c = 'z' - i;
		if (i % 2)
			c = c - 32;
		write(1, &c, 1);
		i++;
	}
	write(1, "\\n", 1);
	return (0);
}
""",
        tests=[[], ["ignored"]],
        hints=[
            "This is maff_alpha counting down: 'z' - i instead of 'a' + i.",
            "The parity follows the printing order, not the alphabet, so the last "
            "letter printed ('a') comes out uppercase.",
        ],
    ),
    # only_a and only_z print NO trailing newline. The subject is silent about
    # it; the exam's own reference solution is a single write(1, "a", 1), which
    # is what settles it. Do not "fix" this by adding a newline.
    ex(
        name="only_a",
        exams={"exam_01": 3},
        kind=PROGRAM,
        allowed=["write"],
        subject="""
Write a program that displays the character 'a' on the standard output.

The output is exactly one byte. There is no newline at the end -- this is one of
the very few subjects that does not finish with one.

  ./only_a | cat -e   prints   a     (a bare 'a', with no trailing '$', because
                                      there is no newline to mark)
""",
        subject_th="""
เขียนโปรแกรมที่แสดงตัวอักษร 'a' ออกทางเอาต์พุตมาตรฐาน

ผลลัพธ์มีความยาวหนึ่งไบต์พอดี และไม่มีการขึ้นบรรทัดใหม่ต่อท้าย
ข้อนี้เป็นหนึ่งในไม่กี่ข้อที่ไม่จบด้วยการขึ้นบรรทัดใหม่

  ./only_a | cat -e   ได้   a     (มีแค่ตัว a ไม่มีเครื่องหมาย $ ต่อท้าย
                                   เพราะไม่มีการขึ้นบรรทัดใหม่ให้ cat -e แสดง)
""",
        reference="""
#include <unistd.h>

int	main(void)
{
	write(1, "a", 1);
	return (0);
}
""",
        tests=[[], ["ignored"]],
        hints=[
            "One call to write, one byte, and nothing else.",
            "Resist the reflex to add '\\n' -- here it would be a wrong answer.",
        ],
    ),
    ex(
        name="only_z",
        exams={"exam_01": 3},
        kind=PROGRAM,
        allowed=["write"],
        subject="""
Write a program that displays the character 'z' on the standard output.

The output is exactly one byte. There is no newline at the end -- this is one of
the very few subjects that does not finish with one.

  ./only_z | cat -e   prints   z     (a bare 'z', with no trailing '$', because
                                      there is no newline to mark)
""",
        subject_th="""
เขียนโปรแกรมที่แสดงตัวอักษร 'z' ออกทางเอาต์พุตมาตรฐาน

ผลลัพธ์มีความยาวหนึ่งไบต์พอดี และไม่มีการขึ้นบรรทัดใหม่ต่อท้าย
ข้อนี้เป็นหนึ่งในไม่กี่ข้อที่ไม่จบด้วยการขึ้นบรรทัดใหม่

  ./only_z | cat -e   ได้   z     (มีแค่ตัว z ไม่มีเครื่องหมาย $ ต่อท้าย
                                   เพราะไม่มีการขึ้นบรรทัดใหม่ให้ cat -e แสดง)
""",
        reference="""
#include <unistd.h>

int	main(void)
{
	write(1, "z", 1);
	return (0);
}
""",
        tests=[[], ["ignored"]],
        hints=[
            "One call to write, one byte, and nothing else.",
            "Resist the reflex to add '\\n' -- here it would be a wrong answer.",
        ],
    ),
    # ------------------------------------------------------------ exam_01 / 5
    ex(
        name="search_and_replace",
        exams={"exam_01": 5, "exam_02": 1},
        kind=PROGRAM,
        allowed=["write", "exit"],
        subject="""
Write a program called search_and_replace that takes three arguments: a string,
the character to search for, and the character to replace it with.

It displays the string with every occurrence of the second argument replaced by
the third, followed by a newline.

If the number of arguments is not 3, the program displays only a newline. The
same happens if the search or the replacement argument is not exactly one
character long -- "art" is not a character.

If the search character does not appear in the string, the string is simply
rewritten unchanged.

Examples:

  $> ./search_and_replace "Papache est un sabre" "a" "o" | cat -e
  Popoche est un sobre$
  $> ./search_and_replace "zaz" "art" "zul" | cat -e
  $
  $> ./search_and_replace "zaz" "r" "u" | cat -e
  zaz$
  $> ./search_and_replace "jacob" "a" "b" "c" "e" | cat -e
  $
  $> ./search_and_replace "ZoZ eT Dovid oiME le METol." "o" "a" | cat -e
  ZaZ eT David aiME le METal.$
""",
        subject_th="""
เขียนโปรแกรมชื่อ search_and_replace ที่รับอาร์กิวเมนต์สามตัว ได้แก่ ข้อความ
ตัวอักษรที่ต้องการค้นหา และตัวอักษรที่ต้องการนำไปแทนที่

โปรแกรมจะแสดงข้อความนั้นโดยแทนที่ตัวอักษรตัวที่สองทุกตำแหน่งด้วยตัวอักษรตัวที่สาม
แล้วขึ้นบรรทัดใหม่

ถ้าจำนวนอาร์กิวเมนต์ไม่เท่ากับ 3 ให้แสดงเฉพาะการขึ้นบรรทัดใหม่
และถ้าอาร์กิวเมนต์ตัวที่สองหรือตัวที่สามยาวไม่ใช่หนึ่งตัวอักษรพอดี ก็ให้ทำแบบเดียวกัน
เพราะ "art" ไม่ใช่ตัวอักษรตัวเดียว

ถ้าไม่พบตัวอักษรที่ค้นหาในข้อความ ให้แสดงข้อความเดิมตามที่เป็นอยู่

ตัวอย่าง:

  $> ./search_and_replace "Papache est un sabre" "a" "o" | cat -e
  Popoche est un sobre$
  $> ./search_and_replace "zaz" "art" "zul" | cat -e
  $
  $> ./search_and_replace "zaz" "r" "u" | cat -e
  zaz$
  $> ./search_and_replace "jacob" "a" "b" "c" "e" | cat -e
  $
  $> ./search_and_replace "ZoZ eT Dovid oiME le METol." "o" "a" | cat -e
  ZaZ eT David aiME le METal.$
""",
        # argv[2][0] is tested before argv[2][1] on purpose: for an empty
        # argument, reading index 1 would be one byte past the end.
        reference="""
#include <unistd.h>

int	main(int argc, char **argv)
{
	int	i;

	if (argc != 4
		|| !argv[2][0] || argv[2][1]
		|| !argv[3][0] || argv[3][1])
	{
		write(1, "\\n", 1);
		return (0);
	}
	i = 0;
	while (argv[1][i])
	{
		if (argv[1][i] == argv[2][0])
			write(1, argv[3], 1);
		else
			write(1, &argv[1][i], 1);
		i++;
	}
	write(1, "\\n", 1);
	return (0);
}
""",
        tests=[
            ["Papache est un sabre", "a", "o"],
            ["zaz", "art", "zul"],
            ["zaz", "r", "u"],
            ["jacob", "a", "b", "c", "e"],
            ["ZoZ eT Dovid oiME le METol.", "o", "a"],
            [],
            ["abc", "", ""],
            ["aaa", "a", "a"],
            ["", "a", "b"],
        ],
        hints=[
            "Three arguments means argc == 4: argv[0] is the program name.",
            "A single-character argument is one whose argv[n][1] is '\\0' -- but "
            "check argv[n][0] first, or an empty argument sends you one byte past "
            "the end of the string.",
            "You do not have to build a new string: walk the original and write "
            "either the original byte or the replacement.",
        ],
    ),
    # ------------------------------------------------------------ exam_01 / 6
    ex(
        name="ft_putstr",
        exams={"exam_01": 6, "exam_02": 2},
        kind=FUNCTION,
        allowed=["write"],
        prototype="void ft_putstr(char *str);",
        subject="""
Write a function that displays a string on the standard output.

The pointer passed to the function holds the address of the string's first
character.

The function adds nothing of its own: no newline, no return value. An empty
string displays nothing at all.
""",
        subject_th="""
เขียนฟังก์ชันที่แสดงข้อความออกทางเอาต์พุตมาตรฐาน

พอยน์เตอร์ที่ส่งเข้ามาเก็บตำแหน่งของตัวอักษรตัวแรกในข้อความนั้น

ฟังก์ชันนี้ไม่ต้องเพิ่มอะไรเองทั้งสิ้น ไม่ต้องขึ้นบรรทัดใหม่ และไม่ต้องคืนค่าใด ๆ
ถ้าข้อความว่าง ก็ไม่ต้องแสดงอะไรเลย
""",
        reference="""
#include <unistd.h>

void	ft_putstr(char *str)
{
	int	i;

	i = 0;
	while (str[i])
	{
		write(1, &str[i], 1);
		i++;
	}
}
""",
        # The corpus harness calls ft_putstr(argv[1]) without looking at argc,
        # which segfaults when the program is run with no arguments. This one
        # loops over the arguments it actually has.
        harness="""
#include <unistd.h>

void	ft_putstr(char *str);

int	main(int argc, char **argv)
{
	int	i;

	i = 1;
	while (i < argc)
	{
		ft_putstr(argv[i]);
		write(1, "\\n", 1);
		i++;
	}
	return (0);
}
""",
        tests=[
            ["hello"],
            ["42"],
            [""],
            ["one", "two", "three"],
            ["  spaces kept  "],
        ],
        hints=[
            "Stop at the '\\0'; it is not part of the string and must not be "
            "written.",
            "write() takes an address, so pass &str[i] -- not str[i], which is a "
            "single char value.",
            "The grader supplies main(), so your file must not define one.",
        ],
    ),
]
