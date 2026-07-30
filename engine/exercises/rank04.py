"""Exam Rank 04 / 05 pool -- levels 6 to 9.

The ft_list_* family is why the grader had to learn about include paths: these
exercises ship a header that the *student* writes, and the test harness has to
include the student's copy. The previous engine declared `t_list` in a generated
wrapper without including anything, so every one of these was unpassable.

The linked list used throughout is the standard one:

    typedef struct s_list
    {
        struct s_list *next;
        void          *data;
    } t_list;
"""

from engine.exercises.spec import ex, ADDED, EXTRA, PISCINE_2026, PROGRAM, FUNCTION

FT_LIST_H = """
#ifndef FT_LIST_H
# define FT_LIST_H

typedef struct s_list
{
	struct s_list	*next;
	void			*data;
}	t_list;

#endif
"""

_LIST_STRUCT_EN = """
You must also submit ft_list.h, defining the list type:

  typedef struct s_list
  {
      struct s_list *next;
      void          *data;
  } t_list;
"""

_LIST_STRUCT_TH = """
คุณต้องส่งไฟล์ ft_list.h ที่นิยามชนิดข้อมูลของลิสต์ด้วย:

  typedef struct s_list
  {
      struct s_list *next;
      void          *data;
  } t_list;
"""

# Every list harness needs the same scaffolding to build and print a list. Not
# every harness uses all three helpers, hence the unused attribute -- otherwise
# -Werror=unused-function rejects the build.
_LIST_HARNESS_PRELUDE = """
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ft_list.h"

__attribute__((unused)) static t_list	*new_node(void *data)
{
	t_list	*node;

	node = malloc(sizeof(t_list));
	node->data = data;
	node->next = 0;
	return (node);
}

__attribute__((unused)) static t_list	*build_list(int count, char **items)
{
	t_list	*head;
	t_list	**tail;
	int		i;

	head = 0;
	tail = &head;
	i = 0;
	while (i < count)
	{
		*tail = new_node(items[i]);
		tail = &(*tail)->next;
		i++;
	}
	return (head);
}

__attribute__((unused)) static void	print_list(t_list *list)
{
	while (list)
	{
		printf("[%s]", (char *)list->data);
		list = list->next;
	}
	printf("\\n");
}
"""


def _list_exercise(name, exams, prototype, subject, subject_th, reference, harness,
                   stub_body, tests, hints, allowed, source=PISCINE_2026):
    """Build one ft_list_* exercise, wiring in the shared header and prelude."""
    return ex(
        name=name,
        exams=exams,
        source=source,
        kind=FUNCTION,
        allowed=allowed,
        prototype=prototype,
        files=[f"{name}.c", "ft_list.h"],
        subject=subject.rstrip() + "\n" + _LIST_STRUCT_EN,
        subject_th=subject_th.rstrip() + "\n" + _LIST_STRUCT_TH,
        reference={f"{name}.c": reference, "ft_list.h": FT_LIST_H},
        harness=_LIST_HARNESS_PRELUDE + harness,
        stub='#include "ft_list.h"\n\n' + stub_body,
        tests=tests,
        hints=hints,
    )


EXERCISES = [
    # ------------------------------------------------------------------ level 6
    _list_exercise(
        name="ft_list_size",
        exams={"exam_03": 2, "exam_04": 0},
        prototype="int ft_list_size(t_list *begin_list);",
        allowed=[],
        subject="""
Write a function that counts and returns the number of elements in the list.

An empty list (a NULL pointer) has 0 elements.
""",
        subject_th="""
เขียนฟังก์ชันที่นับและคืนค่าจำนวนสมาชิกในลิสต์

ลิสต์ว่าง (พอยน์เตอร์ที่เป็น NULL) มีสมาชิก 0 ตัว
""",
        reference="""
#include "ft_list.h"

int	ft_list_size(t_list *begin_list)
{
	int	count;

	count = 0;
	while (begin_list)
	{
		count++;
		begin_list = begin_list->next;
	}
	return (count);
}
""",
        harness="""
int	ft_list_size(t_list *begin_list);

int	main(int argc, char **argv)
{
	printf("%d\\n", ft_list_size(build_list(argc - 1, argv + 1)));
	return (0);
}
""",
        stub_body="""
int	ft_list_size(t_list *begin_list)
{
	(void)begin_list;
	return (0);
}
""",
        tests=[["a", "b", "c"], ["only"], [], ["1", "2", "3", "4", "5"]],
        hints=[
            "Walk the list with a local pointer; do not modify begin_list itself.",
            "The loop condition is the NULL check -- no separate empty-list case needed.",
        ],
    ),
    _list_exercise(
        name="ft_list_push_front",
        exams={"exam_03": 2, "exam_04": 0},
        source=ADDED,
        prototype="void ft_list_push_front(t_list **begin_list, void *data);",
        allowed=["malloc"],
        subject="""
Write a function that adds a new element holding `data` at the FRONT of the list,
and updates the caller's head pointer to point at it.

The list may be empty, in which case *begin_list is NULL.
""",
        subject_th="""
เขียนฟังก์ชันที่เพิ่มสมาชิกใหม่ซึ่งเก็บข้อมูล data ไว้ที่ต้นลิสต์
แล้วปรับพอยน์เตอร์หัวลิสต์ของผู้เรียกให้ชี้มาที่สมาชิกใหม่นั้น

ลิสต์อาจเป็นลิสต์ว่างได้ ซึ่งในกรณีนั้น *begin_list จะเป็น NULL
""",
        reference="""
#include <stdlib.h>
#include "ft_list.h"

void	ft_list_push_front(t_list **begin_list, void *data)
{
	t_list	*node;

	node = malloc(sizeof(t_list));
	if (!node)
		return ;
	node->data = data;
	node->next = *begin_list;
	*begin_list = node;
}
""",
        harness="""
void	ft_list_push_front(t_list **begin_list, void *data);

int	main(int argc, char **argv)
{
	t_list	*list;
	int		i;

	list = 0;
	i = 1;
	while (i < argc)
	{
		ft_list_push_front(&list, argv[i]);
		i++;
	}
	print_list(list);
	return (0);
}
""",
        stub_body="""
void	ft_list_push_front(t_list **begin_list, void *data)
{
	(void)begin_list;
	(void)data;
}
""",
        tests=[["a", "b", "c"], ["only"], [], ["1", "2"]],
        hints=[
            "The new node's next is the OLD head, then the head becomes the new node.",
            "You need t_list ** so that the caller's own pointer is updated.",
        ],
    ),
    _list_exercise(
        name="ft_list_push_back",
        exams={"exam_03": 2, "exam_04": 0},
        source=ADDED,
        prototype="void ft_list_push_back(t_list **begin_list, void *data);",
        allowed=["malloc"],
        subject="""
Write a function that adds a new element holding `data` at the END of the list.

If the list is empty, the new element becomes the head, so the caller's pointer
must be updated.
""",
        subject_th="""
เขียนฟังก์ชันที่เพิ่มสมาชิกใหม่ซึ่งเก็บข้อมูล data ไว้ที่ท้ายลิสต์

ถ้าลิสต์ว่าง สมาชิกใหม่จะกลายเป็นหัวลิสต์
ดังนั้นต้องปรับพอยน์เตอร์ของผู้เรียกด้วย
""",
        reference="""
#include <stdlib.h>
#include "ft_list.h"

void	ft_list_push_back(t_list **begin_list, void *data)
{
	t_list	*node;
	t_list	*cursor;

	node = malloc(sizeof(t_list));
	if (!node)
		return ;
	node->data = data;
	node->next = 0;
	if (!*begin_list)
	{
		*begin_list = node;
		return ;
	}
	cursor = *begin_list;
	while (cursor->next)
		cursor = cursor->next;
	cursor->next = node;
}
""",
        harness="""
void	ft_list_push_back(t_list **begin_list, void *data);

int	main(int argc, char **argv)
{
	t_list	*list;
	int		i;

	list = 0;
	i = 1;
	while (i < argc)
	{
		ft_list_push_back(&list, argv[i]);
		i++;
	}
	print_list(list);
	return (0);
}
""",
        stub_body="""
void	ft_list_push_back(t_list **begin_list, void *data)
{
	(void)begin_list;
	(void)data;
}
""",
        tests=[["a", "b", "c"], ["only"], [], ["1", "2"]],
        hints=[
            "Handle the empty list first, or you will dereference NULL.",
            "Walk to the node whose next is NULL -- that is the last one.",
        ],
    ),
    _list_exercise(
        name="ft_list_at",
        exams={"exam_03": 2, "exam_04": 0},
        source=ADDED,
        prototype="t_list *ft_list_at(t_list *begin_list, unsigned int nbr);",
        allowed=[],
        subject="""
Write a function that returns the element at index nbr in the list, counting the
head as index 0.

If there is no such element, return NULL.
""",
        subject_th="""
เขียนฟังก์ชันที่คืนค่าสมาชิกที่ตำแหน่ง nbr ในลิสต์ โดยนับหัวลิสต์เป็นตำแหน่งที่ 0

ถ้าไม่มีสมาชิกที่ตำแหน่งนั้น ให้คืนค่า NULL
""",
        reference="""
#include "ft_list.h"

t_list	*ft_list_at(t_list *begin_list, unsigned int nbr)
{
	unsigned int	i;

	i = 0;
	while (begin_list)
	{
		if (i == nbr)
			return (begin_list);
		begin_list = begin_list->next;
		i++;
	}
	return (0);
}
""",
        harness="""
t_list	*ft_list_at(t_list *begin_list, unsigned int nbr);

int	main(int argc, char **argv)
{
	t_list			*list;
	t_list			*found;
	unsigned int	index;

	if (argc < 2)
		return (0);
	index = (unsigned int)atoi(argv[1]);
	list = build_list(argc - 2, argv + 2);
	found = ft_list_at(list, index);
	if (found)
		printf("[%s]\\n", (char *)found->data);
	else
		printf("(null)\\n");
	return (0);
}
""",
        stub_body="""
t_list	*ft_list_at(t_list *begin_list, unsigned int nbr)
{
	(void)begin_list;
	(void)nbr;
	return (0);
}
""",
        tests=[
            ["0", "a", "b", "c"],
            ["2", "a", "b", "c"],
            ["3", "a", "b", "c"],
            ["0"],
            ["1", "only"],
        ],
        hints=[
            "Index 0 is the head, so compare before you advance.",
            "Running off the end means returning NULL, not the last element.",
        ],
    ),
    _list_exercise(
        name="ft_list_reverse",
        exams={"exam_03": 3, "exam_04": 1},
        source=ADDED,
        prototype="void ft_list_reverse(t_list **begin_list);",
        allowed=[],
        subject="""
Write a function that reverses the order of the elements of the list, in place,
and updates the caller's head pointer.

No node is allocated or freed -- only the next pointers change.
""",
        subject_th="""
เขียนฟังก์ชันที่กลับลำดับสมาชิกของลิสต์ในตัวลิสต์เดิม
แล้วปรับพอยน์เตอร์หัวลิสต์ของผู้เรียกด้วย

ห้ามจองหรือคืนหน่วยความจำใด ให้เปลี่ยนเฉพาะพอยน์เตอร์ next
""",
        reference="""
#include "ft_list.h"

void	ft_list_reverse(t_list **begin_list)
{
	t_list	*prev;
	t_list	*cursor;
	t_list	*next;

	prev = 0;
	cursor = *begin_list;
	while (cursor)
	{
		next = cursor->next;
		cursor->next = prev;
		prev = cursor;
		cursor = next;
	}
	*begin_list = prev;
}
""",
        harness="""
void	ft_list_reverse(t_list **begin_list);

int	main(int argc, char **argv)
{
	t_list	*list;

	list = build_list(argc - 1, argv + 1);
	ft_list_reverse(&list);
	print_list(list);
	return (0);
}
""",
        stub_body="""
void	ft_list_reverse(t_list **begin_list)
{
	(void)begin_list;
}
""",
        tests=[["a", "b", "c"], ["only"], [], ["1", "2", "3", "4"]],
        hints=[
            "Three pointers: previous, current, and the next you saved before overwriting.",
            "Save cursor->next BEFORE you point cursor->next backwards.",
            "The head ends up being the last node you visited.",
        ],
    ),
    # ------------------------------------------------------------------ level 7
    _list_exercise(
        name="ft_list_foreach",
        exams={"exam_04": 2},
        prototype="void ft_list_foreach(t_list *begin_list, void (*f)(void *));",
        allowed=[],
        subject="""
Write a function that applies the function f to the data of every element of the
list, in order, from the head onwards.
""",
        subject_th="""
เขียนฟังก์ชันที่เรียกใช้ฟังก์ชัน f กับข้อมูลของสมาชิกทุกตัวในลิสต์
โดยไล่ตามลำดับจากหัวลิสต์ไปท้ายลิสต์
""",
        reference="""
#include "ft_list.h"

void	ft_list_foreach(t_list *begin_list, void (*f)(void *))
{
	while (begin_list)
	{
		f(begin_list->data);
		begin_list = begin_list->next;
	}
}
""",
        harness="""
void	ft_list_foreach(t_list *begin_list, void (*f)(void *));

static void	shout(void *data)
{
	printf("<%s>", (char *)data);
}

int	main(int argc, char **argv)
{
	ft_list_foreach(build_list(argc - 1, argv + 1), &shout);
	printf("\\n");
	return (0);
}
""",
        stub_body="""
void	ft_list_foreach(t_list *begin_list, void (*f)(void *))
{
	(void)begin_list;
	(void)f;
}
""",
        tests=[["a", "b", "c"], ["only"], [], ["1", "2"]],
        hints=[
            "Call f on the DATA, not on the node.",
            "f(begin_list->data) is how you invoke a function pointer -- no extra syntax needed.",
        ],
    ),
    _list_exercise(
        name="ft_list_remove_if",
        exams={"exam_04": 2},
        prototype="void ft_list_remove_if(t_list **begin_list, void *data_ref, int (*cmp)());",
        allowed=["free"],
        subject="""
Write a function that removes from the list every element whose data is
considered equal to data_ref, and frees the removed nodes with free().

Two data are equal when cmp returns 0, the same convention strcmp uses.

The head may itself be removed, so the caller's pointer must be updated. The
data pointed to by the nodes must NOT be freed -- only the nodes.

Note the prototype: `int (*cmp)()` really is written without parameter types,
exactly as the exam gives it. Declare it that way -- if you write
`int (*cmp)(void *, void *)` instead, your definition conflicts with the
grader's declaration and will not compile.
""",
        subject_th="""
เขียนฟังก์ชันที่ลบสมาชิกทุกตัวที่มีข้อมูลเทียบเท่ากับ data_ref ออกจากลิสต์
และคืนหน่วยความจำของสมาชิกที่ลบด้วย free()

ข้อมูลสองชุดถือว่าเท่ากันเมื่อ cmp คืนค่า 0 ซึ่งเป็นแบบเดียวกับ strcmp

หัวลิสต์เองก็อาจถูกลบได้ ดังนั้นต้องปรับพอยน์เตอร์ของผู้เรียกด้วย
และห้ามคืนหน่วยความจำของข้อมูลที่สมาชิกชี้อยู่ ให้คืนเฉพาะตัวสมาชิกเท่านั้น

สังเกตต้นแบบฟังก์ชัน: `int (*cmp)()` เขียนโดยไม่ระบุชนิดพารามิเตอร์จริง ๆ
ตามที่ข้อสอบให้มา ให้ประกาศแบบนั้น ถ้าเขียนเป็น `int (*cmp)(void *, void *)`
จะขัดแย้งกับการประกาศของตัวตรวจ และคอมไพล์ไม่ผ่าน
""",
        reference="""
#include <stdlib.h>
#include "ft_list.h"

void	ft_list_remove_if(t_list **begin_list, void *data_ref, int (*cmp)())
{
	t_list	*cursor;
	t_list	*doomed;

	while (*begin_list && cmp((*begin_list)->data, data_ref) == 0)
	{
		doomed = *begin_list;
		*begin_list = doomed->next;
		free(doomed);
	}
	cursor = *begin_list;
	while (cursor && cursor->next)
	{
		if (cmp(cursor->next->data, data_ref) == 0)
		{
			doomed = cursor->next;
			cursor->next = doomed->next;
			free(doomed);
		}
		else
			cursor = cursor->next;
	}
}
""",
        harness="""
void	ft_list_remove_if(t_list **begin_list, void *data_ref, int (*cmp)());

static int	cmp_str(void *a, void *b)
{
	return (strcmp((char *)a, (char *)b));
}

int	main(int argc, char **argv)
{
	t_list	*list;

	if (argc < 2)
		return (0);
	list = build_list(argc - 2, argv + 2);
	ft_list_remove_if(&list, argv[1], &cmp_str);
	print_list(list);
	return (0);
}
""",
        stub_body="""
void	ft_list_remove_if(t_list **begin_list, void *data_ref, int (*cmp)())
{
	(void)begin_list;
	(void)data_ref;
	(void)cmp;
}
""",
        tests=[
            ["b", "a", "b", "c"],
            ["a", "a", "a", "a"],
            ["z", "a", "b", "c"],
            ["a", "a"],
            ["a"],
            ["b", "b", "b", "a", "b"],
        ],
        hints=[
            "Strip matching nodes off the front first, then walk with a one-behind pointer.",
            "After unlinking, do NOT advance -- the next node may also match.",
            "cmp returns 0 for equal, like strcmp. Do not treat non-zero as a match.",
        ],
    ),
    _list_exercise(
        name="sorted_list_insert",
        exams={"exam_04": 2},
        source=ADDED,
        prototype="void sorted_list_insert(t_list **begin_list, void *data, int (*cmp)(void *, void *));",
        allowed=["malloc"],
        subject="""
The list is already sorted in ascending order according to cmp. Write a function
that inserts a new element holding `data` at the position that keeps the list
sorted.

cmp returns a negative number, 0, or a positive number, like strcmp. When the new
data compares equal to an existing element, insert the new element before it.

The head may change, so the caller's pointer must be updated.
""",
        subject_th="""
ลิสต์ที่รับเข้ามาเรียงจากน้อยไปมากตามการเปรียบเทียบด้วย cmp อยู่แล้ว
ให้เขียนฟังก์ชันที่แทรกสมาชิกใหม่ซึ่งเก็บข้อมูล data
ลงในตำแหน่งที่ทำให้ลิสต์ยังเรียงลำดับอยู่

cmp คืนค่าเป็นลบ ศูนย์ หรือบวก แบบเดียวกับ strcmp
ถ้าข้อมูลใหม่เทียบเท่ากับสมาชิกที่มีอยู่ ให้แทรกไว้ก่อนสมาชิกนั้น

หัวลิสต์อาจเปลี่ยนได้ ดังนั้นต้องปรับพอยน์เตอร์ของผู้เรียกด้วย
""",
        reference="""
#include <stdlib.h>
#include "ft_list.h"

void	sorted_list_insert(t_list **begin_list, void *data,
		int (*cmp)(void *, void *))
{
	t_list	*node;
	t_list	*cursor;

	node = malloc(sizeof(t_list));
	if (!node)
		return ;
	node->data = data;
	node->next = 0;
	if (!*begin_list || cmp(data, (*begin_list)->data) <= 0)
	{
		node->next = *begin_list;
		*begin_list = node;
		return ;
	}
	cursor = *begin_list;
	while (cursor->next && cmp(data, cursor->next->data) > 0)
		cursor = cursor->next;
	node->next = cursor->next;
	cursor->next = node;
}
""",
        harness="""
void	sorted_list_insert(t_list **begin_list, void *data,
			int (*cmp)(void *, void *));

static int	cmp_str(void *a, void *b)
{
	return (strcmp((char *)a, (char *)b));
}

int	main(int argc, char **argv)
{
	t_list	*list;
	int		i;

	list = 0;
	i = 1;
	while (i < argc)
	{
		sorted_list_insert(&list, argv[i], &cmp_str);
		i++;
	}
	print_list(list);
	return (0);
}
""",
        stub_body="""
void	sorted_list_insert(t_list **begin_list, void *data,
		int (*cmp)(void *, void *))
{
	(void)begin_list;
	(void)data;
	(void)cmp;
}
""",
        tests=[
            ["c", "a", "b"],
            ["a"],
            [],
            ["b", "b", "a", "c"],
            ["z", "y", "x"],
            ["a", "b", "c", "d"],
        ],
        hints=[
            "Inserting at the head is its own case: empty list, or new data <= head.",
            "Otherwise stop at the node whose next should come after the new data.",
            "Link the new node to cursor->next BEFORE overwriting cursor->next.",
        ],
    ),
    # The 2026 pool's equivalent is `sort_list` at exam_04/2, with a different
    # prototype; it is still to be written. When it lands the two sit side by
    # side rather than replacing each other -- same level, different signature.
    _list_exercise(
        name="ft_list_sort",
        exams={"exam_04": 2},
        source=ADDED,
        prototype="void ft_list_sort(t_list **begin_list, int (*cmp)(void *, void *));",
        allowed=[],
        subject="""
Write a function that sorts the elements of the list into ascending order
according to cmp, which returns a negative number, 0, or a positive number like
strcmp.

The sort must be done by rearranging the existing nodes -- do not allocate, do
not free, and do not swap the data between nodes. The caller's head pointer must
end up pointing at the smallest element.
""",
        subject_th="""
เขียนฟังก์ชันที่เรียงลำดับสมาชิกของลิสต์จากน้อยไปมากตามการเปรียบเทียบด้วย cmp
ซึ่งคืนค่าเป็นลบ ศูนย์ หรือบวก แบบเดียวกับ strcmp

การเรียงลำดับต้องทำโดยจัดเรียงสมาชิกที่มีอยู่เท่านั้น ห้ามจองหน่วยความจำใหม่
ห้ามคืนหน่วยความจำ และห้ามสลับข้อมูลระหว่างสมาชิก
เมื่อเสร็จแล้วพอยน์เตอร์หัวลิสต์ของผู้เรียกต้องชี้ไปที่สมาชิกที่มีค่าน้อยที่สุด
""",
        reference="""
#include "ft_list.h"

void	ft_list_sort(t_list **begin_list, int (*cmp)(void *, void *))
{
	t_list	**slot;
	t_list	*node;
	int		swapped;

	swapped = 1;
	while (swapped)
	{
		swapped = 0;
		slot = begin_list;
		while (*slot && (*slot)->next)
		{
			if (cmp((*slot)->data, (*slot)->next->data) > 0)
			{
				node = *slot;
				*slot = node->next;
				node->next = (*slot)->next;
				(*slot)->next = node;
				swapped = 1;
			}
			slot = &(*slot)->next;
		}
	}
}
""",
        harness="""
void	ft_list_sort(t_list **begin_list, int (*cmp)(void *, void *));

static int	cmp_str(void *a, void *b)
{
	return (strcmp((char *)a, (char *)b));
}

int	main(int argc, char **argv)
{
	t_list	*list;

	list = build_list(argc - 1, argv + 1);
	ft_list_sort(&list, &cmp_str);
	print_list(list);
	return (0);
}
""",
        stub_body="""
void	ft_list_sort(t_list **begin_list, int (*cmp)(void *, void *))
{
	(void)begin_list;
	(void)cmp;
}
""",
        tests=[
            ["c", "a", "b"],
            ["a"],
            [],
            ["d", "c", "b", "a"],
            ["b", "a", "b"],
            ["1", "3", "2", "5", "4"],
        ],
        hints=[
            "A t_list ** cursor lets you rewrite the head and any next pointer with the same code.",
            "Bubble sort on nodes: swap a pair, mark that something changed, repeat until a clean pass.",
            "Relinking three pointers per swap is fiddly -- draw it before you code it.",
        ],
    ),
    # ------------------------------------------------------------------ level 8
    ex(
        name="eval_expr",
        exams={"exam_04": 3},
        source=ADDED,
        kind=PROGRAM,
        allowed=["printf", "write"],
        subject="""
Write a program that evaluates the arithmetic expression given as its single
argument and displays the result, followed by a newline.

The expression may contain non-negative integers, the binary operators +, -, *, /
and %, parentheses, and spaces. Standard precedence applies: * / % bind tighter
than + -, parentheses override everything, and operators of equal precedence
associate to the left. A '-' directly in front of a value negates it.

All arithmetic is integer arithmetic. You may assume the expression is valid and
that no division or modulo by zero occurs.

If the number of arguments is not 1, the program writes only a newline.

Examples:

  $> ./eval_expr "1 + 2 * 3" | cat -e
  7$
  $> ./eval_expr "(1 + 2) * 3" | cat -e
  9$
  $> ./eval_expr "10 - 2 - 3" | cat -e
  5$
""",
        subject_th="""
เขียนโปรแกรมที่คำนวณค่าของนิพจน์คณิตศาสตร์ที่รับมาเป็นอาร์กิวเมนต์เดียว
แล้วแสดงผลลัพธ์ ตามด้วยการขึ้นบรรทัดใหม่

นิพจน์อาจประกอบด้วยจำนวนเต็มที่ไม่เป็นลบ ตัวดำเนินการสองตัวแปร +, -, *, / และ %
วงเล็บ และช่องว่าง โดยใช้ลำดับความสำคัญตามปกติ คือ * / % มาก่อน + -
วงเล็บมีความสำคัญสูงสุด และตัวดำเนินการที่มีความสำคัญเท่ากันให้คำนวณจากซ้ายไปขวา
เครื่องหมาย '-' ที่อยู่หน้าค่าโดยตรงหมายถึงการเปลี่ยนเครื่องหมายของค่านั้น

การคำนวณทั้งหมดเป็นการคำนวณแบบจำนวนเต็ม
สามารถสมมติได้ว่านิพจน์ถูกต้อง และไม่มีการหารหรือมอดุโลด้วยศูนย์

ถ้าจำนวนอาร์กิวเมนต์ไม่เท่ากับ 1 ให้แสดงเฉพาะการขึ้นบรรทัดใหม่

ตัวอย่าง:

  $> ./eval_expr "1 + 2 * 3" | cat -e
  7$
  $> ./eval_expr "(1 + 2) * 3" | cat -e
  9$
  $> ./eval_expr "10 - 2 - 3" | cat -e
  5$
""",
        reference="""
#include <stdio.h>

static const char	*g_cursor;

static int	parse_sum(void);

static void	skip_spaces(void)
{
	while (*g_cursor == ' ' || *g_cursor == '\\t')
		g_cursor++;
}

static int	parse_value(void)
{
	int	value;

	skip_spaces();
	if (*g_cursor == '(')
	{
		g_cursor++;
		value = parse_sum();
		skip_spaces();
		if (*g_cursor == ')')
			g_cursor++;
		return (value);
	}
	if (*g_cursor == '-')
	{
		g_cursor++;
		return (-parse_value());
	}
	value = 0;
	while (*g_cursor >= '0' && *g_cursor <= '9')
	{
		value = value * 10 + (*g_cursor - '0');
		g_cursor++;
	}
	return (value);
}

static int	parse_product(void)
{
	int	value;

	value = parse_value();
	while (1)
	{
		skip_spaces();
		if (*g_cursor == '*')
		{
			g_cursor++;
			value = value * parse_value();
		}
		else if (*g_cursor == '/')
		{
			g_cursor++;
			value = value / parse_value();
		}
		else if (*g_cursor == '%')
		{
			g_cursor++;
			value = value % parse_value();
		}
		else
			return (value);
	}
}

static int	parse_sum(void)
{
	int	value;

	value = parse_product();
	while (1)
	{
		skip_spaces();
		if (*g_cursor == '+')
		{
			g_cursor++;
			value = value + parse_product();
		}
		else if (*g_cursor == '-')
		{
			g_cursor++;
			value = value - parse_product();
		}
		else
			return (value);
	}
}

int	main(int argc, char **argv)
{
	if (argc != 2)
	{
		printf("\\n");
		return (0);
	}
	g_cursor = argv[1];
	printf("%d\\n", parse_sum());
	return (0);
}
""",
        tests=[
            ["1 + 2 * 3"],
            ["(1 + 2) * 3"],
            ["10 - 2 - 3"],
            ["42"],
            ["2 * 3 * 4"],
            ["100 / 5 / 2"],
            ["17 % 5"],
            ["-3 + 10"],
            ["((2))"],
            ["1+2*(3-1)"],
            ["8 / 3"],
            [],
        ],
        hints=[
            "Three mutually recursive levels: sums call products, products call values, values can call sums inside parentheses.",
            "Left associativity comes from looping at each level, not from recursing on the right.",
            "Keep the read position in one place (a global or a char ** you pass around).",
        ],
    ),
    ex(
        name="permutations",
        exams={"exam_04": 3},
        source=ADDED,
        kind=PROGRAM,
        allowed=["write"],
        subject="""
Write a program that takes a string of distinct alphabetical characters and
displays every permutation of it in lexicographic order, one per line.

If the number of arguments is not 1, the program writes only a newline.

Example:

  $> ./permutations abc | cat -e
  abc$
  acb$
  bac$
  bca$
  cab$
  cba$
""",
        subject_th="""
เขียนโปรแกรมที่รับข้อความที่ประกอบด้วยตัวอักษรที่ไม่ซ้ำกัน
แล้วแสดงการเรียงสับเปลี่ยนทุกรูปแบบของข้อความนั้นตามลำดับพจนานุกรม
บรรทัดละหนึ่งรูปแบบ

ถ้าจำนวนอาร์กิวเมนต์ไม่เท่ากับ 1 ให้แสดงเฉพาะการขึ้นบรรทัดใหม่

ตัวอย่าง:

  $> ./permutations abc | cat -e
  abc$
  acb$
  bac$
  bca$
  cab$
  cba$
""",
        reference="""
#include <unistd.h>

static void	swap(char *a, char *b)
{
	char	tmp;

	tmp = *a;
	*a = *b;
	*b = tmp;
}

static int	length_of(char *s)
{
	int	n;

	n = 0;
	while (s[n])
		n++;
	return (n);
}

static void	sort_chars(char *s, int n)
{
	int	i;

	i = 0;
	while (i + 1 < n)
	{
		if (s[i] > s[i + 1])
		{
			swap(&s[i], &s[i + 1]);
			i = 0;
		}
		else
			i++;
	}
}

static int	next_permutation(char *s, int n)
{
	int	i;
	int	j;

	i = n - 2;
	while (i >= 0 && s[i] >= s[i + 1])
		i--;
	if (i < 0)
		return (0);
	j = n - 1;
	while (s[j] <= s[i])
		j--;
	swap(&s[i], &s[j]);
	i++;
	j = n - 1;
	while (i < j)
	{
		swap(&s[i], &s[j]);
		i++;
		j--;
	}
	return (1);
}

int	main(int argc, char **argv)
{
	int	n;

	if (argc != 2)
	{
		write(1, "\\n", 1);
		return (0);
	}
	n = length_of(argv[1]);
	sort_chars(argv[1], n);
	write(1, argv[1], n);
	write(1, "\\n", 1);
	while (next_permutation(argv[1], n))
	{
		write(1, argv[1], n);
		write(1, "\\n", 1);
	}
	return (0);
}
""",
        tests=[["abc"], ["ab"], ["a"], [""], ["abcd"], ["cba"], []],
        hints=[
            "Sort the characters first -- the sorted string is the first permutation.",
            "Then repeatedly compute the NEXT permutation: find the rightmost ascent, swap, reverse the tail.",
            "That standard algorithm gives lexicographic order for free, with no recursion.",
        ],
    ),
    ex(
        name="flood_fill",
        exams={"exam_04": 2},
        kind=FUNCTION,
        allowed=[],
        prototype="void flood_fill(char **tab, t_point size, t_point begin);",
        files=["flood_fill.c", "flood_fill.h"],
        subject="""
Write a function that fills, with the character 'F', the whole zone of the 2D map
`tab` that contains the position `begin`.

A zone is the set of positions reachable from begin by moving only up, down, left
or right (never diagonally) across positions holding the same character as
tab[begin.y][begin.x].

size.x is the width of the map and size.y its height. The map is modified in
place.

You must also submit flood_fill.h, defining:

  typedef struct s_point
  {
      int x;
      int y;
  } t_point;
""",
        subject_th="""
เขียนฟังก์ชันที่เติมตัวอักษร 'F' ลงในพื้นที่ทั้งผืนของแผนที่สองมิติ tab
ที่มีตำแหน่ง begin อยู่

พื้นที่ผืนหนึ่ง หมายถึงกลุ่มตำแหน่งที่เดินไปถึงได้จาก begin
โดยเดินได้เฉพาะขึ้น ลง ซ้าย ขวา (ห้ามเดินทแยง)
และตำแหน่งที่เดินผ่านต้องมีตัวอักษรเดียวกับ tab[begin.y][begin.x]

size.x คือความกว้างของแผนที่ และ size.y คือความสูง
โดยแก้ไขแผนที่ในตัวเดิม

คุณต้องส่งไฟล์ flood_fill.h ที่นิยามชนิดข้อมูลนี้ด้วย:

  typedef struct s_point
  {
      int x;
      int y;
  } t_point;
""",
        reference={
            "flood_fill.c": """
#include "flood_fill.h"

static void	fill(char **tab, t_point size, int x, int y, char target)
{
	if (x < 0 || y < 0 || x >= size.x || y >= size.y)
		return ;
	if (tab[y][x] != target)
		return ;
	tab[y][x] = 'F';
	fill(tab, size, x + 1, y, target);
	fill(tab, size, x - 1, y, target);
	fill(tab, size, x, y + 1, target);
	fill(tab, size, x, y - 1, target);
}

void	flood_fill(char **tab, t_point size, t_point begin)
{
	char	target;

	if (begin.x < 0 || begin.y < 0 || begin.x >= size.x || begin.y >= size.y)
		return ;
	target = tab[begin.y][begin.x];
	if (target == 'F')
		return ;
	fill(tab, size, begin.x, begin.y, target);
}
""",
            "flood_fill.h": """
#ifndef FLOOD_FILL_H
# define FLOOD_FILL_H

typedef struct s_point
{
	int	x;
	int	y;
}	t_point;

#endif
""",
        },
        harness="""
#include <stdio.h>
#include <stdlib.h>
#include "flood_fill.h"

void	flood_fill(char **tab, t_point size, t_point begin);

int	main(int argc, char **argv)
{
	char	rows[5][8] = {
		"1111111",
		"1001001",
		"1001001",
		"1000001",
		"1111111",
	};
	char	*tab[5];
	t_point	size;
	t_point	begin;
	int		i;

	if (argc != 3)
		return (0);
	i = 0;
	while (i < 5)
	{
		tab[i] = rows[i];
		i++;
	}
	size.x = 7;
	size.y = 5;
	begin.x = atoi(argv[1]);
	begin.y = atoi(argv[2]);
	flood_fill(tab, size, begin);
	i = 0;
	while (i < 5)
	{
		printf("%s\\n", tab[i]);
		i++;
	}
	return (0);
}
""",
        stub='#include "flood_fill.h"\n\n'
        "void\tflood_fill(char **tab, t_point size, t_point begin)\n"
        "{\n\t(void)tab;\n\t(void)size;\n\t(void)begin;\n}\n",
        tests=[
            ["1", "1"],
            ["0", "0"],
            ["3", "1"],
            ["1", "3"],
            ["99", "99"],
            ["-1", "0"],
        ],
        hints=[
            "Recursion is the short route: paint the current cell, then recurse in the four directions.",
            "Check the bounds BEFORE reading tab[y][x], or you will read outside the map.",
            "Painting the cell before recursing is what stops the recursion from looping forever.",
            "Note that size.x is the width, so it bounds x, which indexes the inner string.",
        ],
    ),
    # ------------------------------------------------------------------ level 9
    ex(
        name="n_queens",
        exams={"extra": 1},
        source=EXTRA,
        kind=PROGRAM,
        allowed=["atoi", "printf", "write"],
        subject="""
Write a program that takes an integer n and displays every solution to the
n-queens problem: n queens placed on an n x n board so that no two of them share
a row, a column, or a diagonal.

Print one solution per line. A solution is written as the row index of the queen
in each column, from the first column to the last, separated by single spaces.
Rows and columns are numbered from 0.

Solutions must be printed in ascending lexicographic order of those index
sequences.

If the number of arguments is not 1, or if n is not strictly positive, the
program prints nothing. If there is no solution, the program prints nothing.

Example:

  $> ./n_queens 4 | cat -e
  1 3 0 2$
  2 0 3 1$
""",
        subject_th="""
เขียนโปรแกรมที่รับจำนวนเต็ม n แล้วแสดงคำตอบทุกรูปแบบของปัญหา n ควีน
คือการวางควีน n ตัวบนกระดานขนาด n x n โดยไม่มีควีนคู่ใดอยู่ในแถวเดียวกัน
คอลัมน์เดียวกัน หรือแนวทแยงเดียวกัน

แสดงคำตอบบรรทัดละหนึ่งรูปแบบ โดยเขียนเป็นหมายเลขแถวของควีนในแต่ละคอลัมน์
ไล่จากคอลัมน์แรกไปคอลัมน์สุดท้าย คั่นด้วยช่องว่างหนึ่งช่อง
โดยนับหมายเลขแถวและคอลัมน์เริ่มจาก 0

คำตอบต้องแสดงเรียงตามลำดับพจนานุกรมของลำดับหมายเลขเหล่านั้นจากน้อยไปมาก

ถ้าจำนวนอาร์กิวเมนต์ไม่เท่ากับ 1 หรือ n ไม่เป็นจำนวนเต็มบวก
ให้โปรแกรมไม่แสดงอะไรเลย และถ้าไม่มีคำตอบก็ไม่ต้องแสดงอะไรเช่นกัน

ตัวอย่าง:

  $> ./n_queens 4 | cat -e
  1 3 0 2$
  2 0 3 1$
""",
        reference="""
#include <stdio.h>
#include <stdlib.h>

static int	g_size;
static int	g_rows[32];

static int	is_safe(int column, int row)
{
	int	i;

	i = 0;
	while (i < column)
	{
		if (g_rows[i] == row)
			return (0);
		if (g_rows[i] - i == row - column)
			return (0);
		if (g_rows[i] + i == row + column)
			return (0);
		i++;
	}
	return (1);
}

static void	solve(int column)
{
	int	row;

	if (column == g_size)
	{
		row = 0;
		while (row < g_size)
		{
			printf("%d", g_rows[row]);
			if (row + 1 < g_size)
				printf(" ");
			row++;
		}
		printf("\\n");
		return ;
	}
	row = 0;
	while (row < g_size)
	{
		if (is_safe(column, row))
		{
			g_rows[column] = row;
			solve(column + 1);
		}
		row++;
	}
}

int	main(int argc, char **argv)
{
	if (argc != 2)
		return (0);
	g_size = atoi(argv[1]);
	if (g_size <= 0 || g_size > 32)
		return (0);
	solve(0);
	return (0);
}
""",
        tests=[["4"], ["1"], ["2"], ["3"], ["5"], ["6"], ["0"], ["-1"], []],
        hints=[
            "Place one queen per column, and recurse to the next column.",
            "Two queens share a diagonal when row - column matches, or when row + column matches.",
            "Trying rows in ascending order at every column produces lexicographic output naturally.",
            "n = 2 and n = 3 have no solutions, so printing nothing is the correct answer.",
        ],
    ),
    ex(
        name="ft_printf",
        exams={"extra": 0},
        source=EXTRA,
        kind=FUNCTION,
        allowed=["write", "malloc", "free", "va_start", "va_arg", "va_copy", "va_end"],
        prototype="int ft_printf(const char *format, ...);",
        # The variadic `...` has no name, so the stub cannot be synthesised.
        stub="int\tft_printf(const char *format, ...)\n{\n\t(void)format;\n\treturn (0);\n}\n",
        subject="""
Write a variadic function that mimics printf for a small set of conversions, and
returns the number of characters it printed.

The conversions to handle are:

  %s   a string of characters
  %d   a signed decimal integer
  %x   an unsigned integer in lowercase hexadecimal
  %%   a literal percent sign

Any other character following a '%' is printed as-is, preceded by the '%'.
Flags, field widths and precisions are not required. The function must handle
INT_MIN for %d.

Output goes to standard output.
""",
        subject_th="""
เขียนฟังก์ชันแบบรับอาร์กิวเมนต์ไม่จำกัดจำนวน ที่ทำงานเลียนแบบ printf
สำหรับรูปแบบการแปลงชุดเล็ก ๆ แล้วคืนค่าจำนวนตัวอักษรที่แสดงออกไป

รูปแบบการแปลงที่ต้องรองรับคือ:

  %s   ข้อความ
  %d   จำนวนเต็มฐานสิบแบบมีเครื่องหมาย
  %x   จำนวนเต็มไม่มีเครื่องหมายในระบบฐานสิบหกตัวพิมพ์เล็ก
  %%   เครื่องหมายเปอร์เซ็นต์

อักขระอื่นที่ตามหลัง '%' ให้แสดงตามเดิมโดยมี '%' นำหน้า
ไม่ต้องรองรับแฟล็ก ความกว้างของช่อง หรือความละเอียดทศนิยม
และฟังก์ชันต้องรองรับค่า INT_MIN สำหรับ %d

ให้แสดงผลออกทางเอาต์พุตมาตรฐาน
""",
        reference="""
#include <stdarg.h>
#include <unistd.h>

static int	put_char(char c)
{
	write(1, &c, 1);
	return (1);
}

static int	put_str(const char *s)
{
	int	len;

	if (!s)
		s = "(null)";
	len = 0;
	while (s[len])
		len++;
	write(1, s, len);
	return (len);
}

static int	put_base(unsigned long value, unsigned long base,
		const char *digits)
{
	int	count;

	count = 0;
	if (value >= base)
		count += put_base(value / base, base, digits);
	count += put_char(digits[value % base]);
	return (count);
}

static int	put_int(int value)
{
	unsigned long	magnitude;
	int				count;

	count = 0;
	if (value < 0)
	{
		count += put_char('-');
		magnitude = (unsigned long)(-(long)value);
	}
	else
		magnitude = (unsigned long)value;
	return (count + put_base(magnitude, 10, "0123456789"));
}

static int	convert(char spec, va_list *ap)
{
	if (spec == 's')
		return (put_str(va_arg(*ap, char *)));
	if (spec == 'd')
		return (put_int(va_arg(*ap, int)));
	if (spec == 'x')
		return (put_base(va_arg(*ap, unsigned int), 16, "0123456789abcdef"));
	if (spec == '%')
		return (put_char('%'));
	return (put_char('%') + put_char(spec));
}

int	ft_printf(const char *format, ...)
{
	va_list	ap;
	int		count;
	int		i;

	va_start(ap, format);
	count = 0;
	i = 0;
	while (format[i])
	{
		if (format[i] == '%' && format[i + 1])
		{
			i++;
			count += convert(format[i], &ap);
		}
		else
			count += put_char(format[i]);
		i++;
	}
	va_end(ap);
	return (count);
}
""",
        harness="""
#include <stdio.h>

int	ft_printf(const char *format, ...);

static void	report(int count)
{
	/* ft_printf writes unbuffered, so flush to keep the order honest. */
	printf(" -> %d\\n", count);
	fflush(stdout);
}

int	main(void)
{
	report(ft_printf("plain text"));
	report(ft_printf("str=[%s]", "hello"));
	report(ft_printf("empty=[%s]", ""));
	report(ft_printf("dec=%d %d %d", 42, 0, -42));
	report(ft_printf("min=%d", -2147483648));
	report(ft_printf("hex=%x %x %x", 255, 0, 4294967295u));
	report(ft_printf("100%% sure"));
	report(ft_printf("mixed %s=%d (%x)", "id", 7, 7));
	report(ft_printf("unknown %q here"));
	report(ft_printf(""));
	return (0);
}
""",
        tests=[[]],
        hints=[
            "va_start, then va_arg once per conversion, then va_end.",
            "To pass the va_list to a helper, take a va_list * -- copying it is not portable.",
            "Count every character you write, including the '-' and the padding-free digits.",
            "Negating INT_MIN overflows an int, so widen to long before you negate.",
        ],
    ),
]
