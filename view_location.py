import pandas as pd
from pandas import Series
from collections import defaultdict
import requests
import urllib
import json
import re
from datetime import datetime
from baidu_util import search_list


def split_name_level(name):
    if name.endswith('A'):
        new_name = name[:-3].strip()
        level = name[-2:]
        return new_name, level
    else:
        return name, None


def split_use_time(usetime):
    # 2020.11.1-2021.10.31
    index = usetime.find(',')
    if index > 0:
        # 2020年11月，2021年2月，3月
        if '-' not in usetime[:index]:
            return None, usetime
        else:
            return usetime[:index], usetime[index + 1:]
    # 只有时间的场景
    elif '-' in usetime:
        return usetime, None
    # 其他特殊场景
    index = usetime.find(' ')
    if index > 0:
        return usetime[:index], usetime[index + 1:].strip()
    return None, usetime


def formate_full_time(timestr):
    timestr = timestr.replace('-', '.')
    items = timestr.split('.')
    if len(items) == 3:
        items[1] = items[1].rjust(2, '0')
        items[2] = items[2].rjust(2, '0')
        return '.'.join(items)


def split_start_end_time(start_end):
    if not start_end:
        return None, None
    index = start_end.find('-')
    if index > 0:
        start = formate_full_time(start_end[:index])
        end = formate_full_time(start_end[index+1:])
        return start, end
    return None, None


def parse_addr():
    data_path = r'data\data1.xlsx'
    df = pd.read_excel(data_path)
    rows = defaultdict(list)
    last_name = None
    timedetail = None
    for row_id, row in df.iterrows():
        name = row['景区名称']
        price = row['票价']
        rights = row['使用权益']
        timestr = row['接待时间']
        if pd.isnull(price) and pd.isnull(timestr):
            continue
        if pd.isnull(last_name) and\
                not pd.isnull(name):
            # 新的一行数据
            # 拆分上调数据的时间
            if timedetail:
                start_end, detail = split_use_time(timedetail)
                start, end = split_start_end_time(start_end)
                rows['start'].append(start)
                rows['end'].append(end)
                rows['detail'].append(detail)

            name, level = split_name_level(name)
            rows['name'].append(name)
            rows['level'].append(level)
            rows['price'].append(price)
            rows['rights'].append(rights)
            timedetail = timestr

        elif not pd.isnull(timestr):
            timedetail = timedetail + ',' + timestr
    else:
        start_end, detail = split_use_time(timedetail)
        start, end = split_start_end_time(start_end)
        rows['start'].append(start)
        rows['end'].append(end)
        rows['detail'].append(detail)

        name_arr = rows['name']
        locat_arr = search_list(name_arr)
        rows['lat'] = [x['lat'] for x in locat_arr]
        rows['lng'] = [x['lng'] for x in locat_arr]
        df = pd.DataFrame(rows)
        df.to_excel('data/new_data.xlsx')
        print('over')


if __name__ == "__main__":
    # name = '北京国际鲜花港（顺义） 4A'
    # name, level = split_name_level(name)
    parse_addr()
