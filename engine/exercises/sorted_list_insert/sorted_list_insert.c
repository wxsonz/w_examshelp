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
