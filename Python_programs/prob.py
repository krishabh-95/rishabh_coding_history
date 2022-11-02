import sys

def factorial(val):
    if val<=1:
        return 1
    else:
        return val*factorial(val-1)

def combine(l, val, arr, combs, ind):
    if val==len(arr)-ind-1:
        l=l+arr[ind+1:len(arr)]
        combs.append(l)
    else:
        for i in range(ind+1,len(arr)):
            if val>1:
                combine(l+list(arr[i]), val-1, arr, combs, i)
            else:
                if val==1:
                    for j in arr[ind+1:len(arr)]:
                        combs.append(l+list(j))
                    break
                else:
                    combs.append(l)
                    break
    
def getComb(arr,K):
    combs=[]
    
    for i in range(len(arr)):
        lis=[arr[i]]
        if K-1<=len(arr)-i-1:   
            combine(lis,K-1,arr,combs,i)
        else:
            break

    return combs

if __name__=='__main__':
    arr=[]
    ind=0
    
    for line in sys.stdin:
        if ind==0:
            N=int(line.split()[0])
            ind+=1
        elif ind==1:
            arr=[ele for ele in line.split()]
            ind+=1
        else:
            K=int(line.split()[0])
            break
    
    if len(arr)!=N:
        print('Invalid input')
        exit(0)

    combs=getComb(arr, K)
    combWithA=0
    
    for i in combs:
        if 'a' in i:
            combWithA+=1
    
    if len(combs)==0:
        print('0.000')
    else:
        print(f'{(combWithA/len(combs)):.3f}')
    
    
    