import os
import sys
import requests, json,time,hashlib

from des_verify import des_encrypt,des_descrypt

def getconfig():
    api_url = 'http://127.0.0.1:8000/check/'
    encode = 'utf-8'
    #get mac address from txt
    with open('./mac.txt', encoding=encode,  mode = 'r') as f:
        mac = f.readline()

    timespan = str(int(time.time()))
    tokenstr = mac + '_' + timespan
    token=des_encrypt(tokenstr)
    #data = json.dumps({"v1":2267,"v2":2269,"v3":2274,"l1":0,"l2":0,"l3":0,"pf1":0,"pf2":0,"pf3":0,"kwh":0,"building_id":1,"rasp_id":1,"meter_id":1,"time":"2019-04-13 00:01:24"})
    #r = requests.post(api_url, data, auth=('user', '*****'))
    #r = requests.get(api_url, data)
    headers={'Token': token,'Timespan':timespan}
    response = requests.get(api_url, headers=headers)
    resultStr = json.dumps(str(response.content,encoding = encode))
    resultStr = resultStr.encode(encode).decode("unicode-escape")
    resultJson=json.loads(response.content)
    jsonContent=resultJson[0]
    upsecond=jsonContent['paramValue']

getconfig()