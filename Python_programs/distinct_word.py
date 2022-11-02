#hackerrank problem

n=int(input())
S=[]
dic={}
for i in range(n):
    S.append(input())
    if dic.get(S[i]) is not None:
        dic.update({S[i]:dic.get(S[i])+1})
    else:
        dic.update({S[i]:1})

sets=set(S)

print(len(sets))

for i in range(n):
    if dic.get(S[i]) is not None:
        print(dic.get(S[i]), end=' ')
        dic.pop(S[i])