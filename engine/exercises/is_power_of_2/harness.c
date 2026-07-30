#include <stdio.h>
#include <stdlib.h>

int	is_power_of_2(unsigned int n);

int	main(int argc, char **argv)
{
	int	i;

	i = 1;
	while (i < argc)
	{
		printf("%d\n", is_power_of_2((unsigned int)atoi(argv[i])));
		i++;
	}
	return (0);
}
