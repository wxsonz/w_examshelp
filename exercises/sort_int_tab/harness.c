#include <stdio.h>
#include <stdlib.h>

void	sort_int_tab(int *tab, unsigned int size);

int	main(int argc, char **argv)
{
	int				tab[256];
	unsigned int	i;
	unsigned int	size;

	size = 0;
	while (size + 1 < (unsigned int)argc && size < 256)
	{
		tab[size] = atoi(argv[size + 1]);
		size++;
	}
	sort_int_tab(tab, size);
	i = 0;
	while (i < size)
	{
		printf("%d", tab[i]);
		if (i + 1 < size)
			printf(" ");
		i++;
	}
	printf("\n");
	return (0);
}
