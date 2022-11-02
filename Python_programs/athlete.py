import sys

if __name__=='__main__':
    tab=[]
    ind=0
    
    N,M=-1,-1
    
    for line in sys.stdin:
        if ind==0:
            N=int(line.split()[0])
            M=int(line.split()[1])
            ind+=1
        elif ind>0 and ind<N+1:
            tab.append([int(e) for e in line.split()])
            ind+=1
        else:
            K=int(line.split()[0])
            break
    
    for i in range(len(tab)-1):
        for j in range(len(tab)-i-1):
            if tab[j][K] > tab[j+1][K]:
                temp=tab[j]
                tab[j]=tab[j+1]
                tab[j+1]=temp
        
    for i in range(len(tab)):
        for j in range(M):
            print(tab[i][j], end=' ')
        print()