def str_rev(s):
    newStr=''
    
    for i in range(len(s)):
        newStr+=s[len(s)-1-i]
    return newStr

print(str_rev(input()))