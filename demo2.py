

import json
import jwt
import requests
import time
import os

shop_dict = json.load(open("src_main_resources_store_for_wechat.json", 'r'))
path = r'demo2_result.txt'
if os.path.exists(path):  # 如果文件存在
    os.remove(path)

def get_token(sid):
    return jwt.encode({"shop_id": int(sid)}, '', 'HS256').decode('utf8')


def make_request(token):
    headers = {"Authentication-Token": token}
    response = requests.get("https://stg-api.leyanbot.com/ford/v1/report/wechat", headers=headers)
    return response.text


flag = ''
sid = ''
i = 0
resp = ''
for sid in shop_dict:
    token = get_token(sid)
    for i in range(10):
        try:
            resp = make_request(token)
        except BaseException:
            time.sleep(5)
        else:
            break
    if i == 9:
        flag = 'connect timeout!'
        print(sid, flag, i)
        open('demo2_result.json', 'a+').write(str(sid) + flag + str(i) + '\n')
        continue

    for info in shop_dict[sid]:
        if str(shop_dict[sid][info]) not in resp:
            flag = 'failed!!!!!!!!!!!!!'
            break
        else:
            flag = 'pass'
    print(sid, flag, i)
    open('demo2_result.txt', 'a+').write(str(sid) + flag + str(i)+'\n')
