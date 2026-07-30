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
