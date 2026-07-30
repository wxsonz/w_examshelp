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
	printf("\n");
}

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
