#include <stdio.h>
#include <stdlib.h>

int	main(int argc, char **argv)
{
	int	a;
	int	b;
	int	tmp;

	if (argc != 3)
	{
		printf("\n");
		return (0);
	}
	a = atoi(argv[1]);
	b = atoi(argv[2]);
	while (b != 0)
	{
		tmp = b;
		b = a % b;
		a = tmp;
	}
	printf("%d\n", a);
	return (0);
}
