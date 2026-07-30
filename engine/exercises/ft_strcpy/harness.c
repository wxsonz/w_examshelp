#include <stdio.h>

char	*ft_strcpy(char *s1, char *s2);

int	main(int argc, char **argv)
{
	char	buffer[1024];
	int		i;

	i = 1;
	while (i < argc)
	{
		buffer[0] = 'X';
		printf("[%s]\n", ft_strcpy(buffer, argv[i]));
		i++;
	}
	return (0);
}
