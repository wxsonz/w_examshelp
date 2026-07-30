#include <unistd.h>

static void	emit(char *s, char *seen)
{
	int	i;

	i = 0;
	while (s[i])
	{
		if (!seen[(unsigned char)s[i]])
		{
			write(1, &s[i], 1);
			seen[(unsigned char)s[i]] = 1;
		}
		i++;
	}
}

int	main(int argc, char **argv)
{
	char	seen[256];
	int		i;

	if (argc == 3)
	{
		i = 0;
		while (i < 256)
			seen[i++] = 0;
		emit(argv[1], seen);
		emit(argv[2], seen);
	}
	write(1, "\n", 1);
	return (0);
}
