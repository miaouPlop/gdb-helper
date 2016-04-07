# coding=utf-8


from gdbhelper import Gdb


debug = Gdb("./crackme1")
debug.bp("*0x8048545")  # (1)
debug.r("blurp", prompt=True)  # (2)
value = debug.reg("esp")[1]  # (3)
print(debug.x(value, "s"))  # (4)
