def getRanges(ranges, indVals, lis, ind):

    if ind<len(indVals):
        if ind<len(indVals)-1:
            for m in range(len(indVals[ind])):
                if indVals[ind][m] in lis:
                    continue
                lis.append(indVals[ind][m])
                getRanges(ranges, indVals, lis, ind+1)
                lis.pop()
        else:
            for n in indVals[ind]:
                if n in lis:
                    continue
                lis.append(n)
                getExtremes(ranges, lis)
                lis.pop()
                
def getExtremes(ranges,l):
    least,greatest=None,None
    
    for i in l:
        if least is None or least>i:
            least=i
        if greatest is None or greatest<i:
            greatest=i
    
    diff=greatest-least   

    ranges.update({diff: [least,greatest]})

def getSubString(arr):
    N=arr.split()[0]
    K=arr.split()[1]
    indices={}
    for i in K:
        val=N.find(i)
        vals=[]

        while val>-1:
            vals.append(val)
            val=N.find(i, val+1)
        
        while indices.get(i) is not None:
            i=i+'_'
            
        indices.update({i: vals})
    
    indVals=list(indices.values())
    ranges={}
    lis=[]
    getRanges(ranges, indVals, lis, 0)           
    least=None
    
    for x in ranges.keys():
        if least is None or least>x:
            least=x
    
    sub=ranges.get(least)
    print(N[sub[0]:sub[1]+1])
    
if __name__=='__main__':
    arr=input()
    
    getSubString(arr)
