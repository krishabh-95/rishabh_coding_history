import re

def fun(s):
    loc=s.find("@")
    if loc==-1:
        return False
    else:
        un=s[0:loc]
        
        if not re.match('^[-_a-zA-Z0-9]+$', un):
            return False
        
        loc2=s.find(".")

        if loc2==-1:
            return False
        else:
            wb=s[loc+1:loc2]
            
            if not re.match('^[a-zA-Z0-9]+$',wb):
                return False
            
            ext=s[loc2+1:len(s)]

            if not re.match('^[a-zA-Z]+$',ext) or len(ext)>3:
                return False
            else:
                return True

def filter_mail(emails):
    return list(filter(fun, emails))

if __name__ == '__main__':
    n = int(input())
    emails = []
    for _ in range(n):
        emails.append(input())

    filtered_emails = filter_mail(emails)
    filtered_emails.sort()
    print(filtered_emails)