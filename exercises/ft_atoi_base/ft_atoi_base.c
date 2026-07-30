static int	digit_value(char c)
{
	if (c >= '0' && c <= '9')
		return (c - '0');
	if (c >= 'a' && c <= 'f')
		return (c - 'a' + 10);
	if (c >= 'A' && c <= 'F')
		return (c - 'A' + 10);
	return (-1);
}

int	ft_atoi_base(const char *str, int str_base)
{
	int	i;
	int	sign;
	int	out;
	int	value;

	if (str_base < 2 || str_base > 16)
		return (0);
	i = 0;
	sign = 1;
	if (str[0] == '-')
	{
		sign = -1;
		i = 1;
	}
	out = 0;
	value = digit_value(str[i]);
	while (value >= 0 && value < str_base)
	{
		out = out * str_base + value;
		i++;
		value = digit_value(str[i]);
	}
	return (out * sign);
}
