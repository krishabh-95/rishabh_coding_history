# hackerrank problem

def merge_tools(string, k):
    if k <1 or k>len(string):
        return 'Invalid input'
    
    i=0
    tempStr=''
    S=[]
    lines=len(string)//k
    size=len(string)//lines
    while i<len(string):
        tempStr+=string[i]
        i+=1
        if len(tempStr)==size:
            S.append(tempStr)
            tempStr=''
    
    index=0
    
    for i in S:
        sub=i
        T=[]
        for j in range(len(sub)):
            if sub[j] not in T:
                T.append(sub[j])
        S[index]=''.join([str(element) for element in T])
        index+=1
    
    for i in S:
        print(i)
        
if __name__== '__main__':
    string=input("Enter the string")
    k=int(input("Enter the value"))
    
    if merge_tools(string,k):
        print('Invalid input')
        