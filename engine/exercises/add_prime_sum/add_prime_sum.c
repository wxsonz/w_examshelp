#include <unistd.h>

static void	put_nbr(int n)
{
	char	c;

	if (n >= 10)
		put_nbr(n / 10);
	c = (n % 10) + '0';
	write(1, &c, 1);
}

static int	is_prime(int n)
{
	int	d;

	if (n < 2)
		return (0);
	d = 2;
	while (d * d <= n)
	{
		if (n % d == 0)
			return (0);
		d++;
	}
	return (1);
}

int	main(int argc, char **argv)
{
	int	limit;
	int	sum;
	int	i;

	limit = 0;
	if (argc == 2)
	{
		i = 0;
		while (argv[1][i] >= '0' && argv[1][i] <= '9')
			limit = limit * 10 + (argv[1][i++] - '0');
		if (argv[1][i] || i == 0)
			limit = 0;
	}
	sum = 0;
	i = 2;
	while (i <= limit)
	{
		if (is_prime(i))
			sum += i;
		i++;
	}
	put_nbr(sum);
	write(1, "\n", 1);
	return (0);
}
