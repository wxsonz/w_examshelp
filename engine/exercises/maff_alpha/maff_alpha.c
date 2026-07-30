#include <unistd.h>

int	main(void)
{
	char	c;
	int	i;

	i = 0;
	while (i < 26)
	{
		c = 'a' + i;
		if (i % 2)
			c = c - 32;
		write(1, &c, 1);
		i++;
	}
	write(1, "\n", 1);
	return (0);
}
