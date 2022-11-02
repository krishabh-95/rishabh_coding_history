#hackerrank problem

vowels=('A','E','I','O','U')

def kevin_pts(S):
    pts=0
    
    for i in range(len(S)):
        if S[i] in vowels:
            pts+=(len(S)-i)
    return pts

def stuart_pts(S):
    pts=0
    
    for i in range(len(S)):
        if S[i] not in vowels:
            pts+=(len(S)-i)
    return pts

if __name__=='__main__':
    S=input()
    
    kp=kevin_pts(S)
    sp=stuart_pts(S)
    
    if kp < sp:
        print(f'Stuart {sp}')
    elif sp < kp:
        print(f'Kevin {kp}')
    else:
        print('Draw')