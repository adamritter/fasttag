# try to crash the program by using a large input
from fasttag import *
a = Div(" ")
for i in range(10000):
    # print("len(a):", len(a.bytes()))
    a = Div(a)