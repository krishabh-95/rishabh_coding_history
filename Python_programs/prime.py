# finding prime numbers

import platform
import sys

print('The python version is {}'.format(platform.python_version()))

def isprime(a):
    if a<=1:
        return 'prime'
    else:
        for x in range(2,a):
            if a % x==0:
                return 'not prime'
        return 'prime'
            
def fn(a=10,b=15):
    print('Function execution has started')
    print('function execution ended')
    return a*b
    
x=fn(5)

def temp():
    print('Testing')

print(f'The function has returned {x} and {x+1}')

print(temp())

num=15

print('num is a {} number'.format(isprime(num)))

    