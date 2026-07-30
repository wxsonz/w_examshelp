#include <stdio.h>
#include <stdlib.h>

char	*ft_strjoin(int size, char **strs, char *sep);

int	main(int argc, char **argv)
{
	char	*joined;

	if (argc < 2)
		return (0);
	joined = ft_strjoin(argc - 2, argv + 2, argv[1]);
	if (!joined)
		return (1);
	printf("[%s]\n", joined);
	free(joined);
	return (0);
}
