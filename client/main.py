import requests, json,time,datetime,random,os,logging
#from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from urllib3 import encode_multipart_formdata

from des_verify import des_encrypt,des_descrypt

data_url=''
check_url=''
file_url=''
config={}
config['base_url'] = 'http://127.0.0.1:8000'
config['mac']=''
config['log_path']=''
config['hour']=''
config['minute']=''
#讀取數據文件間隔秒數
encode = 'utf-8'
bid=0
rid=0
loop_files=[]#遍歷文件數組
meters=[]#電錶數組
mids=[]
rasps=''
last_read_times=[]#最後讀取數據文件時間數組，與電錶數組數量一致
headers=''
locked=0
#file up param
data = {}
headers = {}

#Read local txt，get:raspberry mac、meter number
#Read server api，get:txt type、txt path、read second for txt
#Loop to find txt,upload file by api

#log info
def log():
    logger = logging.getLogger()
    fh = logging.FileHandler("client_log.log")
    sh = logging.StreamHandler()
    fm = logging.Formatter('%(asctime)s-%(filename)s[line%(lineno)d]-%(levelname)s-%(message)s')
    fh.setFormatter(fm)
    sh.setFormatter(fm)
    logger.addHandler(fh)
    logger.addHandler(sh)
    logger.setLevel(logging.DEBUG)

    #logging.debug("調試訊息")
    #logging.info("一般訊息")
    #logging.warning("警告訊息")
    #logging.error("錯誤訊息")
    #logging.critical("嚴重錯誤")
#Read local txt，get:raspberry mac、meter number
def getConfig():
    #get mac address from txt
    global config,data_url,check_url,meters,last_read_times,bid,rid,file_url
    with open('./config.txt', encoding=encode, mode = 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if line.find('||')>=0:
                sp1 = line.split("||")[0]
                sp2 = line.split("||")[1]
                config[sp1]=sp2
    data_url=config['base_url']+'/data/'
    check_url=config['base_url']+'/meter/'
    file_url=config['base_url']+'/upload/'
    #split meters
    if config['meter'].find('|')>=0:
        for m in config['meter'].split("|"):
            meters.append(m)
    else:
        meters.append(config['meter'])
    #get mid,bid,rid
    for j in range(0,len(meters)):
        bid,rid,mid=getParams(meters[j])
        last_read_time=getLastUpTime(mid)
        mids.append(mid)
        last_read_times.append(last_read_time)

#get mid bid rid from api
def getParams(meter):
    global upsecond
    data={'rasp':config['mac'],'meter':meter}
    jsonContent=callUrl(check_url,'get',data)
    if jsonContent!=None:
        return jsonContent['bid'],jsonContent['rid'],jsonContent['mid']
    else:
        locked=0
        return 0,0,0
#get last up time from api
def getLastUpTime(mid):
    data={'mid':mid}
    tm=''
    jsonContent=callUrl(file_url,'get',data)
    if jsonContent!=None:
        tm=jsonContent['tm']
    else:
        locked=0
        tm=''
    if tm=='':
        tm=config['last_read_time']
    return tm


#Loop path and child's path，get:txt path list
def loopFiles():
    global loop_files,locked
    if locked==1:
        return
    locked=1
    rootdir=config['log_path']
    for parent, dirnames, filenames in os.walk(rootdir,  followlinks=True):
        for filename in filenames:
            path = os.path.join(parent, filename)
            if os.path.isfile(path)==False:
                continue
            loop_files.append(path)
    loopRasps()
    loopMeters()
    locked=0
def loopRasps():
    global rasps
    logging.info("開始搜尋本機log文件……")
    for p in loop_files:
        fs=os.path.splitext(p)[0].split("-")
        fstr=fs[1]
        r=fstr in rasps
        if r==False:
            rasps+=fstr
            rasps+=','
    logging.info("搜尋到的文件數："+str(len(loop_files)))
    logging.info("搜尋到的log文件中的MAC地址有："+rasps)
    logging.info("配置文件中的MAC地址是："+config["mac"])
    if fstr in rasps:
        logging.info("配置文件中的MAC地址配置正確")
    else:
        logging.warning("配置文件中的MAC地址配置錯誤：mac地址與log名稱中的mac地址不符")
        
def loopMeters():
    #loop meters between config time and now,if contains,update
    delta = datetime.timedelta(days=1)
    length=len(meters)
    if len(mids)<length:
        length=len(mids)
    logging.info("電錶數："+str(length))
    
    for j in range(length):
        dtstr=last_read_times[j]
        if dtstr.find(' ')>0:
            dtstr=dtstr.split(' ')[0]
        dt=datetime.datetime.strptime(dtstr,'%Y-%m-%d')
        now = datetime.datetime.now()
        mid=mids[j]
        #loop date between config time and now
        for i in range((now - dt).days):
            dtl=dt + datetime.timedelta(days=i)
            logging.info("開始上傳："+str(dtl)+"的文件")
            #loop filepath to find meter's txt
            i_up=0
            for p in loop_files:
                fs=os.path.splitext(p)[0].split("-")
                dttstr=fs[3]+"-"+fs[4]+"-"+fs[5]
                dtt=datetime.datetime.strptime(dttstr,'%Y-%m-%d')
                if fs[1]==config['mac'] and fs[2]==meters[j] and dtl==dtt:
                    filename=os.path.basename(p)
                    #update file
                    hadup=0
                    while hadup==0:
                        logging.info('開始上傳:'+filename)
                        try:
                            resp=sendFile(filename,p,mid,dtl.strftime("%Y-%m-%d"))
                            hadup=1
                            logging.info('上傳成功:'+filename)
                        except:
                            logging.warning('上傳失敗，重新上傳')
                    #updata(p,dttstr,mid)
                    i_up+=1
            if i_up>0:
                logging.info("上傳完成，上傳文件數："+str(i_up))
            else:
                logging.info("處理完成，無文件上傳")
        logging.info(str(dt)+"至"+str(now)+"的文件處理完成")
    logging.info("所有電錶數據處理完成")

def sendFile(filename, file_path,mid,dt):
    global data,headers
    with open(file_path, mode="r", encoding="utf8")as f:
        file = {
				"file": (filename, f.read()),
				"name": filename,
                "meter_id": mid,
                "rasp_id": rid,
                "building_id": bid,
                "record_date":str(dt),
		}
        encode_data = encode_multipart_formdata(file)
        file_data = encode_data[0]
        headers['Content-Type'] = encode_data[1]
        r=0
        while r==0:
            r = requests.post(file_url, headers=headers, data=file_data, timeout=500)
            return r

def getHeaders():
    global headers
    #get token
    timespan = str(int(time.time()))
    tokenstr = config['mac'] + '_' + timespan
    token=des_encrypt(tokenstr)
    #get headers
    headers={'Token': token,'Timespan':timespan,'Content-Type':'application/json; charset=UTF-8'}

def callUrl(url,mthd,data):
    getHeaders()
    response=''
    print('url:',url)
    hadget=0
    while hadget==0:
        logging.info("正在請求伺服器……")
        if(mthd=='get'):
            try:
                response = requests.get(url,data =json.dumps(data), headers=headers)
                hadget=1
                logging.info("請求成功")
            except:
                response=''
                logging.warning("請求失敗，重新請求")
        else:
            try:
                response = requests.post(url=url,data =json.dumps(data),headers=headers)
                hadget=1
                logging.info("請求成功")
            except:
                response=''
                logging.warning("請求失敗，重新請求")
    if response.status_code<400:
        return json.loads(response.content.decode(encode))
    else:
        return None


def main():
    global mac, headers
    log()
    getConfig()
    loopFiles()
    #schedule task
    scheduler = BlockingScheduler()
    job2=scheduler.add_job(loopFiles, 'cron', hour=config['hour'],minute=config['minute'], id='updatajob')
    scheduler.start()

if __name__ == '__main__':
    main()




