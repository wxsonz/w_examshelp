#include <unistd.h>

int	main(int argc, char **argv)
{
	char	seen[256];
	int		i;
	int		j;

	if (argc == 3)
	{
		i = 0;
		while (i < 256)
			seen[i++] = 0;
		i = 0;
		while (argv[1][i])
		{
			j = 0;
			while (argv[2][j] && argv[2][j] != argv[1][i])
				j++;
			if (argv[2][j] && !seen[(unsigned char)argv[1][i]])
			{
				write(1, &argv[1][i], 1);
				seen[(unsigned char)argv[1][i]] = 1;
			}
			i++;
		}
	}
	write(1, "\n", 1);
	return (0);
}
