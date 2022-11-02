# string type

import platform
import sys

print('The python version is ', platform.python_version())

s='''I am AweSome

'''.lower()

print(s)
print("It size is {}".format(sys.getsizeof(s)))

country='Australia'
x='I am Rishabh and I study at {2:>015} in {0:<011},{1}'.format('Swinburne','Victoria',country)

print(x)
print("This is the {} of {}")