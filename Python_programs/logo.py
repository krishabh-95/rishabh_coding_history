#hackerrank

def get_chars(cdic, val):
    l=[]
    for k,v in cdic.items():
        if v==val:
            l.append(k)
    return l

def get_logo(S):
    cdic={}
    
    for i in range(len(S)):
        if (S[i] in cdic.keys()):
            val=cdic.get(S[i])
            cdic.update({S[i]: val+1})
        else:
            cdic.update({S[i]:1})
    
    valList=list(cdic.values())
    for i in range(len(valList)):
        v=valList[i]
        j=i
        base_of_largest=j
        while j < len(valList):
            if valList[j] > v:
                v=valList[j]
                base_of_largest=j
            j+=1
        
        if i!=base_of_largest:  
            temp=valList[i]
            valList[i]=valList[base_of_largest]
            valList[base_of_largest]=temp
    index=0
    u=0
    
    while u < len(valList) and u<=2:
        val=valList[u]
        l=get_chars(cdic, val)
        
        if len(l)==1:
            print('{} {}'.format(l[0],val))
            index+=1
        else:
            u+=len(l)-1
            
            for o in range(len(l)): 
                if o==3:
                    break

                value=ord(l[o])
                p=o
                base_of_smallest=p
                
                while p < len(l):

                    if ord(l[p]) < value:   
                        value=ord(l[p])
                        base_of_smallest=p
                    p+=1
                

                if o!=base_of_smallest:
                    temp=l[o]
                    l[o]=l[base_of_smallest]
                    l[base_of_smallest]=temp
            ind=0
            
            while index<3 and ind < len(l):
                print('{} {}'.format(l[ind],val))
                ind+=1
                index+=1
        u+=1
    

if __name__=='__main__':
    S=input()
    get_logo(S)