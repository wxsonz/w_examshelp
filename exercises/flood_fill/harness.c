#include <stdio.h>
#include <stdlib.h>
#include "flood_fill.h"

void	flood_fill(char **tab, t_point size, t_point begin);

int	main(int argc, char **argv)
{
	char	rows[5][8] = {
		"1111111",
		"1001001",
		"1001001",
		"1000001",
		"1111111",
	};
	char	*tab[5];
	t_point	size;
	t_point	begin;
	int		i;

	if (argc != 3)
		return (0);
	i = 0;
	while (i < 5)
	{
		tab[i] = rows[i];
		i++;
	}
	size.x = 7;
	size.y = 5;
	begin.x = atoi(argv[1]);
	begin.y = atoi(argv[2]);
	flood_fill(tab, size, begin);
	i = 0;
	while (i < 5)
	{
		printf("%s\n", tab[i]);
		i++;
	}
	return (0);
}
