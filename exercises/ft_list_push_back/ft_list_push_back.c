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
