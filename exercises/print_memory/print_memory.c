#include <unistd.h>

static void	put_hex_byte(unsigned char b)
{
	char	*digits = "0123456789abcdef";

	write(1, &digits[b >> 4], 1);
	write(1, &digits[b & 15], 1);
}

static void	dump_line(const unsigned char *p, size_t count)
{
	size_t	i;
	char	c;

	i = 0;
	while (i < 16)
	{
		if (i < count)
			put_hex_byte(p[i]);
		else
			write(1, "  ", 2);
		if (i % 2 == 1)
			write(1, " ", 1);
		i++;
	}
	i = 0;
	while (i < count)
	{
		c = '.';
		if (p[i] >= 32 && p[i] <= 126)
			c = (char)p[i];
		write(1, &c, 1);
		i++;
	}
	write(1, "\n", 1);
}

void	print_memory(const void *addr, size_t size)
{
	const unsigned char	*p;
	size_t				done;
	size_t				count;

	p = (const unsigned char *)addr;
	done = 0;
	while (done < size)
	{
		count = size - done;
		if (count > 16)
			count = 16;
		dump_line(p + done, count);
		done += count;
	}
}
