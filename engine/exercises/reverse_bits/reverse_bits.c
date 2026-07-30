unsigned char	reverse_bits(unsigned char octet)
{
	unsigned char	out;
	int				i;

	out = 0;
	i = 0;
	while (i < 8)
	{
		out = (out << 1) | ((octet >> i) & 1);
		i++;
	}
	return (out);
}
