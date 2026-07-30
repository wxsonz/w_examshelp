#include <stddef.h>

static int	in_set(char c, const char *set)
{
	int	i;

	i = 0;
	while (set[i])
	{
		if (set[i] == c)
			return (1);
		i++;
	}
	return (0);
}

size_t	ft_strspn(const char *s, const char *accept)
{
	size_t	n;

	n = 0;
	while (s[n] && in_set(s[n], accept))
		n++;
	return (n);
}
