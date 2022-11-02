#hackerrank

def is_next_character_same(c,S,i):
    if (i+1) < len(S):
        if S[i+1]==c:
            return True
        else:
            return False
    else:
        return False

def modify_string(S):
    temp=''
    pattern='(X, c)'
    
    i=0
    count=0
    while i<len(S):
        c=S[i]
        count+=1
        
        while is_next_character_same(c,S,i):
            count+=1
            i+=1
            
        i+=1
        
        pstr=pattern.replace('X',str(count))
        pstr=pstr.replace('c',c)
        temp+=pstr+' '
        count=0
        
    print(temp)
    
if __name__=='__main__':
    S=input()
    modify_string(S)