# datafile: contact details/data
# ext: extension of the attachment
# fromadd: sendeer's email add.
  #importing modules
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import psycopg2
import time

#datafile = "D:\Study\Technology Enquiry Project\Disbot\emailID.txt" #path of contacts file

fromadd =  "group2.disbot@gmail.com"

while True:
    time.sleep(5) #pause for 30 seconds
    
    conn=psycopg2.connect(host="SG-disbotswinpostgres-1986-pgsql-master.servers.mongodirector.com", user="postgres", password="Swin1234@2021", dbname="disbot_db", port="6432", sslmode="verify-ca",sslrootcert="D:\\Study Materials\\Python\\Project\\ca.pem")
    cur=conn.cursor()
    mailIds=''
    sql='select MAIL_ID from InstituteStaff'
    cur.execute(sql)
    res=cur.fetchall()
    
    if res is not None:
        for row in res:
            mailIds+=str(row[0])+' '    
    
    toaddress=mailIds
    cur.close()
    conn.close()
    
    if toaddress is not None and toaddress!='':        
        # Preparing the Email Temp.
        
        msg = MIMEMultipart()   # for multiparting the object
        msg['FROM'] = fromadd
        msg['TO'] = toaddress
        msg['SUBJECT'] ="Disbot test email"
        body = "Hi,\n\nThis email has been sent to notify you that an update is available in the Disbot visualization. In order to view it please click the following link: https://mercury.swin.edu.au/cos60004/s103167568/disbot/main.php \n\nRegards\nDisbot application"
        msg.attach(MIMEText(body,'plain'))

       # Establishing SMTP
        
        s=smtplib.SMTP('smtp.gmail.com', 587)   #for Gmail
        s.ehlo()
        s.starttls()
        s.login(fromadd,'Me.disbot2021')
        text=msg.as_string()
        s.sendmail(fromadd,toaddress,text)
        s.quit()
        print("Email sent!")
        time.sleep(30) #pause for 30 seconds
