#include <stdlib.h>

void	is_negative(int n);

int	main(int argc, char **argv)
{
	int	i;

	i = 1;
	while (i < argc)
	{
		is_negative(atoi(argv[i]));
		i++;
	}
	return (0);
}
