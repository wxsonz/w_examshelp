#include <unistd.h>

static void	swap(char *a, char *b)
{
	char	tmp;

	tmp = *a;
	*a = *b;
	*b = tmp;
}

static int	length_of(char *s)
{
	int	n;

	n = 0;
	while (s[n])
		n++;
	return (n);
}

static void	sort_chars(char *s, int n)
{
	int	i;

	i = 0;
	while (i + 1 < n)
	{
		if (s[i] > s[i + 1])
		{
			swap(&s[i], &s[i + 1]);
			i = 0;
		}
		else
			i++;
	}
}

static int	next_permutation(char *s, int n)
{
	int	i;
	int	j;

	i = n - 2;
	while (i >= 0 && s[i] >= s[i + 1])
		i--;
	if (i < 0)
		return (0);
	j = n - 1;
	while (s[j] <= s[i])
		j--;
	swap(&s[i], &s[j]);
	i++;
	j = n - 1;
	while (i < j)
	{
		swap(&s[i], &s[j]);
		i++;
		j--;
	}
	return (1);
}

int	main(int argc, char **argv)
{
	int	n;

	if (argc != 2)
	{
		write(1, "\n", 1);
		return (0);
	}
	n = length_of(argv[1]);
	sort_chars(argv[1], n);
	write(1, argv[1], n);
	write(1, "\n", 1);
	while (next_permutation(argv[1], n))
	{
		write(1, argv[1], n);
		write(1, "\n", 1);
	}
	return (0);
}
