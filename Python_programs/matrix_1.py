import re

nums= input().split()

n=int(nums[0])
m=int(nums[1])

matrix=[]

for i in range(n):
    matrix.append(input())

string=''

print(matrix)

for j in range(3):
    for i in range(n):
        st=matrix[i]
        string+=st[j]

l1=re.split('[^a-zA-Z0-9]', string)
try:
    while True:
        l1.remove('')
except ValueError:
    pass

l2=re.split('[a-zA-Z0-9$]', string)
try:
    while True:
        l2.remove('')
except ValueError:
    pass

print(l1)
print(l2)
