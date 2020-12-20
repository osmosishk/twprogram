import requests
import json
import time
import random
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from apscheduler.schedulers.blocking import BlockingScheduler
import pymysql
import math
import logging
import os.path

config_arr = {}
encode = 'utf-8'
config_arr['mysql_host'] = ''
config_arr['mysql_user'] = ''
config_arr['mysql_pwd'] = ''
config_arr['mysql_db'] = ''
config_arr['log_path'] = ''

schedule_prase_file_hour=1
schedule_month_hour=2
schedule_day_hour=3
schedule_hour_hour=4
schedule_minute_hour=5

building_list=[]
meter_list=[]
#lock for countMinute()
lock_count_minute=0

#log info
def log():
    logger = logging.getLogger()
    now=datetime.now()
    nowstr=now.strftime("%Y%m%d")
    logname="schedule_log"+nowstr+".log"
    if os.path.isfile(logname)==False:
        f = open(logname,'a')
        f.close()
    fh = logging.FileHandler(logname)
    sh = logging.StreamHandler()
    fm = logging.Formatter('%(asctime)s-%(filename)s[line%(lineno)d]-%(levelname)s-%(message)s')
    fh.setFormatter(fm)
    sh.setFormatter(fm)
    logger.addHandler(fh)
    logger.addHandler(sh)
    logger.setLevel(logging.DEBUG)

    #logging.debug("調試訊息")
    #logging.info("一般訊息")
    #logging.warning("警告信息")
    #logging.error("錯誤訊息")
    #logging.critical("嚴重錯誤")

#Read local txt，get:raspberry mac、meter number
def getConfig():
    logging.info("開始讀取配置文件")
    #get mac address from txt
    global config_arr
    with open('./config.txt', encoding=encode, mode = 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if line.find('||')>=0:
                sp1 = line.split("||")[0]
                sp2 = line.split("||")[1]
                config_arr[sp1]=sp2
    logging.info("配置文件內容："+str(config_arr))

#get schedule time by api
def getParams():
    global schedule_prase_file_hour,schedule_month_hour,schedule_day_hour,schedule_hour_hour,schedule_minute_hour
    logging.info("開始獲取任務時間")
    sql = "SELECT paramName,paramValue FROM m_params where status=1"
    rs_all,ok = executesql(sql,'s')
    for rs in rs_all:
        try:
            if rs[0]=='schedule_prase_file_hour':
                schedule_prase_file_hour=int(rs[1])
            elif rs[0]=='schedule_process_month_hour':
                schedule_month_hour=int(rs[1])
            elif rs[0]=='schedule_process_day_hour':
                schedule_day_hour=int(rs[1])
            elif rs[0]=='schedule_process_hour_hour':
                schedule_hour_hour=int(rs[1])
            elif rs[0]=='schedule_process_minute_hour':
                schedule_minute_hour=int(rs[1])
        except:
            continue
    logging.info("任務時間獲取完成")

# clear meterdata datas for every month
def cleanMeterData():
    logging.info("開始清理MeterData數據")
    sql = "SELECT paramValue FROM m_params where paramName='schedule_clean_meter_data'"
    rs_all,ok = executesql(sql,'s')
    cleanNum=2
    try:
        cleanNum=int(rs[0])
    except:
        pass
    tm = datetime.now()+relativedelta(months=-cleanNum)
    sql = "delete from meter_datas where time<'%s'"%tm
    rs_all,ok = executesql(sql,'i')
    if ok=="ok":
        logging.info("清理MeterData數據操作成功！")
    else:
        logging.info("清理MeterData數據操作失敗！")
# process upload files into db
def praseFiles():
    logging.info("開始讀取資料庫中待處理文件")
    sql = "SELECT file,building_id,rasp_id,meter_id,record_date FROM m_upfiles where status=0 order by record_date"
    rs_all,ok = executesql(sql,'s')
    for rs in rs_all:
        pth=config_arr['log_path']+rs[0]
        bid=rs[1]
        rid=rs[2]
        mid=rs[3]
        logging.info("開始解析文件："+rs[0])
        if os.path.isfile(pth)==False:
            logging.error("文件不存在："+pth)
            continue
        with open(pth, encoding=encode, mode = 'r') as f:
            sql = "update m_upfiles set status=1 where file='%s'" % (rs[0])
            results,ok=executesql(sql,'i')
            for line in f.readlines():
                line = line.strip()
                data=line.split(';')
                try:
                    v1 = int(data[0])
                    v2 = int(data[1])
                    v3 = int(data[2])
                    l1 = int(data[3])
                    l2 = int(data[4])
                    l3 = int(data[5])
                    p1 = int(data[6])
                    p2 = int(data[7])
                    p3 = int(data[8])
                    kwh = int(data[9])
                    tm = rs[4]+' '+data[10]

                    #insert db
                    sql = "insert into meter_datas (time,v1,v2,v3,l1,l2,l3,pf1,pf2,pf3,kwh,building_id,rasp_id,meter_id,createTime) values('%s',%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,'%s')" % (tm, v1, v2, v3, l1, l2, l3, p1, p2, p3, kwh, bid,rid,mid, datetime.now())
                    results,ok=executesql(sql,'i')
                    if ok!='ok':
                        logging.debug('insert wrong!')
                    else:
                        #寫入總表
                        sql_all = "insert into meter_datas_all(time,v1,v2,v3,l1,l2,l3,pf1,pf2,pf3,kwh,building_id,rasp_id,meter_id,createTime) values('%s',%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,'%s')" % (tm, v1, v2, v3, l1, l2, l3, p1, p2, p3, kwh, bid,rid,mid, datetime.now())
                        executesql(sql_all,'i')
                except Exception as err:
                    logging.error(err)
                    continue
            sql = "update m_upfiles set status=2 where file='%s'" % (rs[0])
            results,ok=executesql(sql,'i')
        logging.info(rs[0]+"解析完成")
    logging.info("待處理文件處理完成")

    countMinute()

# get buildings list
def getBuildings():
    global building_list
    sql = "SELECT id FROM m_buildings"
    rs_all,ok = executesql(sql,'s')
    for rs in rs_all:
        building_list.append(rs[0])
    building_list.append(0)

# get meters list
def getMeters():
    global meter_list
    logging.info("開始獲取電錶……")
    sql = "SELECT id,name FROM m_meters"
    rs_all,ok = executesql(sql,'s')
    for rs in rs_all:
        meter_list.append(rs[0])
        logging.info("電錶："+rs[1])

# execute sql function
def executesql(sql,typ):
    try:
        db = pymysql.connect(config_arr['mysql_host'], config_arr['mysql_user'],
                     config_arr['mysql_pwd'], config_arr['mysql_db'], charset='utf8')
    except Exception as ee:
        print (ee,"Can't connect database")
        return None,'error'
    try:
        cursor = db.cursor()
        cursor.execute(sql)
        if typ=='i':
            results=db.commit()
        else:
            results = cursor.fetchall()
        return results,'ok'
    except Exception as r:
        print(r)
        return None,'error'
    finally:
        db.close()   

# get start time and end time to search data
def getTimeRange(table,bid):
    results = ""
    tm_first=None
    tm_last=None
    # get lastest count time
    sql = "SELECT dt FROM %s where building_id=%d order by id desc limit 1" %(table,bid)
    if bid==0:
        sql = "SELECT dt FROM %s order by id desc limit 1" %table
    datanum = 0
    results,ok = executesql(sql, 's')
    try:
        datanum = len(results)
    except:
        return None,0
    # no data,insert first data
    if datanum == 0:
        #print('no data')
        sql = "SELECT time FROM meter_datas where building_id=%d order by time asc limit 1" %(bid)
        if bid==0:
            sql = "SELECT time FROM meter_datas order by time asc limit 1"
        rs_all,ok = executesql(sql,'s')
        if len(rs_all)>0:
            tm_first = rs_all[0][0]
            datanum=len(rs_all)
    else:
        tm_first=results[0][0]
    try:
        tm_first=tm_first.strftime("%Y-%m-%d %H:%M:%S")
    except:
        pass
    #get tm_last
    if tm_first!=None:
        sql = "SELECT time FROM meter_datas where building_id=%d order by time desc limit 1" %(bid)
        if bid==0:
            sql = "SELECT time FROM meter_datas order by time desc limit 1"
        rs_all,ok = executesql(sql,'s')
        if len(rs_all)>0:
            tm_last = rs_all[0][0]
    return tm_first,tm_last,datanum

# get data use start time and end time,count data,insert data table
def insertCount(tm_start,tm_end,bid,table):
    sql = "SELECT * FROM meter_datas where building_id=%d and time>='%s' and time<'%s'" % (bid,tm_start,tm_end)
    if bid==0:
        sql = "SELECT * FROM meter_datas where time>='%s' and time<'%s'" % (tm_start,tm_end)
    rs_all,ok = executesql(sql,'s')
    if len(rs_all)==0:
        logging.info("no data in meter_datas,skip.datatable:%s,tm_start:%s" %(table,tm_start))
        return
    dt = tm_start
    v1,v2,v3 = 0,0,0
    l1,l2,l3 = 0,0,0
    pf1,pf2,pf3 = 0,0,0
    kva,kw,karl,hr=0,0,0,0
    kwh=0
    kva1,kva2,kva3=0,0,0
    kw1,kw2,kw3=0,0,0
    KVA,KW,KARL,OpeationHR=0,0,0,0
    rid=0
    tm_update=''
    i,iv1,iv2,iv3,il1,il2,il3,ip1,ip2,ip3,ik,ikva,ikw=0,0,0,0,0,0,0,0,0,0,0,0,0
    for rs in rs_all:
        tm = rs[11]
        tm_update=tm
        if tm.__ge__(tm_start) and tm.__lt__(tm_end):
            v1 += rs[1];v2 += rs[2];v3 += rs[3];l1 += rs[4];l2 += rs[5];l3 += rs[6]
            pf1 += rs[7];pf2 += rs[8];pf3 += rs[9]
            kwh += rs[10]
            rid=rs[15]
            #day count

            if rs[1]!=0 and rs[2]!=0 and rs[3]!=0 and rs[4]!=0 and rs[5]!=0 and rs[6]!=0:
                kva1=rs[1]*rs[4]/1000;kva2=rs[2]*rs[5]/1000;kva3=rs[3]*rs[6]/1000
                KVA+=kva1+kva2+kva3
                ikva+=1
            if rs[1]!=0 and rs[2]!=0 and rs[3]!=0 and rs[4]!=0 and rs[5]!=0 and rs[6]!=0 and rs[7]!=0 and rs[8]!=0 and rs[9]!=0:
                kw1=kva1*rs[7];kw2=kva2*rs[8];kw3=kva3*rs[9]
                KW+=kw1 +kw2+ kva3
                    
                hk1=kva1**2
                hw1=kw1**2
                h1=hw1-hk1
                hk2=kva2**2
                hw2=kw2**2
                h2=hw2-hk2
                hk3=kva3**2
                hw3=kw3**2
                h3=hw3-hk3
                KARL+=math.sqrt(h1)+math.sqrt(h2)+math.sqrt(h3)

                ikw+=1
            #count
            i += 1
            if rs[1]!=0:
                iv1+=1
            if rs[2]!=0:
                iv2+=1
            if rs[3]!=0:
                iv3+=1
            if rs[4]!=0:
                il1+=1
            if rs[5]!=0:
                il2+=1
            if rs[6]!=0:
                il3+=1
            if rs[7]!=0:
                ip1+=1
            if rs[8]!=0:
                ip2+=1
            if rs[9]!=0:
                ip3+=1
            if rs[10]!=0:
                ik+=1
    OpeationHR=il1*10
    if iv1>0:
        v1 = v1/iv1
    if iv2>0:
        v2 = v2/iv2
    if iv3>0:
        v3 = v3/iv3
    if il1>0:
        l1 = l1/il1
    if il2>0:
        l2 = l2/il2
    if il3>0:
        l3 = l3/il3
    if ip1>0:
        pf1 = pf1/ip1
    if ip2>0:
        pf2 = pf2/ip2
    if ip3>0:
        pf3 = pf3/ip3
    if ik>0:
        kwh=kwh/ik
    if ikva>0:
        KVA=KVA/ikva
    if ikw>0:
        KW=KW/ikw
        KARL=KARL/ikw

    #day count
    sql = "insert into %s (dt,v1,v2,v3,l1,l2,l3,pf1,pf2,pf3,kwh,kva,kw,karl,opeationHR,building_id,createTime) values('%s',%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,'%s')" % (table,dt, v1, v2, v3, l1, l2, l3, pf1, pf2, pf3, kwh,KVA,KW,KARL,OpeationHR,bid, datetime.now())
    results,ok=executesql(sql,'i')
    istot="total" in table
    if ok=="ok" and  istot==False:
        logging.info('insert sql:'+ok+' for table:'+table)
        table=table+"_all"
        sql = "insert into %s (dt,v1,v2,v3,l1,l2,l3,pf1,pf2,pf3,kwh,kva,kw,karl,opeationHR,building_id,createTime) values('%s',%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,'%s')" % (table,dt, v1, v2, v3, l1, l2, l3, pf1, pf2, pf3, kwh,KVA,KW,KARL,OpeationHR,bid, datetime.now())
        results,ok=executesql(sql,'i')
        if ok=="ok":
            logging.info('insert sql:'+ok+' for table:'+table)
    #update m_meters set lastMinuteTime
    '''
    if table=='m_minute_count':
        sql = "update m_meters set lastMinuteTime='%s' where id=%d" % (dt,bid)
    elif table=='m_hour_count':
        sql = "update m_meters set lastHourTime='%s' where id=%d" % (dt,bid)
    elif table=='m_day_day':
        sql = "update m_meters set lastDayTime='%s' where id=%d" % (dt,bid)
    elif table=='m_day_month':
        sql = "update m_meters set lastMonthTime='%s' where id=%d" % (dt,bid)
    results,ok=executesql(sql,'i')
    logging.info('update sql:'+ok+' for table:'+table)
    '''

#count data by minute
def countMinute():
    global lock_count_minute
    if lock_count_minute==1:
        return
    lock_count_minute=1
    logging.info('開始統計countMinute')
    results = ""
    table='m_minute_count'
    # loop meter_list
    for bid in building_list:
        if bid==0:
            table='m_minute_count_total'
        else:
            table='m_minute_count'
        logging.info('大廈：'+str(bid))
        tm_first,tm_last,datanum=getTimeRange(table,bid)
        if datanum <= 0 or tm_first==None or tm_last==None:
            continue
        tm_first = datetime.strptime(tm_first, "%Y-%m-%d %H:%M:%S")+timedelta(minutes=1)
        tm_last = datetime.strptime(tm_last, "%Y-%m-%d %H:%M:%S")
        tm_start = datetime(tm_first.year, tm_first.month,tm_first.day, tm_first.hour, tm_first.minute, 0)
        tm_end = tm_start+timedelta(minutes=1)

        while tm_start.__lt__(tm_end) and ((tm_start.__ge__(tm_first) and tm_start.__le__(tm_last)) or (tm_end.__ge__(tm_first) and tm_end.__le__(tm_last))):
            insertCount(tm_start,tm_end,bid,table)
            tm_start=tm_end
            tm_end = tm_start+timedelta(minutes=1)
    lock_count_minute=0

    countHour()

#count data by hour
def countHour():
    print('countHour %s' % (datetime.now()))
    results = ""
    table='m_hour_count'
    # loop meter_list
    for bid in building_list:
        if bid==0:
            table='m_hour_count_total'
        else:
            table='m_hour_count'
        tm_first,tm_last,datanum=getTimeRange(table,bid)
        if datanum <= 0 or tm_first==None or tm_last==None:
            continue
        tm_first = datetime.strptime(tm_first, "%Y-%m-%d %H:%M:%S")+timedelta(hours=1)
        tm_last = datetime.strptime(tm_last, "%Y-%m-%d %H:%M:%S")
        tm_start = datetime(tm_first.year, tm_first.month,tm_first.day, tm_first.hour, 0, 0)
        tm_end = tm_start+timedelta(hours=1)

        while tm_start.__lt__(tm_end) and ((tm_start.__ge__(tm_first) and tm_start.__le__(tm_last)) or (tm_end.__ge__(tm_first) and tm_end.__le__(tm_last))):
            insertCount(tm_start,tm_end,bid,table)
            tm_start=tm_end
            tm_end = tm_start+timedelta(hours=1)
    #繼續進行日統計
    countDay()

def countDay():
    print('countDay %s' % (datetime.now()))
    results = ""
    # loop meter_list to m_day_count
    for bid in building_list:
        if bid>0:
            table='m_day_count'
        else:
            table='m_day_count_total'
        tm_first,tm_last,datanum=getTimeRange(table,bid)
        if datanum <= 0 or tm_first==None or tm_last==None:
            continue
        tm_first = datetime.strptime(tm_first, "%Y-%m-%d %H:%M:%S")+timedelta(days=1)
        tm_last = datetime.strptime(tm_last, "%Y-%m-%d %H:%M:%S")
        tm_start = datetime(tm_first.year, tm_first.month,tm_first.day, 0, 0, 0)
        tm_end = tm_start+timedelta(days=1)

        while tm_start.__lt__(tm_end) and ((tm_start.__ge__(tm_first) and tm_start.__le__(tm_last)) or (tm_end.__ge__(tm_first) and tm_end.__le__(tm_last))):
            insertCount(tm_start,tm_end,bid,table)
            tm_start=tm_end
            tm_end = tm_start+timedelta(days=1)
    #繼續進行月統計
    countMonth()

def countMonth():
    print('countMonth %s' % (datetime.now()))
    results = ""
    table='m_month_count_total'
    # loop meter_list
    for bid in building_list:
        if bid>0:
            table='m_month_count'
        else:
            table='m_month_count_total'
        tm_first,tm_last,datanum=getTimeRange(table,bid)
        if datanum <= 0 or tm_first==None or tm_last==None:
            continue
        tm_first = datetime.strptime(tm_first, "%Y-%m-%d %H:%M:%S")
        tm_first=datetime(tm_first.year,(tm_first.month),tm_first.day)
        tm_last = datetime.strptime(tm_last, "%Y-%m-%d %H:%M:%S")
        tm_start = datetime(tm_first.year, tm_first.month,1, 0, 0, 0)
        tm_end = tm_start+relativedelta(months=1)

        while tm_start.__lt__(tm_end) and ((tm_start.__ge__(tm_first) and tm_start.__le__(tm_last)) or (tm_end.__ge__(tm_first) and tm_end.__le__(tm_last))):
            insertCount(tm_start,tm_end,bid,table)
            tm_start=tm_end
            tm_end = datetime(tm_start.year,(tm_start.month+1),tm_start.day)


def main():
    log()
    getConfig()
    #getMeters()
    getParams()
    getBuildings()
    ## schedule task
    scheduler = BlockingScheduler()
    ## excute scheduler
    scheduler.add_job(log, 'cron', hour=0,minute=10)
    scheduler.add_job(praseFiles, 'cron', hour=schedule_prase_file_hour)
    scheduler.add_job(cleanMeterData, 'cron', day=1,hour=0)
    scheduler.start()

if __name__ == '__main__':
    main()
