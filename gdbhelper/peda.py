# coding=utf-8


from .gdb import Gdb
from util.colors import colorize


def green(text):
    """Wrapper for colorize(text, 'green')"""
    return colorize(text, "green")


def red(text):
    """Wrapper for colorize(text, 'red')"""
    return colorize(text, "red")


def yellow(text):
    """Wrapper for colorize(text, 'yellow')"""
    return colorize(text, "yellow")


def blue(text):
    """Wrapper for colorize(text, 'blue')"""
    return colorize(text, "blue")


class Peda(Gdb):
    def __init__(self, prog, until=None):
        prompt = "\001%s\002" % red("\002gdb-peda$ \001")
        procname = "peda"
        super(Peda, self).__init__(prog, until, prompt, procname)

    def aslr(self, what="on"):
        self.send("aslr %s" % what)
        return self._waitprompt()

    def disass(self, what):
        self.send("pdisass %s" % what)
        return self._waitprompt()

    def dumpmem(self, name, begin, end):
        self.send("dumpmem %s %s %s" % (name, begin, end))
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

    def pattern_create(self, count):
        self.send("pattern_create %d" % count)
        return self._waitprompt().replace("\x1b[0m", "").replace("\x1b[m", "").strip()

    def pattern_offset(self, pattern):
        self.send("pattern_offset %s" % pattern)
        return int(self._waitprompt().replace("\x1b[0m", "").replace("\x1b[m", "").strip().split("offset: ")[1])

    def pattern_search(self, pattern):
        self.send("pattern_search %s" % pattern)
        return self._waitprompt().replace("\x1b[0m", "").replace("\x1b[m", "").strip()

    def refsearch(self, what):
        self.send("refsearch %s" % what)
        return self._waitprompt()

    def searchmem(self, what):
        self.send("searchmem %s" % what)
        return self._waitprompt()

    def skipi(self, number):
        self.send("skipi %s" % number)
        return self._waitprompt()

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
        return None
