#hackerrank problem

import numpy as np
import sys

if __name__=='__main__':
    i = 0
    arr=[]
    for line in sys.stdin:
        if i==0:
            N=int(line.split()[0])
            M=int(line.split()[1])
            i+=1
        else:
            if i==N+1:
                K=int(line.split()[0])
                break
            else:
                arr.append([int(ele) for ele in line.split()])
                i+=1
    
    mat=np.array(arr)
    
    if K>=M:
        sys.exit('Invalid input')
    
    for j in range(mat.shape[0]):
        val=mat[j][K]
        least_base=j
        l=j

        while l < mat.shape[0]:
            if val > mat[l][K]:
                val=mat[l][K]
                least_base=l
            l+=1
        mat[[j, least_base]] = mat[[least_base, j]]
    
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            print(mat[i][j], end=' ')
        print()