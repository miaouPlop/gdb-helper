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
The script uses [pwntools](https://github.com/Gallopsled/pwntools)'s "process" to launch GDB in a subprocess and
communicate with it. Then it basically sends GDB commands like "run", "breakpoint", etc. to instrument it.


```python
from pedahelper import *
debug = Gdb("./examples/crackme1")
```

## Dependancies
[pwntools](https://github.com/Gallopsled/pwntools)

[libheap](https://github.com/cloudburst/libheap)


You should also get [peda](https://github.com/longld/peda)


## Usage
```python
# coding=utf-8


from pedahelper import Peda


debug = Peda("./abcd", until=">")
debug.bp("*0x0000000000400b69")
debug.r(until="show\n>")
debug.e("new %s" % ("A"*0x75))
debug.e("new %s" % ("A"*0x107))
show = debug.e("show")
user_id = show.split("ID")[1].split("= ")[1].split("\n")[0]
debug.e("free %s" % user_id, prompt=True)
rax, value = debug.reg("rax")
debug.ni()
show = debug.x("0x603000", "gx", 100)
debug.c()
user_id = show.split("ID")[1].split("= ")[1].split("\n")[0]
debug.e("free %s" % user_id, skipbp=True)
debug.e("new %s" % ("A"*0x107))
show = debug.e("show")
user_id = show.split("ID")[1].split("= ")[1].split("\n")[0]
debug.e("free %s" % user_id, prompt=True)
debug.i()

```
