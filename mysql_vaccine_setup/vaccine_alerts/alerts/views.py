from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import json
import time
import threading
import alerts
from alerts import check_notif
import os
import requests
import mysql.connector
from mysql.connector import Error

# Create your views here.
def index(request):
    is_thread_active=False
    print('Main thread''s PID is ', os.getpid())
    print('main thread name in add_new is ',threading.current_thread().getName())
    for t in threading.enumerate():
        if t.getName()=='mail_notifications_thread_rishabh':
            is_thread_active=True
            break
    if not is_thread_active:
        print('Going to trigger the notification thread...')
        lock=threading.Lock()
        t1=threading.Thread(target=check_notif.check_for_updates, args=(lock,), name='mail_notifications_thread_rishabh')
        t1.start()   
        
    print('Main thread''s PID is ', os.getpid())
    template=loader.get_template('alerts/index.html')    
    context={'initial_selection':'yes'}
    return HttpResponse(template.render(context, request))

def get_states_details(states):
    hdr={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36','accept':'application/json, text/plain, */*'}
    webUrl=requests.get(url="https://cdn-api.co-vin.in/api/v2/admin/location/states", headers=hdr, verify=False)
    if webUrl.status_code != 200:
        return HttpResponse("There was an internal error while fetching the states' details. The server might be down. Please try again after sometime.")
    else:
        data=webUrl.json()
        for i in data['states']:
            states.append([i['state_id'],i['state_name']])
    

def add_information(request):
    obj=request.POST
    template=loader.get_template('alerts/index.html')
    context={}
    print('Main thread''s PID is ', os.getpid())
    print('main thread name in add_new is ',threading.current_thread().getName())
    for k,v in obj.items():
        if k=='selection_method':   
            if v=='state':
                states=[]
                get_states_details(states)
                context={'states':states}  
            elif v=='pin':
                context={'pincode':'yes'}
        elif k=='states' and (obj.get('district') is None or obj.get('district')=='no_district_selected'):
            print("Fetching the districts!")
            districts=[]
            hdr={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36','accept':'application/json, text/plain, */*'}
            webUrl=requests.get(url="https://cdn-api.co-vin.in/api/v2/admin/location/districts/"+str(v.split(',')[0]), verify=False, headers=hdr)
            if webUrl.status_code != 200:
                return HttpResponse("There was an internal error while fetching the districts' details. The server might be down. Please try again after sometime.")
            else:
                data=webUrl.json()
                for j in data['districts']:
                    districts.append([j['district_id'],j['district_name']])
                states=[]
                get_states_details(states)
                context={'districts':districts, 'state_name': str(v.split(',')[1]), 'state_id':str(v.split(',')[0]), 'states':states}
        elif k=='district' and v!="no_district_selected":
            context={'mail_id':'yes','district_name':str(v.split(',')[1]), 'district_id':int(v.split(',')[0]), 'state_name': str(obj.get('states')).split(',')[1]}
        elif k=='pincode' and obj.get('otp') is None:
            context={'mail_id':'yes','pincode': str(v)}
        elif k=='mail' and obj.get('otp') is None:
            template=loader.get_template('alerts/results.html')
            minusOne=-1
            if obj.get('district') is not None:
                context={'mail':v, 'district_id':int(str(obj.get('district')).split(',')[0]), 'pincode':minusOne}
            else:   
                context={'mail':v, 'district_id':minusOne, 'pincode':int(obj.get('pincode'))}
            
            ip_add=get_ip_address(request)
            lock=threading.Lock()
            val=check_notif.sendOTP(str(v), ip_add, lock)
            
            if not val:
                template=loader.get_template('alerts/index.html')    
                context={'initial_selection':'yes', 'mail_sending_failed':'yes'}
                return HttpResponse(template.render(context, request))
        elif k=='otp':
            distId,pin=-1,-1
            ip_add=get_ip_address(request)
            
            conn=mysql.connector.connect(host='localhost',user='root',database='location_database',password='IAmAwesome',connection_timeout=150)
            cur=conn.cursor()
            
            sql='select max(OTP) from UnverifiedPeople where TO_ADDRESS = %s and FROM_IP = %s'
            cur.execute(sql, (str(obj.get('mail')),ip_add))
            row=cur.fetchone()
            
            if row[0] is None:
                template=loader.get_template('alerts/index.html')    
                context={'initial_selection':'yes', 'verification_failed':'yes'}
                return HttpResponse(template.render(context, request))        
            else:
                val=int(row[0])
                if val==int(v):
                    template=loader.get_template('alerts/index.html')    
                    context={'initial_selection':'yes', 'data_added':'yes'}
                    sql='delete from UnverifiedPeople where TO_ADDRESS = %s and FROM_IP = %s'
                    cur.execute(sql, (str(obj.get('mail')),ip_add))
                    conn.commit()
                else:
                    template=loader.get_template('alerts/index.html')    
                    context={'initial_selection':'yes', 'verification_failed':'yes'}
                    return HttpResponse(template.render(context, request))        
            if obj.get('district_id') is not None:
                try:
                    distId=int(obj.get('district_id'))
                except:
                    template=loader.get_template('alerts/index.html')    
                    context={'initial_selection':'yes'}
                    return HttpResponse(template.render(context, request))                 
            if obj.get('pincode') is not None:
                try:
                    pin=int(obj.get('pincode'))
                except:
                    template=loader.get_template('alerts/index.html')    
                    context={'initial_selection':'yes'}
                    return HttpResponse(template.render(context, request))
                       
            mail_add=str(obj.get('mail'))
            
            if mail_add.find('<')!=-1 or mail_add.find('>')!=-1:
                template=loader.get_template('alerts/index.html')    
                context={'initial_selection':'yes'}
                return HttpResponse(template.render(context, request))
            
            lock=threading.Lock()
            lock.acquire()
            update_db(distId,pin,mail_add,ip_add)
            lock.release()
            template=loader.get_template('alerts/index.html')    
            context={'initial_selection':'yes', 'data_added':'yes'}
            print(context)
            cur.close()
            conn.close()

    return HttpResponse(template.render(context, request))
    
def get_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip=''
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
    
def update_db(distId, pin, mailId, ip_add):
    conn=mysql.connector.connect(host='localhost',user='root',database='location_database',password='IAmAwesome',connection_timeout=150)
    cur=conn.cursor()
    
    if distId==-1:
        sql='select ID, DISTRICT_ID, PINCODE from Location where PINCODE='+str(pin)
    else:
        sql='select ID, DISTRICT_ID, PINCODE from Location where DISTRICT_ID='+str(distId)
            
    cur.execute(sql) 
    
    result=cur.fetchone()
    
    loc_id=None
    
    if result is not None:
        #Location details already exist
        loc_id=str(result[0])
    else:
        #Location needs to be added
        query='select max(ID) from Location'
        cur.execute(query)
        row=cur.fetchone()
        if row[0] is None:
            max_id=0
        else:
            max_id=int(row[0])        
        query='insert into Location values (%s,%s,%s)'
        loc_id=str(max_id+1)
        cur.execute(query, (loc_id, str(distId), str(pin)))
        conn.commit()
    
    sql='select max(ID) from People'
    cur.execute(sql)
    result=cur.fetchone()
    
    peopleId=None
    if result[0] is None:
        peopleId=0
    else:
        peopleId=int(result[0])
    
    sql='insert into People values (%s,%s,%s,%s)'
    cur.execute(sql, (str(peopleId+1),str(mailId),str(ip_add), loc_id))
    conn.commit()
    cur.close()
    conn.close()
           
    