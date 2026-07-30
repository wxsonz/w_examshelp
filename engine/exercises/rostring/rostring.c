#include <unistd.h>

static int	is_space(char c)
{
	return (c == ' ' || c == '\t');
}

static int	put_word(char *s, int i, int need_space)
{
	if (need_space)
		write(1, " ", 1);
	while (s[i] && !is_space(s[i]))
	{
		write(1, &s[i], 1);
		i++;
	}
	return (i);
}

int	main(int argc, char **argv)
{
	int	i;
	int	first;
	int	written;

	if (argc == 2)
	{
		i = 0;
		while (is_space(argv[1][i]))
			i++;
		first = i;
		while (argv[1][i] && !is_space(argv[1][i]))
			i++;
		written = 0;
		while (argv[1][i])
		{
			while (is_space(argv[1][i]))
				i++;
			if (!argv[1][i])
				break ;
			i = put_word(argv[1], i, written);
			written = 1;
		}
		if (argv[1][first])
			put_word(argv[1], first, written);
	}
	write(1, "\n", 1);
	return (0);
}
