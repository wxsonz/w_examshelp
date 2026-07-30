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
