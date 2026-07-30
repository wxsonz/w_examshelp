#include <stdlib.h>
#include <string.h>

void	print_memory(const void *addr, size_t size);

int	main(int argc, char **argv)
{
	size_t	size;

	if (argc < 2)
		return (0);
	size = strlen(argv[1]);
	if (argc > 2)
		size = (size_t)atoi(argv[2]);
	print_memory(argv[1], size);
	return (0);
}
