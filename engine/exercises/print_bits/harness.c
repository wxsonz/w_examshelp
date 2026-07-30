#include <stdio.h>
#include <stdlib.h>

void	print_bits(unsigned char octet);

int	main(int argc, char **argv)
{
	int	i;

	i = 1;
	while (i < argc)
	{
		print_bits((unsigned char)atoi(argv[i]));
		printf("\n");
		i++;
	}
	return (0);
}
