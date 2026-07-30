#include <stdlib.h>

int	*ft_range(int start, int end)
{
	int	*out;
	int	len;
	int	i;
	int	step;

	if (start <= end)
	{
		len = end - start + 1;
		step = 1;
	}
	else
	{
		len = start - end + 1;
		step = -1;
	}
	out = malloc(sizeof(int) * len);
	if (!out)
		return (0);
	i = 0;
	while (i < len)
	{
		out[i] = start + i * step;
		i++;
	}
	return (out);
}
