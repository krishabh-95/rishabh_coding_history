import sys
import math

def add(N,M):
    num=[]
    num.append(N[0]+M[0])
    num.append(N[1]+M[1])
    if num[1]>=0:
        print(f'{num[0]:.2f}+{num[1]:.2F}i')
    else:
        print(f'{num[0]:.2f}{num[1]:.2F}i')
        
def subtract(N,M):
    num=[]
    num.append(N[0]-M[0])
    num.append(N[1]-M[1])
    if num[1]>=0:
        print(f'{num[0]:.2f}+{num[1]:.2F}i')
    else:
        print(f'{num[0]:.2f}{num[1]:.2F}i')

def multiply(N,M):
    num=[]
    num.append(N[0]*M[0]+N[1]*M[1]*(-1))
    num.append(N[0]*M[1]+N[1]*M[0])
    if num[1]>=0:
        print(f'{num[0]:.2f}+{num[1]:.2F}i')
    else:
        print(f'{num[0]:.2f}{num[1]:.2F}i')
        
    return num

def divide(N,M):
    conjugate=[M[0],-M[1]]
    prod=multiply(N,conjugate)
    den=conjugate[0]*conjugate[0]-M[1]*M[1]*(-1)
    prod[0]=prod[0]/den
    prod[1]=prod[1]/den
    if prod[1]>=0:
        print(f'{prod[0]:.2f}+{prod[1]:.2F}i')
    else:
        print(f'{prod[0]:.2f}{prod[1]:.2F}i')    
       

def modulo(N):
    val=N[0]*N[0]+N[1]*N[1]
    print(f'{math.sqrt(val):.2f}+0.00i')

if __name__=='__main__':

    N,M=[],[]
    for line in sys.stdin:
        if len(N)==0:
            N=[int(ele) for ele in line.split()]
        else:
            M=[int(ele) for ele in line.split()]
            break
    
    add(N,M)
    subtract(N,M)
    multiply(N,M)
    divide(N,M)
    modulo(N)
    modulo(M)