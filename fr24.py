import time

import requests

import ujson

headers = {
    'Host': 'data-live.flightradar24.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:55.0) Gecko/20100101 Firefox/55.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Referer': 'https://www.flightradar24.com/24.61,121.52/8',
    'Origin': 'https://www.flightradar24.com',
    'DNT': '1',
    'Connection': 'keep-alive',
}


def area(bound):
    params = (
        ('bounds', bound),
        ('faa', '1'),
        ('mlat', '1'),
        ('flarm', '1'),
        ('adsb', '1'),
        ('gnd', '1'),
        ('air', '1'),
        ('vehicles', '1'),
        ('estimated', '1'),
        ('maxage', '14400'),
        ('gliders', '1'),
        ('stats', '1'),
    )
    r = requests.get('https://data-live.flightradar24.com/zones/fcgi/feed.js',
                     headers=headers, params=params)
    # print(r.url)

    j = r.json()
    # print(j)
    return j


def arr_time(ix):
    params = (
        ('version', '1.5'),
        ('flight', ix),
    )

    r = requests.get(
        'https://data-live.flightradar24.com/clickhandler/', headers=headers, params=params)

    try:
        j = r.json()
        arr = j['time']['estimated']['arrival']

        # for k, v in j.items():
        #     print(k, v)
        #     print('--')
        return arr


    except KeyError as e:
        pass


if __name__ == '__main__':
    ix = '1cdc722e'
    arr_time(ix)
