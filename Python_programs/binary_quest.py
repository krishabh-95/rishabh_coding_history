import sys

def sequenceCheck(x,y,a,b):
    if a>b or b>y:
        return False
        
    

if __name__=='__main__':
    T=int(input())
    arr=[]
    
    for line in sys.stdin:
        l=[int(e) for e in line.split()]
        arr.append(l)
        if len(arr)==T:
            break
    
    for l in arr:
        x,y,a,b=l[0],l[1],l[2],l[3]
        
        val=sequenceCheck(x,y,a,b)