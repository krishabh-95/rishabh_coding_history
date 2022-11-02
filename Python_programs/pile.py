#hackerrank

import sys

def is_piling_possible(arr, n):
    i=0
    is_possible=True
    
    final_list=[]
    
    while i<n:
        if arr[i] < arr[n-1-i]:
            final_list.append(arr[n-1-i])
            arr.pop(n-1-i)
        else:
            final_list.append(arr[i])
            arr.pop(i)

        if len(final_list)>1:
            if final_list[len(final_list)-1]>final_list[len(final_list)-2]:
                is_possible=False
                break            
        n=len(arr)
                
    return is_possible

if __name__=='__main__':
    T=int(input())
    n=[]
    arr=[]
    
    number=True
    i=0

    for line in sys.stdin:
        if i==T:
            break
        if number:
            n.append(int(line.split()[0]))
            number=False
        else:
            arr.append([int(e) for e in line.split()])
            number=True
            i+=1
            if i==T:
                break
            
    for i in range(T):        
        num=n[i]
        A=arr[i]
        
        if len(A)!=num:
            sys.exit('Invalid input')
        
        if is_piling_possible(A, num):
            print('Yes')
        else:
            print('No')
        