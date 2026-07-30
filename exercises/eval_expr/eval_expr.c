#include <stdio.h>

static const char	*g_cursor;

static int	parse_sum(void);

static void	skip_spaces(void)
{
	while (*g_cursor == ' ' || *g_cursor == '\t')
		g_cursor++;
}

static int	parse_value(void)
{
	int	value;

	skip_spaces();
	if (*g_cursor == '(')
	{
		g_cursor++;
		value = parse_sum();
		skip_spaces();
		if (*g_cursor == ')')
			g_cursor++;
		return (value);
	}
	if (*g_cursor == '-')
	{
		g_cursor++;
		return (-parse_value());
	}
	value = 0;
	while (*g_cursor >= '0' && *g_cursor <= '9')
	{
		value = value * 10 + (*g_cursor - '0');
		g_cursor++;
	}
	return (value);
}

static int	parse_product(void)
{
	int	value;

	value = parse_value();
	while (1)
	{
		skip_spaces();
		if (*g_cursor == '*')
		{
			g_cursor++;
			value = value * parse_value();
		}
		else if (*g_cursor == '/')
		{
			g_cursor++;
			value = value / parse_value();
		}
		else if (*g_cursor == '%')
		{
			g_cursor++;
			value = value % parse_value();
		}
		else
			return (value);
	}
}

static int	parse_sum(void)
{
	int	value;

	value = parse_product();
	while (1)
	{
		skip_spaces();
		if (*g_cursor == '+')
		{
			g_cursor++;
			value = value + parse_product();
		}
		else if (*g_cursor == '-')
		{
			g_cursor++;
			value = value - parse_product();
		}
		else
			return (value);
	}
}

int	main(int argc, char **argv)
{
	if (argc != 2)
	{
		printf("\n");
		return (0);
	}
	g_cursor = argv[1];
	printf("%d\n", parse_sum());
	return (0);
}
