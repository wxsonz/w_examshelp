#include <stdio.h>
#include <stdlib.h>

char	*ft_itoa(int nbr);

int	main(int argc, char **argv)
{
	char	*s;
	int		i;

	i = 1;
	while (i < argc)
	{
		s = ft_itoa(atoi(argv[i]));
		if (!s)
			return (1);
		printf("[%s]\n", s);
		free(s);
		i++;
	}
	return (0);
}
