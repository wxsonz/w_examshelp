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

void	ft_list_reverse(t_list **begin_list);

int	main(int argc, char **argv)
{
	t_list	*list;

	list = build_list(argc - 1, argv + 1);
	ft_list_reverse(&list);
	print_list(list);
	return (0);
}
