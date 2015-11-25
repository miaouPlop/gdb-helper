# coding=utf-8


from pwn import *


class Gdb(object):
    def __init__(self, prog):
        self._prog = prog
        self._process = process(["gdb"])
        self._init()

    def _init(self):
        self._waitprompt()
        self._loadfile()

    def _quit(self):
        self._process.sendline("quit")

    def _waitprompt(self):
        return self._process.recvuntil("gdb")[:-3]

    def _loadfile(self):
        self._process.sendline("file %s" % self._prog)
        self._waitprompt()

    def send(self, what):
        self._process.sendline(what)

    def recv(self, until=None):
        if until is None:
            return self._process.recv()
        else:
            return self._process.recvuntil(until)

    def recvuntilprompt(self):
        return self._waitprompt()

    def interactive(self):
        self._process.interactive()

    def bp(self, where):
        self.send("break %s" % where)
        return self._waitprompt()

    def bt(self):
        self.send("backtrace")
        return self._waitprompt()

    def c(self, until=None):
        self.send("continue")
        return self.recv(until)

    def disass(self, what):
        self.send("disassemble %s" % what)
        return self._waitprompt()

    def e(self, what, until=None, prompt=False):
        self.send(what)
        if prompt is True:
            return self._waitprompt()
        else:
            return self.recv(until)

    def hb(self, where):
        self.send("hbreak %s" % where)
        return self._waitprompt()

    def help(self, cmd=""):
        self.send("help %s" % cmd)
        return self._waitprompt()

    def ni(self):
        self.send("nexti")
        return self._waitprompt()

    def quit(self):
        self._quit()

    def reg(self, name):
        x = self.x("$%s" % name)[1:]
        reg, value = x.split(":")
        return reg, value.strip()

    def r(self, until=None):
        self.send("run")
        return self.recv(until)

    def set(self, key, value):
        self.send("set %s=%s" % (key, value))
        return self._waitprompt()

    def si(self):
        self.send("stepi")
        return self._waitprompt()

    def watch(self, where):
        self.send("watch %s" % where)
        return self._waitprompt()

    def x(self, where, what="x", number=1):
        self.send("x/%d%s %s" % (number, what, where))
        return self._waitprompt()
