def getNoOfCombs(N):
    num=N*2
    count=1
    
    for i in range(1, num//2):
        ind=i
        pairs=0
        while ind<num-1-i:
            pairs+=1
            ind+=2
        count+=pow(2, pairs)-1
    
    return count
    

if __name__=='__main__':
    N=int(input())
    print(getNoOfCombs(N))