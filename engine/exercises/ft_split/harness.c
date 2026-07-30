#include <stdio.h>
#include <stdlib.h>

char	**ft_split(char *str);

int	main(int argc, char **argv)
{
	char	**words;
	int		i;

	if (argc != 2)
		return (0);
	words = ft_split(argv[1]);
	if (!words)
		return (1);
	i = 0;
	while (words[i])
	{
		printf("[%s]\n", words[i]);
		free(words[i]);
		i++;
	}
	printf("count=%d\n", i);
	free(words);
	return (0);
}
