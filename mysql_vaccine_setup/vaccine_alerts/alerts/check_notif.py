"""
WSGI config for vaccine_alerts project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import threading
import alerts
from alerts import models
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime
from datetime import date
import time
import requests
import random
import mysql.connector
from mysql.connector import Error

def sendOTP(mailId, ip_add, lock):
    fromAdd='updates@getvaccineslots.in'
    rand_num=random.randint(10000,99999)
    print('Gonna send OTP')
    try:
        body="<html><p>Your OTP to verify your mail ID is given below:<br><br>"+str(rand_num)+"<br><br>In case you didn't request for this OTP, please ignore this mail.</p><br>"
        body+="<p style=\"font-size:11px;\">Note: This is an automated e-mail, so please do not reply to it. You will start receiving notifications regarding vaccination slots' availability for the age group 18-45 only after verifying your account. For more details, visit http://www.getvaccineslots.in</p></html>"
        msg = MIMEMultipart()
        msg['FROM'] = fromAdd 
        msg['TO'] = mailId
        msg['SUBJECT'] ="Vaccine slots verification mail"   
        msg.attach(MIMEText(body,'html'))  
        print('Fetching SMTP')
        s=smtplib.SMTP('smtpout.secureserver.net', 80)   #for godaddy 
        print('SMTP fetched')
        s.ehlo() 
        s.starttls()
        s.login(fromAdd,'DSKBenelli1995') 
        text=msg.as_string() 
        s.sendmail(fromAdd,mailId,text) 
        s.quit() 
        print('Mail sent successfully.')
    except:
        print('Error occurred while sending the mail')
        return False
        
    lock.acquire()
    addUnverifiedPeople(rand_num, mailId, ip_add)
    lock.release()
    
    return True

def addUnverifiedPeople(rand_num, mailId, ip_add):
    conn=mysql.connector.connect(host='localhost',user='root',database='location_database',password='IAmAwesome',connection_timeout=150)
    cur=conn.cursor()
    
    sql='select max(ID) from UnverifiedPeople'
    cur.execute(sql)
    row=cur.fetchone()
    if row[0] is None:
        mv=0
    else:
        mv=int(row[0])
    
    mv+=1
    
    sql='insert into UnverifiedPeople values (%s,%s,%s,%s,now())'
    cur.execute(sql, (str(mv), mailId, ip_add, str(rand_num)))
    conn.commit()
    cur.close()
    conn.close()

def check_for_updates(lock):
    conn=mysql.connector.connect(host='localhost',user='root',database='location_database',password='IAmAwesome',connection_timeout=150)
    cur=conn.cursor()
    base=0
    
    while True:
        print('side thread name is ',threading.current_thread().getName())
        print('Side PID is ',os.getpid())
        dist_id, pins={},{}
        fromAdd='updates@getvaccineslots.in'
        
        sql='select TO_ADDRESS, DISTRICT_ID, PINCODE from People inner join Location on People.LOCATION_ID=Location.ID order by People.ID asc limit 20000 offset '+str(base)
        cur.execute(sql)
        rows=cur.fetchall()
        
        if cur.rowcount==0:
            base=0
        else:
            base+=int(cur.rowcount)
                
        for row in rows:
            if int(row[1])!=-1:
                dist_id.update({row[1]:row[0]})
            else:
                pins.update({row[2]:row[0]})
               
        for k,v in dist_id.items():
            ind=0
            center_info, fast_center_info=[], []
            is_notif_needed=False
            
            while ind<7:
                dateCrit=(date.today()+datetime.timedelta(days=ind)).strftime("%d-%m-%y")
                ind+=1
                #webUrl=urllib.request.urlopen("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id="+str(k)+"&date="+str(dateCrit))
                hdr={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36','accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
                webUrl=requests.get(url="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id="+str(k)+"&date="+str(dateCrit), headers=hdr, verify=False)
                centerDict, fastFilling=[],[]
                print('data: ',webUrl.status_code)
                if webUrl.status_code==200:
                    data=webUrl.json()
                    for x in data['centers']:
                        for y in x['sessions']:
                            if int(y['min_age_limit'])<45:
                                if int(y['available_capacity'])>20:
                                    centerDict.append({x['name']:x['pincode']})
                                elif int(y['available_capacity'])>0:
                                    fastFilling.append({x['name']:x['pincode']})
                                    
                    center_info.append([dateCrit,centerDict])
                    fast_center_info.append([dateCrit,fastFilling])
                else:
                    print('Something went wrong while querying the database.')
                        
            body=""
            
            for val in center_info:
                if len(val[1])>0:
                    is_notif_needed=True
                    body+="Slots are currently available on "+val[0]+" in the following centers:\n\n"
                    for item in val[1]:
                        for a,b in item.items():
                            body+='Name: '+a+', Pincode: '+b+'\n'
            body+='\n' 
            for val in fast_center_info:
                if len(val[1])>0:
                    is_notif_needed=True
                    body+="\nSlots are currently available on "+val[0]+" in the following centers. However they are filling up fast:\n\n"
                    for item in val[1]:
                        for a,b in item.items():
                            body+='Name: '+str(a)+', Pincode: '+str(b)+'\n'
                        
                      
            #Send the notification
            if is_notif_needed:
                try:
                    msg = MIMEMultipart()
                    msg['FROM'] = fromAdd 
                    msg['TO'] = str(v)
                    msg['SUBJECT'] ="Slots availability alert"   
                    msg.attach(MIMEText(body,'plain'))    
                    s=smtplib.SMTP('smtpout.secureserver.net', 465)   #for Gmail 
                    s.ehlo() 
                    s.starttls()
                    s.login(fromAdd,'DSKBenelli1995') 
                    text=msg.as_string() 
                    s.sendmail(fromAdd,str(v),text) 
                    s.quit() 
                    print('Mail sent successfully.')
                except:
                    print('Error occurred while sending the mail')
                    
        for k,v in pins.items():
            ind=0
            center_info,fast_center_info=[],[]
            is_notif_needed=False
            
            while ind<7:
                dateCrit=(date.today()+datetime.timedelta(days=ind)).strftime("%d-%m-%y")
                ind+=1
                hdr={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36','accept':'application/json, text/plain, */*'}
                #webUrl=urllib.request.urlopen("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode="+str(k)+"&date="+str(dateCrit))
                webUrl=requests.get(url="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode="+str(k)+"&date="+str(dateCrit), headers=hdr, verify=False)
                centerDict, fastFilling=[],[]
                
                
                if webUrl.status_code==200:
                    data=webUrl.json()
                    for x in data['centers']:
                        for y in x['sessions']:
                            if int(y['min_age_limit'])<45:
                                if int(y['available_capacity'])>20:
                                    centerDict.append({x['name']:x['pincode']})
                                elif int(y['available_capacity'])>0:
                                    fastFilling.append({x['name']:x['pincode']})
                                    
                    center_info.append([dateCrit,centerDict])
                    fast_center_info.append([dateCrit,fastFilling])
                else:
                    print('Something went wrong while querying the database.')
                        
            body="Hey there\n\n"
            
            for val in center_info:
                if len(val[1])>0:
                    is_notif_needed=True
                    body+="Slots are currently available on "+val[0]+" in the following centers:\n\n"
                    for item in val[1]:
                        for a,b in item.items():
                            body+='Name: '+a+', Pincode: '+b+'\n'
            body+='\n' 
            for val in fast_center_info:
                if len(val[1])>0:
                    is_notif_needed=True
                    body+="\nSlots are currently available on "+val[0]+" in the following centers. However they are filling up fast:\n\n"
                    for item in val[1]:
                        for a,b in item.items():
                            body+='Name: '+a+', Pincode: '+b+'\n'
                        
            body+='\nRegards\nRishabh K'
            
            #Send the notification
            if is_notif_needed:
                try:
                    msg = MIMEMultipart()
                    msg['FROM'] = fromAdd 
                    msg['TO'] = str(v)
                    msg['SUBJECT'] ="Slots availability alert"   
                    msg.attach(MIMEText(body,'plain'))    
                    s=smtplib.SMTP('smtpout.secureserver.net', 465)   #for Gmail 
                    s.ehlo() 
                    s.starttls()
                    s.login(fromAdd,'DSKBenelli1995') 
                    text=msg.as_string() 
                    s.sendmail(fromAdd,str(v),text) 
                    s.quit() 
                    print('Mail sent successfully.')
                except:
                    print('Error occurred while sending the mail')
        
        time.sleep(180)
    
    cur.close()
    conn.close()