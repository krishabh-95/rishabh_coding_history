import sys
import re

mat=[]
ind=True
    
vals=input().rstrip().split()

N=int(vals[0])
M=int(vals[1])

for x in range(N):
    row=input()
    mat.append(row)
    
st=''
    
for i in range(M):
    for j in range(N):
        st+=mat[j][i]

l=re.findall('[A-Za-z0-9]+', st)

start_ind=st.find(l[0])
end_ind=st.rfind(l[len(l)-1])
fstr=st[0:start_ind]

for sub in range(len(l)):
    fstr+=l[sub]+' '

fstr+='\b'
    
fstr+=st[end_ind+len(l[len(l)-1]):len(st)]
print(fstr)        
