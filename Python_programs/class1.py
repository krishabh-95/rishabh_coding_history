# classes intro

import platform
import sys

print('The python version is ',platform.python_version())
print(sys.getsizeof('The python version is {}'.format(platform.python_version())))

class student:
    ID=1
    name='random'
    
    def register(self,a):
        print('The student having ID {} and name {} has registered in {}'.format(self.ID,self.name,a))


Stu=student()
Stu.register(11)

num=10
Num=101

print(num,' and ',Num)
