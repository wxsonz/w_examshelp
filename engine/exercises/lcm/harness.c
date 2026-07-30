#include <stdio.h>
#include <stdlib.h>

unsigned int	lcm(unsigned int a, unsigned int b);

int	main(int argc, char **argv)
{
	unsigned int	a;
	unsigned int	b;

	if (argc != 3)
		return (0);
	a = (unsigned int)strtoul(argv[1], 0, 10);
	b = (unsigned int)strtoul(argv[2], 0, 10);
	printf("%u\n", lcm(a, b));
	return (0);
}
