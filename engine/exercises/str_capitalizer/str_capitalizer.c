#include <unistd.h>

static int	is_space(char c)
{
	return (c == ' ' || c == '\t');
}

int	main(int argc, char **argv)
{
	int		i;
	int		j;
	int		start;
	char	c;

	if (argc < 2)
	{
		write(1, "\n", 1);
		return (0);
	}
	i = 1;
	while (i < argc)
	{
		j = 0;
		start = 1;
		while (argv[i][j])
		{
			c = argv[i][j];
			if (is_space(c))
				start = 1;
			else
			{
				if (start && c >= 'a' && c <= 'z')
					c = c - 32;
				else if (!start && c >= 'A' && c <= 'Z')
					c = c + 32;
				start = 0;
			}
			write(1, &c, 1);
			j++;
		}
		write(1, "\n", 1);
		i++;
	}
	return (0);
}
