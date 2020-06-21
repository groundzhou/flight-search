#!/usr/bin/env python3

import json
import random
from datetime import datetime, timedelta
import requests
from requests.adapters import HTTPAdapter

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=2))
s.mount('https://', HTTPAdapter(max_retries=2))


# 从ip池获取代理ip
def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()


# 删除失效ip
def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


class IPBlockedException(Exception):
    pass


def save_point(date, i):
    """
    保存断点
    :param date: 日期
    :param i: 索引
    """
    with open('../data/checkpoints.txt', 'w') as f:
        json.dump({'date': date, 'i': i}, f)


def load_point():
    """
    读取断点
    :return: 返回断点日期、索引
    """
    with open('../data/checkpoints.txt', 'r') as f:
        j = json.load(f)
        return j['date'], j['i']


def get_cities():
    """
    获取主要城市
    :return: json格式城市列表
    """
    headers = {'Host': 'm.ctrip.com',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0',
               'Accept': 'application/json',
               'Accept-Language': 'zh-CN,en-US;q=0.5',
               'Accept-Encoding': 'gzip, deflate, br',
               'Content-Type': 'application/json',
               'Origin': 'https://m.ctrip.com',
               'Connection': 'keep-alive',
               'Referer': 'https://m.ctrip.com/webapp/flight/schedule/getInlandCity?&_fxpcqlniredt=09031049311771044837',
               'TE': 'Trailers'}
    url = 'https://m.ctrip.com/webapp/flight/schedule/getInlandCity?&_fxpcqlniredt=09031049311771044837'
    response = requests.get(url=url, headers=headers)
    return response.json()


def user_agent():
    """
    随机返回User Agent
    :return: ua list
    """
    ua_list = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
        'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    ]
    return random.choice(ua_list)


def request(source, destination, date, proxy):
    """
    爬取一次数据
    :param source: 出发地
    :param destination: 目的地
    :param date: 日期
    :param proxy: 代理
    :return: flight list
    """
    url = 'https://m.ctrip.com/restapi/soa2/14022/flightListSearch?_fxpcqlniredt=09031124412121055112'
    j = {"contentType": "json", "flag": 8,
         "head": {"auth": None, "cid": "09031124412121055112", "ctok": "", "cver": "1.0",
                  "extension": [{"name": "appId", "value": "100008344"}, {"name": "aid", "value": "66672"},
                                {"name": "sid", "value": "508668"}, {"name": "protocal", "value": "https"}],
                  "lang": "01", "sid": "8888", "syscode": "09"}, "preprdid": "",
         "rid": "BBE0515DAAFC4CB09A66E7C70B095E6F", "rtoken": "p0a7d551282e59075325029534b6fbdbd8326e82cfbee",
         "searchitem": [{"accode": destination, "dccode": source, "dtime": date}], "subchannel": None,
         "tid": "{d03ed6d8-24f3-4eab-b26e-2d49ddb865fc}", "trptpe": 1}
    headers = {'Host': 'm.ctrip.com',
               'User-Agent': user_agent(),
               'Accept': 'application/json',
               'Accept-Language': 'zh-CN,en-US;q=0.5',
               'Accept-Encoding': 'gzip, deflate, br',
               'X-Requested-With': 'XMLHttpRequest',
               'Content-Type': 'application/json',
               'Origin': 'https://m.ctrip.com',
               'Connection': 'keep-alive',
               'Referer': 'https://m.ctrip.com/html5/flight/swift/domestic/' + source + '/' + destination + '/' + date,
               'TE': 'Trailers'}

    try:
        response = s.post(url=url, headers=headers, json=j, timeout=4, proxies={"https": "http://{}".format(proxy)})
        fltitem = json.loads(response.text).get('fltitem', None)
        flights = []
        if fltitem:
            for f in fltitem:
                if len(f['mutilstn']) == 2:
                    continue

                punctuality = [i['stip'] for i in f['mutilstn'][0]['comlist'] if i['type'] == 2]
                line = [f['mutilstn'][0]['dportinfo']['aport'],
                        f['mutilstn'][0]['dportinfo']['aportsname'],
                        f['mutilstn'][0]['dportinfo']['bsname'],
                        f['mutilstn'][0]['dportinfo']['city'],
                        f['mutilstn'][0]['dportinfo']['cityname'],
                        f['mutilstn'][0]['aportinfo']['aport'],
                        f['mutilstn'][0]['aportinfo']['aportsname'],
                        f['mutilstn'][0]['aportinfo']['bsname'],
                        f['mutilstn'][0]['aportinfo']['city'],
                        f['mutilstn'][0]['aportinfo']['cityname'],
                        f['mutilstn'][0]['basinfo']['aircode'],
                        f['mutilstn'][0]['basinfo']['airsname'],
                        f['mutilstn'][0]['basinfo']['flgno'],
                        f['mutilstn'][0]['craftinfo']['craft'],
                        f['mutilstn'][0]['craftinfo']['kind'],
                        f['mutilstn'][0]['craftinfo']['cname'],
                        f['mutilstn'][0]['dateinfo']['ddate'],
                        f['mutilstn'][0]['dateinfo']['adate'],
                        f['policyinfo'][0]['priceinfo'][0]['price'],
                        f['policyinfo'][0]['priceinfo'][0]['drate'],
                        f['policyinfo'][0]['classinfor'][0]['display'],
                        punctuality[0] if punctuality else '',
                        len(f['mutilstn'][0]['fsitem'])]
                flights.append(','.join([str(i) for i in line]) + '\n')
    except requests.exceptions.RequestException as e:
        print('Time out', end='\t')
        raise Exception("Time out")
    except KeyError as e:
        print('Key Error', end='\t')
        raise Exception("Key Error")
    except:
        raise Exception("Other error")
    else:
        rlt = json.loads(response.text).get('rlt', None)
        if rlt == 508 or rlt == 509:
            raise IPBlockedException
        elif rlt != 0:
            print('No flight', end='\t')
            raise Exception('No flight')
        return flights


def main():
    # get_risk()
    # with open('../data/flights.csv', 'a') as f:
    #     f.writelines(request('ZUH', 'CKG', '2020-06-20'))

    # 城市列表
    with open('../data/cities.json') as f:
        cities = list(set([c['code'] for c in json.load(f)['inLandData']['inlandHot']]))
        cities.sort()

    # 从成都出发或返回成都
    departure = 'CTU'

    date, i = load_point()
    # 日期列表
    date_list = [datetime.strftime(datetime.strptime(date, '%Y-%m-%d') + timedelta(i), '%Y-%m-%d')
                 for i in range(120)]

    # 去程
    exception = 0
    for d in date_list:
        while i < len(cities):
            if cities[i] == 'CTU':
                i += 1
            retry_count = 5  # 重复2次
            proxy = get_proxy().get("proxy")
            while retry_count > 0:
                try:
                    flights = request(departure, cities[i], d, proxy)
                    with open('../data/flights.csv', 'a') as f:
                        f.writelines(flights)
                except IPBlockedException:
                    print('IP Blocked', i, departure, '-->', cities[i], d)
                    retry_count -= 3
                except:
                    print('Other Error', i, departure, '-->', cities[i], d)
                    retry_count -= 2
                else:
                    exception = 0
                    i += 1
                    break
            if retry_count <= 0:
                print('Delete proxy', proxy)
                delete_proxy(proxy)
                exception += 1
                if exception > 5:
                    save_point(d, i)
                    return
        i = 0

    # 返程
    exception = 0
    for d in date_list:
        while i < len(cities):
            if cities[i] == 'CTU':
                i += 1
            retry_count = 5  # 重复5次
            proxy = get_proxy().get("proxy")
            while retry_count > 0:
                try:
                    flights_return = request(cities[i], departure, d, proxy)
                    with open('../data/flights.csv', 'a') as f:
                        f.writelines(flights_return)
                except IPBlockedException:
                    print('IP Blocked', i, cities[i], '-->', departure, d)
                    retry_count -= 3
                except:
                    print('Other Error', i, cities[i], '-->', departure, d)
                    retry_count -= 2
                else:
                    exception = 0
                    i += 1
                    break
            if retry_count <= 0:
                print('Delete proxy:', proxy)
                delete_proxy(proxy)
                exception += 1
                if exception >= 5:
                    save_point(d, i)
                    return
        i = 0


if __name__ == '__main__':
    main()
