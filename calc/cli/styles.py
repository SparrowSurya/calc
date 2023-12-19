"""
This module contains various styles and colors for text in terminal.

Some styles might not be visible.
"""


def term_esc_seq(*seq: str | int) -> str:
    """convert a sequence to terminal escape seq"""
    return f"\033[{';'.join(map(str, seq))}m"

def term_fg(r: int, g: int, b: int) -> str:
    """terminal escape sequence for foregroud color"""
    return term_esc_seq(38, 2, r, g, b)

def term_bg(r: int, g: int, b: int) -> str:
    """terminal escape sequence for backgroud color"""
    return term_esc_seq(48, 2, r, g, b)

def wrap(text: str, start: str, end: str) -> str:
    """wraps a style one text"""
    return f"{start}{text}{end}"


# colors light/dark fg/bg

LT_GRAY_FG = term_esc_seq(30)
LT_RED_FG = term_esc_seq(31)
LT_GREEN_FG = term_esc_seq(32)
LT_YELLOW_FG = term_esc_seq(33)
LT_CYAN_FG = term_esc_seq(34)
LT_PURPLE_FG = term_esc_seq(35)
LT_TEAL_FG = term_esc_seq(36)
LT_WHITE_FG = term_esc_seq(37)

LT_GRAY_BG = term_esc_seq(40)
LT_RED_BG = term_esc_seq(41)
LT_GREEN_BG = term_esc_seq(42)
LT_YELLOW_BG = term_esc_seq(43)
LT_CYAN_BG = term_esc_seq(44)
LT_PURPLE_BG = term_esc_seq(45)
LT_TEAL_BG = term_esc_seq(46)
LT_WHITE_BG = term_esc_seq(47)

DK_GRAY_FG = term_esc_seq(90)
DK_RED_FG = term_esc_seq(91)
DK_GREEN_FG = term_esc_seq(92)
DK_YELLOW_FG = term_esc_seq(93)
DK_CYAN_FG = term_esc_seq(94)
DK_PURPLE_FG = term_esc_seq(95)
DK_TEAL_FG = term_esc_seq(96)
DK_WHITE_FG = term_esc_seq(97)

DK_GRAY_BG = term_esc_seq(100)
DK_RED_BG = term_esc_seq(101)
DK_GREEN_BG = term_esc_seq(102)
DK_YELLOW_BG = term_esc_seq(103)
DK_CYAN_BG = term_esc_seq(104)
DK_PURPLE_BG = term_esc_seq(105)
DK_TEAL_BG = term_esc_seq(106)
DK_WHITE_BG = term_esc_seq(107)

# styles

RESET = term_esc_seq(0)
BOLD = term_esc_seq(1)
CURSIVE = term_esc_seq(3)
UNDERLINE = term_esc_seq(4)
BLINK_SLOW = term_esc_seq(5)
BLINK_FAST = term_esc_seq(6)
INVERT = term_esc_seq(7)
HIDE = term_esc_seq(8)
STRIKE = term_esc_seq(9)
DOUBLE_UNDERLINE = term_esc_seq(21)
OVERLINE = term_esc_seq(53)
