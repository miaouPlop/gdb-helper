# gdb-helper
Lightweight helper class to instrument GDB using Python


## Usage
```python
# coding=utf-8


from PedaHelper import Peda


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
