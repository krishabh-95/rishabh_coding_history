def isBinary(S):
    arr=[ele for ele in S.split()]
    
    children, parents=[],[]
    
    for i in arr:
        s1=int(i[1:i.index(',')])
        s2=int(i[i.index(',')+1:len(i)-1])
        
        if s1 in children:
            print('false')
            exit(0)
        
        count=0
        for j in parents:
            if j==s2:
                count+=1
                if count==2:
                    break
        
        if count==2:
            print('false')
            exit(0)
        
        children.append(s1)
        parents.append(s2)
    
    print('true')

if __name__=='__main__':
    S=input()
    isBinary(S)