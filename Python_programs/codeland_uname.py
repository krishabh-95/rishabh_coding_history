import re

def CodelandUsernameValidation(strParam):
    val=True
    
    if not re.match("^[a-zA-Z]",strParam) or not re.match("^[_a-zA-Z0-9]+$",strParam) or re.match("[_]$", strParam) or len(strParam)<4 or len(strParam)>25:
        val=False
    
    return val

# keep this function call here 
print(CodelandUsernameValidation(input()))