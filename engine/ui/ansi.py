"""Terminal primitives: display width, ANSI-safe wrapping, boxes.

Zero dependencies, so ./examshelp runs on a bare school machine.

Three things the previous renderer got wrong, all visible on screen:

  * width was len(), which counts Thai vowel and tone marks as one cell each
    even though they are combining marks that occupy none, so every Thai line
    was padded short and the right border walked left;
  * the word wrapper split lines without tracking SGR state, so a continuation
    line lost its colour and carried a stray reset;
  * the box was a hardcoded 76 columns, and the 80-dash rule in every official
    subject overflowed it and broke the border.
"""

import re
import shutil

from engine.textwidth import char_width, display_width, pad, strip_ansi  # noqa: F401

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

CYAN = "\033[1;36m"
MAGENTA = "\033[1;35m"
YELLOW = "\033[1;33m"
GREEN = "\033[1;32m"
RED = "\033[1;31m"
WHITE = "\033[1;37m"
BLUE = "\033[1;34m"

MIN_WIDTH = 44
MAX_WIDTH = 100

_SGR = re.compile(r"\x1b\[[0-9;]*m")
_RULE = re.compile(r"^\s*([-=_*~])\1{7,}\s*$")


def terminal_width(default=80):
    try:
        return shutil.get_terminal_size((default, 24)).columns
    except OSError:
        return default


def box_width(preferred=76):
    """Box width that fits the current terminal."""
    return max(MIN_WIDTH, min(preferred, MAX_WIDTH, terminal_width() - 2))


def visible(text):
    """Render text the way `cat -e` does, so newlines and tabs can be seen."""
    out = []
    for ch in text:
        if ch == "\n":
            out.append("$\n")
        elif ch == "\t":
            out.append("^I")
        elif ch == "\r":
            out.append("^M")
        elif ord(ch) < 32:
            out.append(f"^{chr(ord(ch) + 64)}")
        else:
            out.append(ch)
    return "".join(out)


# --------------------------------------------------------------------------
# Wrapping
# --------------------------------------------------------------------------


def _tokenize(text):
    position = 0
    for match in _SGR.finditer(text):
        for ch in text[position : match.start()]:
            yield ("char", ch)
        yield ("sgr", match.group(0))
        position = match.end()
    for ch in text[position:]:
        yield ("char", ch)


class _LineBuilder:
    """Accumulates tokens into lines, carrying SGR state across breaks."""

    def __init__(self, width, indent):
        self.width = width
        self.indent = indent
        self.lines = []
        self.state = ""
        self.line = []
        self.line_state = ""
        self.line_w = 0
        self.first = True

    def limit(self):
        return self.width if self.first else self.width - display_width(self.indent)

    def emit(self):
        if not self.line and self.first:
            return
        body = "".join(value for _, value in self.line)
        prefix = "" if self.first else self.indent
        # Only re-open the colour if the body does not already do it itself.
        opening = self.line_state
        if opening and body.startswith(opening):
            opening = ""
        if body.endswith(RESET):
            closing = ""
        else:
            closing = RESET if (opening or "\x1b[" in body) else ""
        self.lines.append(prefix + opening + body + closing)
        self.first = False
        self.line = []
        self.line_state = self.state
        self.line_w = 0

    def add_word(self, tokens, word_w, entry_state, leading_space):
        space_w = 1 if (leading_space and self.line_w) else 0
        if self.line_w and self.line_w + space_w + word_w > self.limit():
            self.emit()
            space_w = 0
        elif space_w:
            self.line.append(("char", " "))
            self.line_w += 1
        if not self.line:
            self.line_state = entry_state
        self.line.extend(tokens)
        self.line_w += word_w

    def finish(self):
        if self.line or not self.lines:
            self.emit()
        return self.lines


def wrap(text, width, indent="  "):
    """Wrap to a display width without breaking escape sequences or losing colour.

    Continuation lines are prefixed with `indent` and re-open whatever SGR state
    was active at the break, so a coloured paragraph stays coloured.
    """
    text = str(text)
    if width <= 1:
        return [text]
    if display_width(text) <= width and "\n" not in text:
        return [text]

    builder = _LineBuilder(width, indent)
    state = ""
    word, word_w, word_state = [], 0, ""
    pending_space = False

    def flush_word():
        nonlocal word, word_w, word_state, pending_space
        if word:
            builder.add_word(word, word_w, word_state, pending_space)
            word, word_w = [], 0
            pending_space = False

    for kind, value in _tokenize(text):
        if kind == "sgr":
            if value in (RESET, "\x1b[m"):
                state = ""
            else:
                state += value
            if not word:
                word_state = state
            word.append((kind, value))
            continue

        if value == " ":
            flush_word()
            pending_space = True
            word_state = state
            continue

        cell = char_width(value)
        # A single word longer than the line has to be broken somewhere.
        if word_w + cell > builder.limit():
            flush_word()
            word_state = state
        word.append((kind, value))
        word_w += cell

    flush_word()
    return builder.finish()


# --------------------------------------------------------------------------
# Boxes
# --------------------------------------------------------------------------


def draw_box(title, lines, color=CYAN, footer=None, preferred=76, out=print,
             indent="  "):
    """Draw a titled box that fits the terminal and wraps its contents.

    A line that is nothing but a run of dashes (the rule in every official
    subject) is refitted to the box instead of overflowing it.
    """
    width = box_width(preferred)
    inner = width - 4

    title_w = display_width(title)
    if title_w > inner:
        title, title_w = title[:inner], inner
    left = max(1, (inner - title_w) // 2)
    right = max(1, inner - title_w - left)
    out(f"{color}╭{'─' * left} {title} {'─' * right}╮{RESET}")

    for line in lines:
        if _RULE.match(strip_ansi(line)):
            fill = strip_ansi(line).strip()[0]
            out(f"{color}│{RESET} {DIM}{fill * inner}{RESET} {color}│{RESET}")
            continue
        for piece in wrap(line, inner, indent=indent):
            out(f"{color}│{RESET} {pad(piece, inner)} {color}│{RESET}")

    if footer:
        footer_w = display_width(footer)
        dashes = max(1, width - 5 - footer_w)
        out(f"{color}╰{'─' * dashes} {footer} ─╯{RESET}")
    else:
        out(f"{color}╰{'─' * (width - 2)}╯{RESET}")


def rule(label=None, color=CYAN, out=print):
    """A full-width horizontal rule, optionally with a centred label."""
    width = box_width()
    if not label:
        out(f"{color}{'─' * width}{RESET}")
        return
    label_w = display_width(label)
    left = max(1, (width - label_w - 2) // 2)
    right = max(1, width - label_w - 2 - left)
    out(f"{color}{'─' * left} {label} {'─' * right}{RESET}")
