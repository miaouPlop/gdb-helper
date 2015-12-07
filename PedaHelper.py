# coding=utf-8


from GdbHelper import Gdb


def colorize(text, color=None, attrib=None):
    """
    Colorize text using ansicolor
    ref: https://github.com/hellman/libcolors/blob/master/libcolors.py
    """
    # ansicolor definitions
    COLORS = {"black": "30", "red": "31", "green": "32", "yellow": "33",
                "blue": "34", "purple": "35", "cyan": "36", "white": "37"}
    CATTRS = {"regular": "0", "bold": "1", "underline": "4", "strike": "9",
                "light": "1", "dark": "2", "invert": "7"}

    CPRE = '\033['
    CSUF = '\033[0m'

    ccode = ""
    if attrib:
        for attr in attrib.lower().split():
            attr = attr.strip(",+|")
            if attr in CATTRS:
                ccode += ";" + CATTRS[attr]
    if color in COLORS:
        ccode += ";" + COLORS[color]
    return CPRE + ccode + "m" + text + CSUF


def green(text, attrib=None):
    """Wrapper for colorize(text, 'green')"""
    return colorize(text, "green", attrib)


def red(text, attrib=None):
    """Wrapper for colorize(text, 'red')"""
    return colorize(text, "red", attrib)


def yellow(text, attrib=None):
    """Wrapper for colorize(text, 'yellow')"""
    return colorize(text, "yellow", attrib)


def blue(text, attrib=None):
    """Wrapper for colorize(text, 'blue')"""
    return colorize(text, "blue", attrib)


class Peda(Gdb):
    def __init__(self, prog, until=None):
        self._prompt = "\001%s\002" % red("\002gdb-peda$ \001")
        super(Peda, self).__init__(prog, until)

    def _init(self):
        self._waitprompt()
        self._loadfile()

    def _waitprompt(self):
        return self._process.recvuntil(self._prompt)[:-len(self._prompt)]

    def disass(self, what):
        self.send("pdisass %s" % what)
        return self._waitprompt()

    def goto(self, where):
        self.send("goto %s" % where)
        return self._waitprompt()

    def help(self, cmd="peda"):
        self.send("help %s" % cmd)
        return self._waitprompt()

    def nextcall(self, where):
        self.send("nextcall %s" % where)
        return self._waitprompt()

    def nextjmp(self, where):
        self.send("nextjmp %s" % where)
        return self._waitprompt()

    def refsearch(self, what):
        self.send("refsearch %s" % what)
        return self._waitprompt()

    def searchmem(self, what):
        self.send("searchmem %s" % what)
        return self._waitprompt()

    def session(self):
        return open("peda-session-%s.txt" % self._prog.replace("./", "")).read()

    def skipi(self, number):
        self.send("skipi %s" % number)
        return self._waitprompt()

    def start(self):
        self.send("start")

    def stepuntil(self, where):
        self.send("stepuntil %s" % where)
        return self._waitprompt()

    def unptrace(self):
        self.send("unptrace")
        return self._waitprompt()

    def vmmap(self):
        self.send("vmmap")
        return self._waitprompt()

    def xrefs(self, where):
        self.send("xrefs %s" % where)
        return self._waitprompt()

    def xinfo(self, where):
        self.send("xinfo %s" % where)
        return self._waitprompt()

    def xormem(self, xfrom, xto, key):
        self.send("xormem %s %s %s" % (xfrom, xto, key))
        return self._waitprompt()

    def xuntil(self, where):
        self.send("xuntil %s" % where)
        return self._waitprompt()

    # TODO
    def heap(self):
        mmap = self.vmmap().splitlines()
        for i in mmap:
            if "[heap]" in i:
                heap_start = i.split()[0].strip("\x1b[m")
                heap_end = i.split()[1]
                heap_perm = i.split()[2]
        print(self.x(heap_start, "gx", 200))
        return heap_start, heap_end, heap_perm
