"""How wide text is on a terminal.

Kept separate from engine.ui so that the exercise pack can align its subject
headers without depending on the rendering layer. `len()` is not the answer:
Thai vowel and tone marks are combining characters that occupy no cell, so a
Thai label padded by character count comes out visibly short.
"""

import re
import unicodedata

_SGR = re.compile(r"\x1b\[[0-9;]*m")
_ZERO_WIDTH = ("​", "‌", "‍")


def strip_ansi(text):
    return _SGR.sub("", str(text))


def char_width(ch):
    """Cells one character occupies: 0 for combining marks, 2 for wide, else 1."""
    if unicodedata.category(ch) in ("Mn", "Me", "Cf"):
        return 0
    if ch in _ZERO_WIDTH:
        return 0
    if unicodedata.east_asian_width(ch) in ("W", "F"):
        return 2
    return 1


def display_width(text):
    """How many terminal cells `text` occupies, ignoring escape sequences."""
    return sum(char_width(ch) for ch in strip_ansi(text))


def pad(text, width):
    """Right-pad to `width` display cells. Never truncates."""
    return text + " " * max(0, width - display_width(text))
