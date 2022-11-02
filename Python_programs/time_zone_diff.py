# hackerrank problem

def calculate_diff(t1,t2):
    global mon_map
    global months
    mon_map={'Jan':31,'Mar':31,'Apr':30,'May':31,'Jun':30,'Jul':31,'Aug':31,'Sep':30,'Oct':31,'Nov':30,'Dec':31}
    months=('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')
    t1_list=get_list(t1)
    t2_list=get_list(t2)
    
    least_yr=get_least_base_year(t1_list,t2_list)
    t1_secs, t2_secs= calculate_secs(t1_list, int(least_yr)), calculate_secs(t2_list, int(least_yr))
    
    print(abs(int(t1_secs-t2_secs)))
    
def calculate_secs(t, least_yr):
    secs=0
        
    for p in range(least_yr,t[2]):
        if(is_leap_year(p)):
            secs+=366*24*60*60
        else:
            secs+=365*24*60*60
    
    i=0
    while i < months.index(t[1]):
        if mon_map.get(months[i]):
            secs+=mon_map.get(months[i])*24*60*60
        else:
            #February
            if is_leap_year(int(t[2])):
                secs+=29*24*60*60
            else:
                secs+=28*24*60*60
        i+=1
    secs+=(int(t[0])-1)*24*60*60

    secs+=int(t[3])*60*60

    secs+=int(t[4])*60

    secs+=int(t[5])
    return secs
    
def get_least_base_year(t1,t2):
    if t1[2]>t2[2]:
        return t2[2]
    elif t2[2]>t1[2]:
        return t1[2]
    else:
        return t1[2]
    
def get_list(t):
    l=t.split(' ')
    
    timezone=l[5]
    tm=l[4]
    
    symbol=timezone[0]
    hr=int(timezone[1:3])
    mi=int(timezone[3:5])
   
    timing=tm.split(':')
    
    hr2=int(timing[0]) #final hours
    min2=int(timing[1]) #final minutes
    sec=int(timing[2]) #final seconds
    
    if symbol == '+':
        mi=-mi
        hr=-hr
   
    min2+=mi   
    extrahr=0
    while min2>60:
        min2-=60
        extrahr+=1
    
    while min2<0:
        min2+=60
        extrahr-=1
    
    hr2+=hr
    extraday=0
    while hr2>24:
        hr2-=24
        extraday+=1
        
    while hr2<0:
        hr2+=24
        extraday-=1
        
    day, month, year=int(l[1]), l[2], int(l[3])
    if extraday!=0:
        day+=extraday
    
    extrayr=0    
    if month in mon_map.keys():
        if day>mon_map.get(month):
            if (months.index(month)+1)<12:
                month=months[(months.index(month)+1)]
            else:
                month=months[0]
                extrayr+=1
            day=1
        elif day<1:
            if (months.index(month)-1)>=0:
                month=months[(months.index(month)-1)]
            else:
                month=months[11]
                extrayr-=1
                
            if mon_map.get(month):
                day=mon_map.get(month)
            else: #this means it is February
                if is_leap_year(year):
                    day=29
                else:
                    day=28
    else:
        if day<1:
            if (months.index(month)-1)>=0:
                month=months[(months.index(month)-1)]
            else:
                month=months[11]
                extrayr-=1
                
            if mon_map.get(month):
                day=mon_map.get(month)
            else: #this means it is February
                if is_leap_year(year):
                    day=29
                else:
                    day=28
        else:
            if is_leap_year(year):
                if day>29:
                    if (months.index(month)+1)<12:
                        month=months[(months.index(month)+1)]
                    else:
                        month=months[0]
                        extrayr+=1
                    day=1
            else:
                if day>28:
                    if (months.index(month)+1)<12:
                        month=months[(months.index(month)+1)]
                    else:
                        month=months[0]
                        extrayr+=1
                    day=1
                    
    if extrayr != 0:
        year+=extrayr
    
    return [day,month,year,hr2,min2,sec] #final time in GMT
        
    
def is_leap_year(year):
    if(year%100==0 and year%400==0 or year%100!=0 and year%4==0):
        return True
    else:
        return False
    
if __name__=='__main__':
    n=int(input()) #test cases
    times=[]
    for i in range(n): 
        t1=input()
        t2=input()
        times.append([t1,t2])
    
    for k in times:
        calculate_diff(k[0],k[1])