#include <stdio.h>

int	ft_printf(const char *format, ...);

static void	report(int count)
{
	/* ft_printf writes unbuffered, so flush to keep the order honest. */
	printf(" -> %d\n", count);
	fflush(stdout);
}

int	main(void)
{
	report(ft_printf("plain text"));
	report(ft_printf("str=[%s]", "hello"));
	report(ft_printf("empty=[%s]", ""));
	report(ft_printf("dec=%d %d %d", 42, 0, -42));
	report(ft_printf("min=%d", -2147483648));
	report(ft_printf("hex=%x %x %x", 255, 0, 4294967295u));
	report(ft_printf("100%% sure"));
	report(ft_printf("mixed %s=%d (%x)", "id", 7, 7));
	report(ft_printf("unknown %q here"));
	report(ft_printf(""));
	return (0);
}
