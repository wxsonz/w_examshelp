#include <stdio.h>

char	*ft_strrev(char *str);

int	main(int argc, char **argv)
{
	int	i;

	i = 1;
	while (i < argc)
	{
		printf("[%s]\n", ft_strrev(argv[i]));
		i++;
	}
	return (0);
}
