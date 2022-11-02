import sys
import re

if __name__=='__main__':
    mat=[]
    ind=True
    
    for line in sys.stdin:
        if ind:
            ind=False
            N=int(line.split()[0])
            M=int(line.split()[1])
        else:
            mat.append(line)
            if len(mat)==N:
                break
    
    st=''
    
    for i in range(M):
        for j in range(N):
            st+=mat[j][i]
    
    l=re.findall('[A-Za-z0-9]+', st)
    
    if len(l)>0:
        start_ind=st.index(l[0])
        end_ind=st.rfind(l[len(l)-1])
        fstr=st[0:start_ind]
        
        for sub in range(len(l)):
            if sub==len(l)-1:
                fstr+=l[sub]
            else:
                fstr+=l[sub]+' '
        
        fstr+=st[end_ind+len(l[len(l)-1]):len(st)]
        print(fstr)        
    else:
        print(st)