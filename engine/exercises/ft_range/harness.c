#include <stdio.h>
#include <stdlib.h>

int	*ft_range(int start, int end);

int	main(int argc, char **argv)
{
	int	*tab;
	int	start;
	int	end;
	int	len;
	int	i;

	if (argc != 3)
		return (0);
	start = atoi(argv[1]);
	end = atoi(argv[2]);
	if (start <= end)
		len = end - start + 1;
	else
		len = start - end + 1;
	tab = ft_range(start, end);
	if (!tab)
		return (1);
	i = 0;
	while (i < len)
	{
		printf("%d", tab[i]);
		if (i + 1 < len)
			printf(" ");
		i++;
	}
	printf("\n");
	free(tab);
	return (0);
}
