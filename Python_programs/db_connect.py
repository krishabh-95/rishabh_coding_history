import sqlite3

db=sqlite3.connect('test.db')
cur=db.cursor()
cur.execute('drop table if exists test')
cur.execute('create table test (ID bigint, NAME varchar(10), primary key(ID))')
cur.execute('insert into test(ID, NAME) values (1,"Rishabh")')
db.commit()
print('test')
db.close()