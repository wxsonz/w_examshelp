#include <stdarg.h>
#include <unistd.h>

static int	put_char(char c)
{
	write(1, &c, 1);
	return (1);
}

static int	put_str(const char *s)
{
	int	len;

	if (!s)
		s = "(null)";
	len = 0;
	while (s[len])
		len++;
	write(1, s, len);
	return (len);
}

static int	put_base(unsigned long value, unsigned long base,
		const char *digits)
{
	int	count;

	count = 0;
	if (value >= base)
		count += put_base(value / base, base, digits);
	count += put_char(digits[value % base]);
	return (count);
}

static int	put_int(int value)
{
	unsigned long	magnitude;
	int				count;

	count = 0;
	if (value < 0)
	{
		count += put_char('-');
		magnitude = (unsigned long)(-(long)value);
	}
	else
		magnitude = (unsigned long)value;
	return (count + put_base(magnitude, 10, "0123456789"));
}

static int	convert(char spec, va_list *ap)
{
	if (spec == 's')
		return (put_str(va_arg(*ap, char *)));
	if (spec == 'd')
		return (put_int(va_arg(*ap, int)));
	if (spec == 'x')
		return (put_base(va_arg(*ap, unsigned int), 16, "0123456789abcdef"));
	if (spec == '%')
		return (put_char('%'));
	return (put_char('%') + put_char(spec));
}

int	ft_printf(const char *format, ...)
{
	va_list	ap;
	int		count;
	int		i;

	va_start(ap, format);
	count = 0;
	i = 0;
	while (format[i])
	{
		if (format[i] == '%' && format[i + 1])
		{
			i++;
			count += convert(format[i], &ap);
		}
		else
			count += put_char(format[i]);
		i++;
	}
	va_end(ap);
	return (count);
}
