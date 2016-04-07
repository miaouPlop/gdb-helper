# coding=utf-8


from os import environ
from signal import SIGINT
from psutil import process_iter
from pwn import process


class Gdb(object):
    def __init__(self, prog, until=None, prompt="(gdb) ", procname="gdb"):
        self._target = prog
        self._until = until
        self._session = ""
        self._prompt = prompt
        self._procname = procname
        self._init()

    def _init(self):
        self._process = process([environ["SHELL"], "-i", "-c", self._procname + " -q"])
        self._process.recvrepeat(0.3)
        self.send("set confirm off")
        self._loadfile()

    def _loadfile(self):
        self.recv()
        self._process.sendline("file %s" % self._target)
        self._waitprompt()

    def _quit(self):
        self._process.sendline("quit")

    def _waitprompt(self):
        return self._process.recvuntil(self._prompt)[:-len(self._prompt)]

    def close(self):
        self._quit()

    def send(self, what):
        self._process.sendline(what)

    def recv(self, until=None, prompt=False):
        if until is None:
            if prompt is True:
                ret = self._waitprompt()
            elif self._until is None:
                ret = self._process.recv()
            else:
                # ret = self._process.recvuntil(self._until, timeout=1)
                ret = self._process.recvrepeat(0.1)
        else:
                ret = self._process.recvuntil(until, timeout=1)
        return ret

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

    def getprocess(self):
        for p in process_iter():
            # print(p.parent(), p.name())
            if p.parent() is not None:
                if p.parent().name() == "gdb" \
                        and p.name() in self._target:
                    return p

    def pid(self):
        return self.getprocess().pid

    def sigint(self):
        self.getprocess().send_signal(SIGINT)
        # essential because it intercepts the "quit" before it is sent
        # to the debugger
        return self._waitprompt()

    def bp(self, where):
        self.send("break %s" % where)
        return self._waitprompt()

    def bt(self):
        self.send("backtrace")
        return self._waitprompt()

    def c(self, until=None, prompt=False, skipbp=False):
        return self.execute("continue", until, prompt, skipbp)

    def dis(self, bp):
        self.send("disable %d" % bp)
        return self._waitprompt()

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

    def registers(self):
        self.send("info register")
        return self._waitprompt()

    def r(self, args=None, until=None, prompt=False, skipbp=False):
        if args is not None:
            cmd = "run %s" % args
        else:
            cmd = "run"
        return self.execute(cmd, until, prompt, skipbp)

    def set(self, key, value):
        self.send("set %s=%s" % (key, value))
        return self._waitprompt()

    def si(self):
        self.send("stepi")
        return self._waitprompt()

    def start(self):
        self.send("start")
        return self._waitprompt()

    def watch(self, where):
        self.send("watch %s" % where)
        return self._waitprompt()

    def x(self, where, what="x", number=1):
        self.send("x/%d%s %s" % (number, what, where))
        return self._waitprompt()
