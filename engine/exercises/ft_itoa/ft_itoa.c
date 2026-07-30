#include <stdlib.h>

static int	digit_count(long n)
{
	int	count;

	count = 1;
	while (n >= 10 || n <= -10)
	{
		n /= 10;
		count++;
	}
	return (count);
}

char	*ft_itoa(int nbr)
{
	char	*out;
	long	n;
	int		len;
	int		neg;

	n = nbr;
	neg = (n < 0);
	len = digit_count(n) + neg;
	out = malloc(sizeof(char) * (len + 1));
	if (!out)
		return (0);
	out[len] = '\0';
	if (neg)
	{
		out[0] = '-';
		n = -n;
	}
	while (len-- > neg)
	{
		out[len] = (n % 10) + '0';
		n /= 10;
	}
	return (out);
}
