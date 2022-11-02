import mysql.connector
from mysql.connector import Error

conn=mysql.connector.connect(host='localhost',user='root',database='location_database',password='IAmAwesome',connection_timeout=150)
    
if conn.is_connected():
    try:
        print('Connected to the database')
        cur=conn.cursor()
        sql='CREATE TABLE Location(ID bigint, DISTRICT_ID integer, PINCODE integer, primary key(ID))'
        cur.execute(sql)
        print('Created the table Location')
        
        sql='CREATE TABLE People(ID bigint, TO_ADDRESS varchar(100) not null, FROM_IP varchar(60), LOCATION_ID bigint, primary key(ID), foreign key(LOCATION_ID) references Location(ID) on delete cascade)'
        cur.execute(sql)
             
        print('Created the table People')
        
        sql='CREATE TABLE UnverifiedPeople(ID bigint, TO_ADDRESS varchar(100) not null, FROM_IP varchar(60), OTP integer, TIME datetime, primary key(ID))'
        cur.execute(sql)
        conn.commit()
    except mysql.connector.Error as e:
        print('Error occured while creating the tables', e)

    if conn.is_connected():
        cur.close()
        conn.close()
else:   
    print('Failed to connect to the database')