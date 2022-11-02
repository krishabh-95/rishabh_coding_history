
if __name__=='__main__':
    file=open('D:\\SanDisk\\temp.txt','w')
    # default mode is read 'r'
    l=['I','am','a','hero']
    print(l)
    for line in l:
        file.write(line+ ' ')

    file.close()
    
    li=['Dog','Monkey']
    file=open('test.txt','a')
    for line in li:
        file.write(line+' ')
    file.close()
    
    print('\nDone')