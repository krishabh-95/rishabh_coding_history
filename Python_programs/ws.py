#testing program

import platform
import sys

def msg():
    print('The python version is ',format(platform.python_version()))
    print('Job done.')
    if False:
        print('yes')
    else:
        print('no')

def test():
    x=100
    print(f'The number is {x}')
    print(sys.getsizeof(x))

print('Execution has begun')   
msg()

if __name__ == '__main__': test()