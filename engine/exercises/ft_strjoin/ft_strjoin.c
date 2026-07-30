#include <stdlib.h>

static int	len_of(char *s)
{
	int	i;

	i = 0;
	while (s[i])
		i++;
	return (i);
}

static int	copy_into(char *dst, int at, char *src)
{
	int	i;

	i = 0;
	while (src[i])
		dst[at++] = src[i++];
	return (at);
}

char	*ft_strjoin(int size, char **strs, char *sep)
{
	char	*out;
	int		total;
	int		at;
	int		i;

	total = 0;
	i = 0;
	while (i < size)
		total += len_of(strs[i++]);
	if (size > 1)
		total += len_of(sep) * (size - 1);
	out = malloc(sizeof(char) * (total + 1));
	if (!out)
		return (0);
	at = 0;
	i = 0;
	while (i < size)
	{
		at = copy_into(out, at, strs[i]);
		if (i + 1 < size)
			at = copy_into(out, at, sep);
		i++;
	}
	out[at] = '\0';
	return (out);
}
