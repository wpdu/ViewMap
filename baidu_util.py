import pandas as pd
import requests
import urllib
import json
import time

# data_path = r'data\data1.xlsx'
# df = pd.read_excel(data_path)

ak = 'G3gUDHyyAOoB7alD9WGfuNbkp4Cqullo'


def addr_decode(addr):
    url = 'http://api.map.baidu.com/geocoding/v3/'
    # address=北京市海淀区上地十街10号&output=json&ak=您的ak&callback=showLocation
    addr = urllib.parse.quote(addr)
    args = {'address': addr, 'output': 'json', 'ak': ak}
    ret = requests.get(url, params=args)
    text = ret.content.decode('utf8')
    jobj = json.loads(text)
    if jobj['status'] == 200:
        print(jobj)
    print(ret.text)


def search(name):
    '''根据名称获取定位 lat lng dict'''
    err = None
    try:
        url = f'http://api.map.baidu.com/place/v2/search'
        args = {'query': name, 'region': '北京', 'output': 'json', 'ak': ak}
        ret = requests.get(url, args)
        if ret.status_code == 200:
            text = ret.content.decode('utf8')
            jobj = json.loads(text)
            if jobj['status'] == 0:
                if len(jobj['results']) > 0 and\
                        jobj['result_type'] == 'poi_type':
                    return jobj['results'][0]['location']
                else:
                    err = '搜索结果为空'
            else:
                err = jobj['message']
        else:
            err = 'err 网络异常'
    except Exception as ex:
        err = str(err)
    print(f'{err}：{name}')
    return {'lat': None, 'lng': None}


def search_list(name_arr):
    locat_arr = []
    for name in name_arr:
        location = search(name)
        time.sleep(3)  # 防止并发限制
        locat_arr.append(location)
    return locat_arr


if __name__ == "__main__":
    addr = '北京国际鲜花港'
    search(addr)
