#include <unistd.h>

static void	put_nbr(int n)
{
	char	c;

	if (n >= 10)
		put_nbr(n / 10);
	c = (n % 10) + '0';
	write(1, &c, 1);
}

static int	str_to_int(char *s)
{
	int	out;

	out = 0;
	while (*s >= '0' && *s <= '9')
		out = out * 10 + (*s++ - '0');
	return (out);
}

int	main(int argc, char **argv)
{
	int	n;
	int	i;

	if (argc != 2)
	{
		write(1, "\n", 1);
		return (0);
	}
	n = str_to_int(argv[1]);
	i = 1;
	while (i <= 9)
	{
		put_nbr(i);
		write(1, " x ", 3);
		put_nbr(n);
		write(1, " = ", 3);
		put_nbr(i * n);
		write(1, "\n", 1);
		i++;
	}
	return (0);
}
