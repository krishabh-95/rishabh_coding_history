import sys

def func(l, M):
    total=0
    for i in l:
        total+=i*i
    return total%M

def calculateVals(vals, ind, M, lists, t):
    if ind<len(lists):
        if ind==len(lists)-1:   
            for m in range(len(lists[ind])):
                vals.append(func(t+[lists[ind][m]], M))
        else:
            for m in range(len(lists[ind])):
                t+=[lists[ind][m]]
                calculateVals(vals, ind+1, M, lists, t)
                t.pop()
    elif len(lists)==1:
        vals.append(func(t, M))
        

def getMax(l):
    maxVal=None
    for i in l:
        if maxVal is None or maxVal<i:
            maxVal=i
    return maxVal
    
if __name__=='__main__':
    lists=[]
    ind=True
    
    for line in sys.stdin:
        if ind:
            K=int(line.split()[0])
            M=int(line.split()[1])
            ind=False
        else:
            arr=[int(ele) for ele in line.split()]
            arr.pop(0)
            lists.append(arr)
            if len(lists)==K:
                break
        
    vals=[]
    
    i=0
    if i<len(lists):
        for j in range(len(lists[i])):
            t=[lists[i][j]]
            calculateVals(vals, i+1, M, lists, t)
    
    print(getMax(vals))
            