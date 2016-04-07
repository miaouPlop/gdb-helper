# coding=utf-8


from gdbhelper import Peda


debug = Peda("./crackme2", until="plz! \n")  # (1)
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
