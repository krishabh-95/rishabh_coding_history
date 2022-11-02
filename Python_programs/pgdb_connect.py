# connecting to postgresql

import psycopg2

def connect():
    conn=psycopg2.connect(dbname="test",user="postgres",host="localhost",port="5432",password="IAmAwesome")

    cur=conn.cursor()
    sql='INSERT INTO Location(ID, NAME) VALUES (%s,%s);'
    cur.execute(sql,('4','Kolkata'))
    
    #sql='create table Users(ID integer, NAME varchar(40), SERVER varchar(40), MESSAGES varchar(40), PRIMARY KEY(ID));'
    #cur.execute(sql)

    sql='INSERT INTO Users(ID, NAME,SERVER,MESSAGES) VALUES (%s,%s,%s,%s);'
    cur.execute(sql,('1','Rishabh','MA-IT','Hi guys'))
    cur.execute(sql,('2','Swapnil','MA-IT','Hi'))
    cur.execute(sql,('3','Pratibha','MA-IT','Hi guys'))
    cur.execute(sql,('4','Gokul','MA-IT','Hi guys'))
    cur.execute(sql,('5','Saumya','MA-IT','Hi folks'))
    conn.commit()
    cur.close()
    conn.close()
    print('DONE!')
    
if __name__=='__main__':
    connect()