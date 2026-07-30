#include <stdio.h>
#include <stdlib.h>

char	*ft_strdup(char *src);

int	main(int argc, char **argv)
{
	char	*copy;
	int		i;

	i = 1;
	while (i < argc)
	{
		copy = ft_strdup(argv[i]);
		if (!copy)
			return (1);
		/* A different address proves it really allocated. */
		printf("[%s] copied=%d\n", copy, copy != argv[i]);
		free(copy);
		i++;
	}
	return (0);
}
