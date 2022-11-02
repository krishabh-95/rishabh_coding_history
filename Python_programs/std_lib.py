import os
import sys
import class1
from test import classes

sys.path.append('D:\\Study Materials\\Python\\Ex_Files_Python_EssT\\Ex_Files_Python_EssT\\Exercise Files')

from Chap01 import hello

print(os.getenv('PATH'))
print(os.getcwd())

Stu=class1.student()
Stu.register(11)

c1=classes.Car('Audi','R8')
print(c1)

print(sys.path)

print('FINALLY\n:')
hello.printsomething()