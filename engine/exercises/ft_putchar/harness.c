#include <unistd.h>

void	ft_putchar(char c);

int	main(int argc, char **argv)
{
	int	i;

	i = 1;
	while (i < argc)
	{
		if (argv[i][0])
			ft_putchar(argv[i][0]);
		i++;
	}
	write(1, "\n", 1);
	return (0);
}
