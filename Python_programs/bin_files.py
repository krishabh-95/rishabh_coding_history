#reading from binary files

if __name__=='__main__':
    file=open("IMG_4401.MOV",'rb')
    out=open("CopyIMG_4401.MOV", 'wb')
    index=0
    try:
    
        while True:
            buf=file.read(1000)
            
            if buf:
                out.write(buf)
                index+=1
            else:
                break
            
            print('.',end='',flush=True)
        
        out.close()
        
        print('DONE')
    except Error as e:
        print('An error occurred', e)
        
        
    tf = open('Test.txt', 'rt')
    
    print(tf)
    print(tf.encoding)
    for line in tf:
        print(line)
        
    ch='A'
    print(ord(ch))
    num=100
    print(chr(num))
    
    x=(1,2,3)
    y=x