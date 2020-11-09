import jwt
import requests
import time
import os

shop_list = open('src_main_resources_sid_uuid_map.json', 'r').readlines()
path = r'demo_result.txt'
if os.path.exists(path):  # 如果文件存在
    os.remove(path)


def get_token(sid):
    return jwt.encode({"shop_id": int(sid)}, '', 'HS256').decode('utf8')


def make_request(token):
    headers = {"Authentication-Token": token}
    response = requests.get("https://stg-api.leyanbot.com/ford/v1/store_report/uuid", headers=headers)
    return response.text


sid = ''
flag = ''
i = 0
resp = ''
for shop in shop_list:
    if ':' in shop:
        get_shop = shop.split('"')
        sid, uuid = get_shop[1], get_shop[3]
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
            open('demo_result.json', 'a+').write(str(sid) + flag + str(i) + '\n')
            continue
        if uuid in resp:
            flag = 'pass'
        else:
            flag = 'failed!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
        print(sid, flag, i)
        open('demo_result.txt', 'a+').write(str(sid) + flag + str(i) + '\n')

