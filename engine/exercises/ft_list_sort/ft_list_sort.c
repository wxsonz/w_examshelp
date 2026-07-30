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
