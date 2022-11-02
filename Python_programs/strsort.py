#hackerrank problem

S=input()

lcase=[]
ucase=[]
odigits=[]
edigits=[]

for i in range(len(S)):
    if S[i].isdigit():
        num=int(S[i])
        if num%2==0:
            edigits.append(S[i])
        else:
            odigits.append(S[i])
    elif S[i].isupper():
        ucase.append(S[i])
    elif S[i].islower():
        lcase.append(S[i])
    else:
        sys.exit('Invalid input')

lcase.sort()
ucase.sort()
odigits.sort()
edigits.sort()

finalStr=lcase+ucase+odigits+edigits

for i in range(len(finalStr)):
    print(finalStr[i],end='')
