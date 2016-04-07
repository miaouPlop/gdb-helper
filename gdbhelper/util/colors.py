# coding=utf-8


COLORS = {"black": "30", "red": "31", "green": "32", "yellow": "33",
          "blue": "34", "purple": "35", "cyan": "36", "white": "37"}
CATTRS = {"regular": "0", "bold": "1", "underline": "4", "strike": "9",
          "light": "1", "dark": "2", "invert": "7"}

CPRE = '\033['
CSUF = '\033[0m'


def colorize(text, color=None, attrib=None):
    """
    Colorize text using ansicolor
    ref: https://github.com/hellman/libcolors/blob/master/libcolors.py
    """
    # ansicolor definitions
    ccode = ""
    if attrib:
        for attr in attrib.lower().split():
            attr = attr.strip(",+|")
            if attr in CATTRS:
                ccode += ";" + CATTRS[attr]
    if color in COLORS:
        ccode += ";" + COLORS[color]
    return CPRE + ccode + "m" + text + CSUF


def colorize2(text, color=None, attrib=None):
    ccode = ""
    if attrib:
        for attr in attrib.lower().split():
            attr = attr.strip(",+|")
            if attr in CATTRS:
                ccode += CATTRS[attr]
    if color in COLORS:
        ccode += COLORS[color]
    return '\x1b[1m' + CPRE + ccode + "m" + text + CSUF + CSUF
