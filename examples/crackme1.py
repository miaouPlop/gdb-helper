# coding=utf-8


from gdbhelper import Gdb


debug = Gdb("./crackme1")  # (1)
debug.bp("*0x8048545")  # (2)
debug.r("blurp", prompt=True)  # (3)
value = debug.reg("esp")[1]  # (4)
print(debug.x(value, "s"))  # (5)
