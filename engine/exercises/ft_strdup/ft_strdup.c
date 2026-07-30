#include <stdlib.h>

char	*ft_strdup(char *src)
{
	char	*out;
	int		len;
	int		i;

	len = 0;
	while (src[len])
		len++;
	out = malloc(sizeof(char) * (len + 1));
	if (!out)
		return (0);
	i = 0;
	while (i < len)
	{
		out[i] = src[i];
		i++;
	}
	out[i] = '\0';
	return (out);
}
