# integer type

import platform
import sys

from decimal import *

print('The python version is {}'.format(platform.python_version()))

x=Decimal('9.9')

print('The number is ',x,' its size is ', sys.getsizeof(x),' and type is ', type(x))

a=Decimal('.1')
b=Decimal('.2')

c=a+a-b
print(c, ' and its type is ', type(c))

ex=None

print('The value is {} and its type is {}. Its size is {}'.format(ex, type(ex), sys.getsizeof(ex)))

ex=199.0

print(type(ex))

# lists, tuples, dictionaries

arr = range(4,10,4)
for i in arr:
    print(i)
    
print('arr''s size is {}'.format(sys.getsizeof(arr)))

dic={1:"Rishabh",2:"Balaji",3:"Venky",4:"Abhishek"}

for k, v in dic.items():
    print(k,' : ', v)
print('type is ',type(dic))

var=[1,'Rock',None,4,4]
var2=(1,6,7,8)

print(id(var))
print(id(var2))

if isinstance(dic, dict):
    print("yes")
else:
    print("no")
