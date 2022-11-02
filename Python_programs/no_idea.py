# hackerrank problem
import sys

def calculate_happiness(arr,A,B):
    h=0
    for i in arr:
        if i in A:
            h+=1
        elif i in B:
            h-=1
    print(h)

if __name__=='__main__':
    i=0
    for line in sys.stdin:
        if i==0:
            n=int(line.split()[0])
            m=int(line.split()[1])
            i+=1
        elif i==1:
            arr=[int(ele) for ele in line.split()]
            i+=1
        elif i==2:
            A=[int(ele) for ele in line.split()]
            i+=1
        elif i==3:
            B=[int(ele) for ele in line.split()]
            break
    
    if len(arr)!=n or len(A)!=m or len(B)!=m:
        print('The size of one of the arrays you have entered does not match the required length')
        exit()
    
    A=set(A)
    B=set(B)
        
    calculate_happiness(arr,A,B)
    
