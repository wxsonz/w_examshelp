#include <stdio.h>
#include <stdlib.h>

static int	g_size;
static int	g_rows[32];

static int	is_safe(int column, int row)
{
	int	i;

	i = 0;
	while (i < column)
	{
		if (g_rows[i] == row)
			return (0);
		if (g_rows[i] - i == row - column)
			return (0);
		if (g_rows[i] + i == row + column)
			return (0);
		i++;
	}
	return (1);
}

static void	solve(int column)
{
	int	row;

	if (column == g_size)
	{
		row = 0;
		while (row < g_size)
		{
			printf("%d", g_rows[row]);
			if (row + 1 < g_size)
				printf(" ");
			row++;
		}
		printf("\n");
		return ;
	}
	row = 0;
	while (row < g_size)
	{
		if (is_safe(column, row))
		{
			g_rows[column] = row;
			solve(column + 1);
		}
		row++;
	}
}

int	main(int argc, char **argv)
{
	if (argc != 2)
		return (0);
	g_size = atoi(argv[1]);
	if (g_size <= 0 || g_size > 32)
		return (0);
	solve(0);
	return (0);
}
