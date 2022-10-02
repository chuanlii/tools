
# -*- coding: utf-8 -*-
from encodings.utf_8 import encode
import sys
from textwrap import indent
import uuid
import requests
import hashlib
import time
from importlib import reload
import time
import json 


reload(sys)

YOUDAO_URL = 'https://openapi.youdao.com/api'
APP_KEY = ''
APP_SECRET = ''


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def fanyi(q,args):

    data = {}
    data['from'] = 'en'#'zh-CHS'
    data['to'] = 'zh-CHS'
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['q'] = q
    data['salt'] = salt
    data['sign'] = sign
    data['vocabId'] = ""

    response = do_request(data)
    
    js  =response.json()
    if js['errorCode'] != '0':
        print(js['errorCode'])
        return 
    if len(js['basic']["explains"] )>0:
        print(js['basic']["explains"][0])
    if '-e' in args:
        print("web释义:")
        if len(js["web"]) > 0:
            for item in js["web"]:
                print("    "+item["key"]+"\t:"+",".join(item["value"]))
    if '-v' in args:
        if js["speakUrl"]:
            print("voice url:")
            print(js["speakUrl"])
    if '-r' in args:
        print(json.dumps(js,indent=2,ensure_ascii=False))
if __name__ == '__main__':
    n = len(sys.argv)
    args = sys.argv 
    if n == 1:
        print("请输入要查询的词\n例如：fy apple")
    elif n == 2 and args[1] == 'help' or args[1] == '-h':
            hlp = '''
使用方式：
fy word [-d -v -h]
-e  :explain,更多信息
-v  :voice,语音链接
-r  :raw,原始数据
            '''
            print(hlp)
    else: 
        fanyi(args[1],args[2:])
    