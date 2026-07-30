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
		printf("[%s]\n", (char *)found->data);
	else
		printf("(null)\n");
	return (0);
}
