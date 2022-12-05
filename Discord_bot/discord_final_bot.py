import discord
import nltk
from discord.ext import commands
from nltk.corpus import abc
from nltk.corpus import stopwords
from discord import Intents 
from nltk.corpus import wordnet
import re
import os
import threading
import psycopg2
from os import path
from psycopg2 import OperationalError
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from datetime import datetime
import time

intents=Intents.all()  
intents.members=True 
isFilePresent=False
client=discord.Client(intents=intents)

def checkAndCreateDB():
    #To continue appending the log file if it already exists; otherwise it creates the log file
    if(isFilePresent):
        file=open('log.txt','a')
    else:
        file=open('log.txt','w')

    db_present=True
    
    try:
        conn=psycopg2.connect(dbname="disbot_db",user="postgres",host="localhost",port="5432",password="IAmAwesome")
    except OperationalError as err:
        #When you launch the application for the first time
        file.write(str(datetime.now())+":The database has not yet been created. So we are going to create it now.\n") 
        db_present=False
        conn=psycopg2.connect(user="postgres",host="localhost",port="5432",password="IAmAwesome")
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur=conn.cursor()
        cur.execute("CREATE DATABASE disbot_db")
        conn.commit()
        cur.close()
        conn.close()
        file.write("Database disbot_db has been successfully created.\n")
    
    conn=psycopg2.connect(dbname="disbot_db",user="postgres",host="localhost",port="5432",password="IAmAwesome")
    
    #Checking if the application is being run for the first time. If so, the database schema needs to be created
    if not db_present:
        #Create the database schema since the application is being run for the first time
        createDBSchema(conn)
        
    file.write(str(datetime.now())+": Connection to the PostgreSQL database successful.\n") 
    conn.close()
    file.close()

def createDBSchema(conn):
    cur=conn.cursor()
    #First let us create the independent tables
    cur.execute("create table Students(STUDENT_NO integer, DISCORD_USER_ID bigint not null, NAME varchar(50) not null, CONFIDENCE_RATING integer, KARMA_VALUE integer, primary key(STUDENT_NO))")
    cur.execute("create table Keytopics(TOPIC_NO integer, KEYWORD varchar(50) not null,DISCUSSION_COUNT integer, LAST_DISCUSSED_TIME timestamp, IS_NOTIFICATION_SENT bool, primary key(TOPIC_NO), UNIQUE(KEYWORD))")
    cur.execute("create table InstituteStaff(STAFF_ID integer, NAME varchar(50), DISCORD_USER_ID bigint not null, MAIL_ID varchar(50), IS_NOTIFICATION_NEEDED bool default true, LAST_NOTIFIED_TIME timestamp, primary key(STAFF_ID))")
    
    #Now we will create the dependent tables
    cur.execute("create table StudentTexts(ENTRY_NO integer, STUDENT_NO integer not null, SERVER_NAME varchar(100), CHANNEL_NAME varchar(100), GUILD_ID bigint not null, TOPIC_NO integer, KEYWORD varchar(50) not null, MESSAGE_ID bigint not null, MESSAGE_TIME timestamp, primary key(ENTRY_NO), foreign key (STUDENT_NO) references Students(STUDENT_NO) on delete cascade, foreign key (TOPIC_NO) references Keytopics(TOPIC_NO) on delete restrict)")
    cur.execute("create table NonConventionalAcademicTopics(TOPIC_NO integer, TOPIC_NAME varchar(50) not null,primary key(TOPIC_NO))")
    cur.execute("create table TopicStaffNotificationMapping(NOTIFICATION_ID integer,TOPIC_NO integer not null,STAFF_ID integer not null, NOTIFICATION_TIME timestamp, primary key(NOTIFICATION_ID), foreign key (STAFF_ID) references InstituteStaff(STAFF_ID) on delete cascade, foreign key (TOPIC_NO) references Keytopics(TOPIC_NO))")
    cur.execute("create table BlockedStudents(STUDENT_NO integer not null, GUILD_ID bigint not null, primary key(STUDENT_NO,GUILD_ID), foreign key (STUDENT_NO) references Students(STUDENT_NO) on delete cascade)")
    conn.commit()
    cur.close()

def addOrUpdateTopics(word, conn):
    cur=conn.cursor()
    query='select TOPIC_NO,DISCUSSION_COUNT from Keytopics where KEYWORD = %s'
    cur.execute(query, (word,))
    res=cur.fetchone()
    lock=threading.Lock()
    lock.acquire()
    
    if res is None:
        #Add this keyword to the database
        cur.execute('select max(TOPIC_NO) from Keytopics')
        res=cur.fetchone()
        maxVal=None
        
        if res[0] is None:
            maxVal=0
        else:
            maxVal=int(res[0])

        topic_no=maxVal+1
        
        sql='INSERT INTO Keytopics values (%s,%s,%s,now(),%s)'
        addKeyTopicToCloud(str(topic_no),word,'1','false')
        cur.execute(sql,(str(topic_no),word,'1','false'))
        conn.commit()
    else:
        topic_no=int(res[0])
        count=int(res[1])+1
        
        sql='UPDATE Keytopics set DISCUSSION_COUNT=%s , LAST_DISCUSSED_TIME=now(), IS_NOTIFICATION_SENT=false where TOPIC_NO='+str(topic_no)
        updateKeytopicOnCloud('UPDATE Keytopics set DISCUSSION_COUNT='+str(count)+' , LAST_DISCUSSED_TIME=now(), IS_NOTIFICATION_SENT=false where TOPIC_NO='+str(topic_no))
        cur.execute(sql, (str(count)))
        conn.commit()
        
    lock.release()
    cur.close()      
    
    return topic_no
 
#This method should be invoked while trying to alter the karma value of users.
def alterKValue(user_id, change_in_rating):
    conn=psycopg2.connect(dbname="disbot_db",user="postgres",host="localhost",port="5432",password="IAmAwesome")
    cur=conn.cursor()
    
    query='select KARMA_VALUE from Students where DISCORD_USER_ID = %s'
    cur.execute(query, (user_id,))
    res=cur.fetchone()
    
    #To continue appending the log file if it already exists; otherwise it creates the log file
    if(isFilePresent):
        file=open('log.txt','a')
    else:
        file=open('log.txt','w')
        
    if res is None:
        #This means the user is not present in the database 
        print('User not present in the database')
    else:
        file.write(str(datetime.now())+':Going to alter the confidence rating of this user by '+str(change_in_rating))
        newRating=int(res[0])+change_in_rating
        
        sql='UPDATE Students set KARMA_VALUE=%s where DISCORD_USER_ID = %s'
        cur.execute(sql, (str(newRating),str(user_id)))
        conn.commit()
    
    cur.close()
    conn.close()
    file.close()
 
#This method should be invoked while trying to alter the confidence rating of users.
def alterConfidenceRating(user_id, change_in_rating):
    conn=psycopg2.connect(dbname="disbot_db",user="postgres",host="localhost",port="5432",password="IAmAwesome")
    cur=conn.cursor()
    
    query='select CONFIDENCE_RATING from Students where DISCORD_USER_ID = %s'
    cur.execute(query, (user_id,))
    res=cur.fetchone()
    
    #To continue appending the log file if it already exists; otherwise it creates the log file
    if(isFilePresent):
        file=open('log.txt','a')
    else:
        file=open('log.txt','w')
        
    if res is None:
        #This means the user is not present in the database 
        print('User not present in the database')
    else:
        file.write(str(datetime.now())+':Going to alter the confidence rating of this user by '+str(change_in_rating))
        newRating=int(res[0])+change_in_rating
        
        sql='UPDATE Students set CONFIDENCE_RATING=%s where DISCORD_USER_ID = %s'
        cur.execute(sql, (str(newRating),str(user_id)))
        conn.commit()
    
    cur.close()
    conn.close()
    file.close()

@client.event
async def on_ready():
    print('Bot ready:', client.user)
        
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    #To continue appending the log file if it already exists; otherwise it creates the log file
    if(isFilePresent):
        file=open('log.txt','a')
    else:
        file=open('log.txt','w')
    
    file.write(str(datetime.now())+':The user '+str(message.author.name)+' has sent a message.\n')
    if message.content.lower().startswith('hello') and len(message.content)<15:
        file.write('Message sent :'+str(message.content)+' in the channel '+str(message.channel)+'.\n')
        conn=psycopg2.connect(dbname="disbot_db",user="postgres",host="localhost",port="5432",password="IAmAwesome")
        cur=conn.cursor()
        
        authorInfo='select STUDENT_NO from Students where DISCORD_USER_ID='+str(message.author.id)
        cur.execute(authorInfo)
        res=cur.fetchone()
        student_no=None
        
        if res is None:
            #Checking if it is a staff member
            staffQuery='select STAFF_ID from InstituteStaff where DISCORD_USER_ID='+str(message.author.id)
            cur.execute(authorInfo)
            staffRow=cur.fetchone()

            if staffRow is not None:
                #This means that the author is a staff member.
                print('This guy is a staff member.')
                cur.close()
                conn.close()
                file.close()
                return
            #This means that the user is not present in the database. So we need to add this user
            lock=threading.Lock()
            lock.acquire()
            sql='select max(STUDENT_NO) from Students'
            cur.execute(sql)
            row=cur.fetchone()
           
            maxVal=None 
            if row[0] is None:
                maxVal=0
            else:
                maxVal=int(row[0])
            
            student_no=maxVal+1
            
            sql='INSERT INTO Students values (%s,%s,%s,%s,%s)'
            addStudentsToCloud(str(student_no),str(message.author.id),str(message.author.name),'5','15')
            cur.execute(sql,(str(student_no),str(message.author.id),str(message.author.name),'5','15'))
            conn.commit()
            lock.release()
        cur.close()
        conn.close()
        msg="Hi "+ str(message.author.name)
        await message.channel.send(msg)
        file.write('Replied saying: '+msg+'\n')
    elif str(message.channel.type)=='text' and not message.author.bot:   
        if message.content.startswith('!'):
            #This is a command
            if message.content.find('!staff')!=-1:
                if not message.author.guild_permissions.administrator:
                    if message.channel is not None:
                        await message.channel.send('Hi '+str(message.author.mention)+'. Only administrators can be treated as staff members.')
                else:                    
                    if len(message.content.strip())==6:
                        lock_staff=threading.Lock()
                        lock_staff.acquire()
                        addStaffDetails(message.author, None)
                        lock_staff.release()
                        return
                        
                    mailId=message.content[message.content.index('!staff')+7:len(message.content)]
                    mailId=mailId.strip()
                    
                    if len(mailId)>2 and mailId[0]=='|' and mailId[1]=='|':
                        #The message was sent as a hidden text
                        mailId=mailId[2:len(mailId)-2]
                    
                    mailId=mailId.strip()
                    
                    if not validateMailId(mailId):
                        if message.channel is not None:
                            await message.channel.send('Hi '+str(message.author.mention)+'. You have entered an invalid email ID. Please re-enter the command with the correct mail ID.')
                    else:
                        lock_staff=threading.Lock()
                        lock_staff.acquire()
                        addStaffDetails(message.author, mailId)
                        lock_staff.release()
                file.close()
                return
            elif message.content.find('!add_unconventional_topic')!=-1:
                if not message.author.guild_permissions.administrator:
                    if message.channel is not None:
                        await message.channel.send('Hi '+str(message.author.mention)+'. Only administrators are allowed to add unconventional academic topics.')
                else:
                    if len(message.content.strip())==25:
                        if message.channel is not None:
                            await message.channel.send('Hi '+str(message.author.mention)+'. You haven\'t mentioned any topic.')
                        return 
                        
                    topic_name=message.content[message.content.index('!add_unconventional_topic')+26:len(message.content)]

                    if not validateTopicName(topic_name):
                        if message.channel is not None:
                            await message.channel.send('Hi '+str(message.author.mention)+'. You have entered an invalid topic.')
                    else:
                        lock1=threading.Lock()
                        lock1.acquire()
                        retValue=addUnconventionalTopic(topic_name, message)
                        lock1.release()
                        
                        if retValue is not None and retValue=='existing':
                            if message.channel is not None:
                                await message.channel.send(str(message.author.mention)+" This topic already exists in the list of unconventional academic topics.")
                        else:
                            if message.channel is not None:
                                await message.channel.send(str(message.author.mention)+" The topic "+topic_name+" has been added to the list of unconventional academic topics.")
                        
                file.close()
                return
                    
        words=nltk.word_tokenize(message.content)
    
        p=re.compile('^[-''&a-zA-Z0-9]+$')
        
        conn=psycopg2.connect(dbname="disbot_db",user="postgres",host="localhost",port="5432",password="IAmAwesome")
        cur=conn.cursor()
        
        authorInfo='select STUDENT_NO from Students where DISCORD_USER_ID='+str(message.author.id)
        cur.execute(authorInfo)
        res=cur.fetchone()
        student_no=None
        
        if res is None:
            #Checking if it is a staff member
            staffQuery='select STAFF_ID from InstituteStaff where DISCORD_USER_ID='+str(message.author.id)
            cur.execute(authorInfo)
            staffRow=cur.fetchone()

            if staffRow is not None:
                #This means that the author is a staff member.
                print('This guy is a staff member.')
                cur.close()
                conn.close()
                file.close()
                return
            #This means that the user is not present in the database. So we need to add this user
            lock=threading.Lock()
            lock.acquire()
            sql='select max(STUDENT_NO) from Students'
            cur.execute(sql)
            row=cur.fetchone()
           
            maxVal=None 
            if row[0] is None:
                maxVal=0
            else:
                maxVal=int(row[0])
            
            student_no=maxVal+1
            
            sql='INSERT INTO Students values (%s,%s,%s,%s,%s)'
            addStudentsToCloud(str(student_no),str(message.author.id),str(message.author.name),'5','15')
            cur.execute(sql,(str(student_no),str(message.author.id),str(message.author.name),'5','15'))
            conn.commit()
            lock.release()
        else:
            student_no=int(res[0])
        
        cur.execute('select TOPIC_NAME from NonConventionalAcademicTopics')
        topics=cur.fetchall()
        additionalIgnorableWords=['-','&',"'",'hello','guys','get','hi','help','find','see']
        
        #This list would contain all the unconventional academic topics declared so far
        un_topics=[]
        
        for un_top in topics:
            un_topics.append(str(un_top[0]))
                     
        for word in words:
            #If the word is in English
            if p.match(word):
                if word in abc.words() or word.lower() in abc.words() or word.capitalize() in abc.words() or word in un_topics:                    
                    word_type=wordnet.synsets(word)[0].pos() if len(wordnet.synsets(word))>0 else None
                    file.write('Word detected='+word+', its word type is '+(word_type if word_type is not None else 'None')+'. ')
                    
                    if word not in un_topics and (word.lower() in stopwords.words('english') or len(word)==1 or word_type in [None,'v','a','r','s'] or word.lower() in additionalIgnorableWords):
                        continue
                    
                    topic_no=addOrUpdateTopics(word.lower(), conn)
                    
                    cur.execute('select max(ENTRY_NO) from StudentTexts')
                    result=cur.fetchone()
                    
                    entry_no=None
                    lock2=threading.Lock()
                    lock2.acquire()
                    if result[0] is None:
                        entry_no=1
                    else:
                        entry_no=int(result[0])+1
                        
                    sql='INSERT INTO StudentTexts VALUES (%s,%s,%s,%s,%s,%s,%s,%s,now())'
                    cur.execute(sql, (str(entry_no), str(student_no), str(message.guild.name), str(message.channel.name), str(message.guild.id), str(topic_no), word.lower(), str(message.id)))
                    conn.commit()
                    lock2.release()
                    
        file.write('\n')
        cur.close()
        conn.close()
    
    file.close()

@client.event
async def on_message_delete(message):
    if message.author == client.user or message.author.bot:
        return 
        
    #To continue appending the log file if it already exists; otherwise it creates the log file
    if(isFilePresent):
        file=open('log.txt','a')
    else:
        file=open('log.txt','w')
        
    file.write(str(datetime.now())+':The user '+str(message.author.name)+' has deleted a message. ')
    
    if str(message.channel.type)=='text':
        words=nltk.word_tokenize(message.content)
    
        p=re.compile('^[-''&a-zA-Z0-9]+$')
        
        conn=psycopg2.connect(dbname="disbot_db",user="postgres",host="localhost",port="5432",password="IAmAwesome")
        cur=conn.cursor()
        
        authorInfo='select STUDENT_NO from Students where DISCORD_USER_ID='+str(message.author.id)
        cur.execute(authorInfo)
        res=cur.fetchone()
        student_no=None
                
        if res is None:
            #This means that the user itself is not present in the database. So we can terminate this process
            return
        else:
            student_no=int(res[0])
        
        deleteMsg(message, student_no, conn)

        file.write('The entries corresponding to this message have also been deleted.\n')
        file.write('\n')
        cur.close()
        conn.close()
    file.close()

@client.event
async def on_bulk_message_delete(messages):
    conn=psycopg2.connect(dbname="disbot_db",user="postgres",host="localhost",port="5432",password="IAmAwesome")
        
    for msg in messages:
        deleteMsg(msg, None, conn)
    
    conn.close()

@client.event
async def on_member_ban(guild, user):
    conn=psycopg2.connect(dbname="disbot_db",user="postgres",host="localhost",port="5432",password="IAmAwesome")
    cur=conn.cursor()
    
    sql='select STUDENT_NO from Students where DISCORD_USER_ID='+str(user.id)
    cur.execute(sql)
    row=cur.fetchone()
    
    if row is not None: #If the student is present in the database
        student_no=row[0]
        
        sql='select STUDENT_NO from BlockedStudents where GUILD_ID='+str(guild.id)+' and STUDENT_NO='+str(student_no)
        cur.execute(sql)
        row=cur.fetchone()
        
        if row is not None: #This combination already exists in the database. This scenario would occur if there was some downtime in the disbot application.
            return
        
        sql='insert into BlockedStudents values (%s,%s)'
        cur.execute(sql, (str(student_no), str(guild.id)))
        conn.commit()
        
    cur.close()
    conn.close()    
    
@client.event
async def on_member_unban(guild, user):
    conn=psycopg2.connect(dbname="disbot_db",user="postgres",host="localhost",port="5432",password="IAmAwesome")
    cur=conn.cursor()
    
    sql='select STUDENT_NO from Students where DISCORD_USER_ID='+str(user.id)
    cur.execute(sql)
    row=cur.fetchone()
    
    if row is not None: #If the student is present in the database
        student_no=row[0]
        sql='DELETE FROM BlockedStudents WHERE STUDENT_NO = %s AND GUILD_ID = %s'
        cur.execute(sql, (str(student_no), str(guild.id)))
        conn.commit()
        
    cur.close()
    conn.close()  

@client.event
async def on_member_join(member):
    if member.guild_permissions.administrator:
        #To continue appending the log file if it already exists; otherwise it creates the log file
        if(isFilePresent):
            file=open('log.txt','a')
        else:
            file=open('log.txt','w')
        
        channelsList=member.guild.channels
        
        for channel in channelsList:        
            if channel.name=='general':
                msg="Hi "+str(member.name)+". Could you please tell us whether you are a staff member. If yes, please enter the command **!staff** followed by your email address and if not, please ignore this message. If you do not wish to share your mail ID, just enter **!staff**. If you want to share the mail ID without it being visible to the remaining members of the group, please enclose it within this symbol: ||"
                await channel.send(msg)
                file.write(str(datetime.now())+':A message was sent to the user '+str(member.name)+' asking whether he/she is a staff member.')
        
        file.close()

@client.event
async def on_member_update(before, after):
    if (not before.guild_permissions.administrator) and after.guild_permissions.administrator:
        #To continue appending the log file if it already exists; otherwise it creates the log file
        if(isFilePresent):
            file=open('log.txt','a')
        else:
            file=open('log.txt','w')
        
        channelsList=after.guild.channels
        
        for channel in channelsList:        
            if channel.name=='general':
                msg="Hi "+str(after.name)+". Could you please tell us whether you are a staff member. If yes, please enter the command **!staff** followed by your email address and if not, please ignore this message. If you do not wish to share your mail ID, just enter **!staff**. If you want to share the mail ID without it being visible to the remaining members of the group, please enclose it within this symbol: ||"
                await channel.send(msg)
                file.write(str(datetime.now())+':A message was sent to the user '+str(after.name)+' asking whether he/she is a staff member.\n')
        
        file.close()

@client.event
async def on_guild_join(guild):
    admins=[]
    for member in guild.members:
        if member.guild_permissions.administrator:
            admins.append(member.name)
            
    adminStr=''
    for adm in range(len(admins)):
        if client.user.name==str(admins[adm]):
            continue
        if adm==len(admins)-1:
            adminStr+=' and '+admins[adm]
        elif adm==0:
            adminStr+=str(admins[adm])
        else:
            adminStr+=', '+str(admins[adm])

    channelsList=guild.channels
        
    for channel in channelsList:        
        if channel.name=='general':
            msg="Hi "+adminStr+". Could you all please tell us whether you are staff members. If yes, please enter the command **!staff** followed by your email address and if not, please ignore this message. If you do not wish to share your mail ID, just enter **!staff**. If you want to share the mail ID without it being visible to the remaining members of the group, please enclose it within this symbol: ||"
            await channel.send(msg)

def validateTopicName(topic_name):
    if topic_name.find('<')!=-1 or topic_name.find('>')!=-1:
         return False
    return True

def addUnconventionalTopic(topic_name, msg):
    conn=psycopg2.connect(dbname="disbot_db",user="postgres",host="localhost",port="5432",password="IAmAwesome")
    cur=conn.cursor()

    if(isFilePresent):
        file=open('log.txt','a')
    else:
        file=open('log.txt','w')
    
    query="select max(TOPIC_NO) from NonConventionalAcademicTopics where TOPIC_NAME='"+ topic_name +"'"
    cur.execute(query)
    row=cur.fetchone()
    
    if row[0] is not None:
        file.write("The topic "+topic_name+" has already been added to the list of unconventional topics.\n")            
        return 'existing'
        
    cur.execute('select max(TOPIC_NO) from NonConventionalAcademicTopics')
    row=cur.fetchone()
    
    val=None
            
    if row[0] is None:
        val=1
    else:
        val=int(row[0])+1
    
    file.write(str(datetime.now())+':Added the topic '+topic_name+' to the database.\n')
    sql='INSERT INTO NonConventionalAcademicTopics values (%s,%s)'
    cur.execute(sql, (str(val), topic_name))
    conn.commit()
    cur.close()
    conn.close()
    file.close()

def addStaffDetails(user, mailId):
    conn=psycopg2.connect(dbname="disbot_db",user="postgres",host="localhost",port="5432",password="IAmAwesome")
    cur=conn.cursor()
    
    cur.execute('select STAFF_ID from InstituteStaff where DISCORD_USER_ID='+str(user.id))
    res=cur.fetchone()
    
    if(isFilePresent):
        file=open('log.txt','a')
    else:
        file=open('log.txt','w')
        
    if res is not None:
        file.write(str(datetime.now())+':This staff member is already present in the database.\n')
        file.close()
        return
       
    cur.execute('select STUDENT_NO from Students where DISCORD_USER_ID='+str(user.id))
    res=cur.fetchone()    
    
    if res is not None:
        #This implies that this user is currently treated as a student
        stud_no=int(res[0])
        sql='select TOPIC_NO from StudentTexts where STUDENT_NO='+str(stud_no)
        cur.execute(sql)
        rows=cur.fetchall()
        topics={}
        
        for row in rows:
            count=0
            if int(row[0]) in topics.keys():
                count=topics.get(int(row[0]))
                
            topics.update({int(row[0]):(count+1)})
        
        if len(topics)>0:
            sql='select TOPIC_NO, DISCUSSION_COUNT from keytopics where TOPIC_NO in ('
            
            ind=0
            for k,v in topics.items():
                if ind==len(topics)-1:
                    sql+=str(k)+')'
                else:
                    sql+=str(k)+','
                ind+=1
                
            cur.execute(sql)
            data=cur.fetchall()
            
            for d in data:
                top=int(d[0])
                count=int(d[1])
                
                sql='update keytopics set DISCUSSION_COUNT=%s where TOPIC_NO=%s'
                updateKeytopicOnCloud('UPDATE Keytopics set DISCUSSION_COUNT='+str(top)+' where TOPIC_NO='+str(count-topics.get(top)))
                cur.execute(sql,(str(top),str(count-topics.get(top))))
                conn.commit()
        
        sql='delete from Students where STUDENT_NO='+str(stud_no)
        deleteStudentsFromCloud(str(stud_no))
        cur.execute(sql)
        conn.commit()
     
    cur.execute('select max(STAFF_ID) from InstituteStaff')
    row=cur.fetchone()
    
    val=None
            
    if row[0] is None:
        val=1
    else:
        val=int(row[0])+1
    
    file.write(str(datetime.now())+':Added the staff member '+str(user.name)+' to the database.\n')
    sql='INSERT INTO InstituteStaff values (%s,%s,%s,%s,true,null)'
    cur.execute(sql, (str(val), str(user.name), str(user.id), mailId))
    addStaffToCloud(val,mailId)
    conn.commit()
    cur.close()
    conn.close()
    file.close()

def updateKeytopicOnCloud(sql):
    try:
        conn1=psycopg2.connect(host="SG-disbotswinpostgres-1986-pgsql-master.servers.mongodirector.com", user="postgres", password="Swin1234@2021", dbname="disbot_db", port="6432", sslmode="verify-ca", sslrootcert="D:\\Study Materials\\Python\\Project\\ca.pem")
        cur1=conn1.cursor()
        
        cur1.execute(sql)
        conn1.commit()
        cur1.close()
        conn1.close()
    except:
        print('Error occured while adding data to the cloud.')  

def deleteStudentsFromCloud(stud_no):
    try:
        conn1=psycopg2.connect(host="SG-disbotswinpostgres-1986-pgsql-master.servers.mongodirector.com", user="postgres", password="Swin1234@2021", dbname="disbot_db", port="6432", sslmode="verify-ca", sslrootcert="D:\\Study Materials\\Python\\Project\\ca.pem")
        cur1=conn1.cursor()
        
        sql='delete from Students where STUDENT_NO='+stud_no
        cur1.execute(sql)
        conn1.commit()
        cur1.close()
        conn1.close()
    except:
        print('Error occured while adding data to the cloud.')  
    
def addStudentsToCloud(p1,p2,p3,p4,p5):
    try:
        conn1=psycopg2.connect(host="SG-disbotswinpostgres-1986-pgsql-master.servers.mongodirector.com", user="postgres", password="Swin1234@2021", dbname="disbot_db", port="6432", sslmode="verify-ca", sslrootcert="D:\\Study Materials\\Python\\Project\\ca.pem")
        cur1=conn1.cursor()
        
        sql='INSERT INTO Students values (%s,%s,%s,%s,%s)'
        cur1.execute(sql, (p1,p2,p3,p4,p5))
        conn1.commit()
        cur1.close()
        conn1.close()
    except:
        print('Error occured while adding data to the cloud.')

def addKeyTopicToCloud(p1,p2,p3,p4):
    try:
        conn=psycopg2.connect(host="SG-disbotswinpostgres-1986-pgsql-master.servers.mongodirector.com", user="postgres", password="Swin1234@2021", dbname="disbot_db", port="6432", sslmode="verify-ca", sslrootcert="D:\\Study Materials\\Python\\Project\\ca.pem")
        cur=conn.cursor()
        
        sql='INSERT INTO Keytopics values (%s,%s,%s,now(),%s)'
        cur.execute(sql, (p1,p2,p3,p4))
        conn.commit()
        cur.close()
        conn.close()
    except:
        print('Error occured while adding data to the cloud.')
        
def addStaffToCloud(val,mailId):
    try:
        conn=psycopg2.connect(host="SG-disbotswinpostgres-1986-pgsql-master.servers.mongodirector.com", user="postgres", password="Swin1234@2021", dbname="disbot_db", port="6432", sslmode="verify-ca", sslrootcert="D:\\Study Materials\\Python\\Project\\ca.pem")
        cur=conn.cursor()
        
        sql='INSERT INTO InstituteStaff values (%s,\'-\',\'111\',%s,true,null)'
        cur.execute(sql, (str(val),mailId))
        conn.commit()
        cur.close()
        conn.close()
    except:
        print('Error occured while adding data to the cloud.')

def validateMailId(mailId):
    if mailId.find('@')!=-1 and mailId.find('.')!=-1 and re.match('^[-_@+.a-zA-Z0-9]+$',mailId):
        return True
    return False        

#This method will delete the entries corresponding to the deleted message
def deleteMsg(message, student_no, conn):
    cur=conn.cursor()
    if student_no is not None:
        cur.execute('select TOPIC_NO from StudentTexts where STUDENT_NO=%s and MESSAGE_ID=%s', (str(student_no), str(message.id)))
    else:
        query='select TOPIC_NO from StudentTexts where MESSAGE_ID='+str(message.id)
        cur.execute(query)
    result=cur.fetchall() 
    
    if len(result)==0: #This implies that it has been invoked when a user was banned.
        return
    
    sql='select TOPIC_NO, DISCUSSION_COUNT from Keytopics where TOPIC_NO in ('
    ind=True
    
    for res in result:
        if ind:
            sql+=str(res[0])
            ind=False
        else:
            sql+=','+str(res[0])
            
    sql+=')'
    
    cur.execute(sql)
    res=cur.fetchall()
    
    for row in res:
        t_no=str(row[0])
        count=int(row[1])-1
        
        query='update Keytopics set DISCUSSION_COUNT = %s where TOPIC_NO = %s'  
        updateKeytopicOnCloud('UPDATE Keytopics set DISCUSSION_COUNT='+str(count)+' where TOPIC_NO='+t_no)
        cur.execute(query, (str(count), t_no))
        conn.commit()
    
    if student_no is not None:
        sql='delete from StudentTexts where STUDENT_NO = %s and MESSAGE_ID = %s'
        cur.execute(sql, (str(student_no), str(message.id)))
    else:
        sql='delete from StudentTexts where MESSAGE_ID = '+str(message.id)
        cur.execute(sql)
    
    conn.commit()
            
    cur.close()
    
if __name__=='__main__':
    #Checking if the log file is already created or not
    if path.exists('log.txt'):
        isFilePresent=True 
        
    checkAndCreateDB()
    client.run("BOT_TOKEN")
