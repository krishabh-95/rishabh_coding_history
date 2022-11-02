def matchBr(st):
    ob,cb=0,0
    
    for i in st:
        if i=='(':
            ob+=1
        elif i==')':
            cb+=1
    
    if ob==cb:
        print('1')
    else:
        print('0')

if __name__=='__main__':
    st=input()
    matchBr(st)