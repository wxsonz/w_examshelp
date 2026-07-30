#include <stdio.h>
#include <stdlib.h>

int	max(int *tab, unsigned int len);

int	main(int argc, char **argv)
{
	int				tab[256];
	unsigned int	i;

	i = 0;
	while (i + 1 < (unsigned int)argc && i < 256)
	{
		tab[i] = atoi(argv[i + 1]);
		i++;
	}
	printf("%d\n", max(tab, i));
	return (0);
}
