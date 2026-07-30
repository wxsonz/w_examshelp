#include <stdlib.h>

static int	is_sep(char c)
{
	return (c == ' ' || c == '\t' || c == '\n');
}

static int	count_words(char *str)
{
	int	count;
	int	i;

	count = 0;
	i = 0;
	while (str[i])
	{
		while (str[i] && is_sep(str[i]))
			i++;
		if (str[i])
			count++;
		while (str[i] && !is_sep(str[i]))
			i++;
	}
	return (count);
}

static char	*dup_word(char *start, int len)
{
	char	*word;
	int		i;

	word = malloc(sizeof(char) * (len + 1));
	if (!word)
		return (0);
	i = 0;
	while (i < len)
	{
		word[i] = start[i];
		i++;
	}
	word[i] = '\0';
	return (word);
}

char	**ft_split(char *str)
{
	char	**out;
	int		i;
	int		start;
	int		w;

	out = malloc(sizeof(char *) * (count_words(str) + 1));
	if (!out)
		return (0);
	i = 0;
	w = 0;
	while (str[i])
	{
		while (str[i] && is_sep(str[i]))
			i++;
		if (!str[i])
			break ;
		start = i;
		while (str[i] && !is_sep(str[i]))
			i++;
		out[w] = dup_word(str + start, i - start);
		if (!out[w])
			return (0);
		w++;
	}
	out[w] = 0;
	return (out);
}
