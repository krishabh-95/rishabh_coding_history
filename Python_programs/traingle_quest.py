if __name__=='__main__':
    N=int(input())
    
    for i in range(1,N+1):
        num=1
        for j in range(i*2-1):
            print(num,end='')
            if j >= (i*2-1)//2:
                num-=1
            else:
                num+=1
        print()
        