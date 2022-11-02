#testing program

import platform
import sys

print('the python version is {}'.format(platform.python_version()))

a=25
b=25

if a<=b:
    print('yes')
    c=99
print('c is', c)

if a<b:
    print("first one")
elif b<a:
    print('Next one')
else:
    print('last one')
    print('both are equal')

arr=[1,2,3]

n=0
while n<3:
    print('The value is',arr[n])
    n+=1

words=["one",'two','three']

for i in words:
    print(i)