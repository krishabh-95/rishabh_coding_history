#hackerrank

import re

#To check if 4 consecutive numbers are the same
def conse_chars(C):
    for i in range(len(C)):
        ch=C[i]
        count=1
        if (i+1)<len(C) and C[i+1]=='-':
            i+=1
        while (i+1)<len(C) and ch==C[i+1]:  
            count+=1
            i+=1
            if count==4:
                return False
            if (i+1)<len(C) and C[i+1]=='-':
                i+=1
            
    return True

def remaining_crit(C):
    if len(C)!=16 and len(C)!=19:
        return False
    elif len(C)==16 and (not re.search("[0-9]",C)):
        return False
    elif not conse_chars(C):
        return False
    elif len(C)==19:
        if not re.search("[0-9]",C[:4]) or not re.search("[0-9]",C[5:9]) or not re.search("[0-9]",C[10:14]) or not re.search("[0-9]", C[15:19]):
            return False
        if C[4]!='-' or C[9]!='-' or C[14]!='-':
            return False
    return True
            

def validate_card(C):
    valid=True
    
    if re.search("^4|^5|^6",C) and remaining_crit(C):  
        return 'Valid'
    return 'Invalid'
if __name__=='__main__':
    N=int(input())
    S=[]
    
    for i in range(N):
        S.append(input())
    
    for i in range(N):
        print(validate_card(S[i]))