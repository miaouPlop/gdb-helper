# coding=utf-8


import signal
import psutil
from pwn import *


class Gdb(object):
    def __init__(self, prog, until=None):
        self._prog = prog
        self._until = until
        self._session = ""
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
            if self._until is None:
                return self._process.recv()
            else:
                return self._process.recvuntil(self._until, timeout=1)
        else:
            return self._process.recvuntil(until, timeout=1)

    def recvuntilprompt(self):
        return self._waitprompt()

    def execute(self, what, until=None, prompt=False, skipbp=False,
                nosession=False):
        if until is not None and skipbp is True:
            raise AttributeError("Until attribute can't be used with "
                                 "skipbp attribute")
        if nosession is False:
            self._session += "%s\n" % what
        self.send(what)
        if skipbp is True:
            ret = self._waitprompt()
            ret += self.c(until)
            return ret
        else:
            if prompt is True:
                return self._waitprompt()
            else:
                return self.recv(until)

    def e(self, what, until=None, prompt=False, skipbp=False,
          nosession=False):
        return self.execute(what, until, prompt, skipbp, nosession)

    def interactive(self):
        self._process.interactive()

    def i(self):
        self.interactive()

    def session(self):
        return self._session

    def sigint(self):
        for p in psutil.process_iter():
            if p.parent() is not None:
                if p.parent().name() == "gdb" \
                        and p.name() in self._prog:
                    p.send_signal(signal.SIGINT)
                    break
        # essential because it intercepts the "quit" before it is sent
        # to the debugger
        return self._waitprompt()

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
