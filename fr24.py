import time

import requests

headers = {
    'Host': 'data-live.flightradar24.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:55.0) Gecko/20100101 Firefox/55.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Referer': 'https://www.flightradar24.com/24.61,121.52/3',
    'Origin': 'https://www.flightradar24.com',
    'DNT': '1',
    'Connection': 'keep-alive',
}


def area(bounds):
    params = (
        ('bounds', bounds),
        ('faa', '0'),
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
        ('to', 'TPE'),

    )
    r = requests.get('https://data-live.flightradar24.com/zones/fcgi/feed.js',
                     headers=headers, params=params)
    j = r.json()
    return j


def detail(bounds, ix):
    params = (
        ('bounds', bounds),
        ('faa', '1'),
        ('satellite', '1'),
        ('mlat', '1'),
        ('flarm', '1'),
        ('adsb', '1'),
        ('gnd', '1'),
        ('air', '1'),
        ('vehicles', '0'),
        ('estimated', '1'),
        ('maxage', '14400'),
        ('gliders', '0'),
        ('stats', '1'),
        ('selected', ix),
        ('ems', '1'),
        ('enc', 'qPgPtpctGA0YZPTS9NF_mD6QVwq27mkhfOawf2qaSh4'),
        ('to', 'TPE'),
    )

    r = requests.get(
        'https://data-live.flightradar24.com/zones/fcgi/feed.js', headers=headers, params=params)

    try:
        j = r.json()
        assigned = j[ix]

        ems = j['selected-aircraft']['ems']

        return assigned[3:6]
    except KeyError as e:
        pass


def arrtime(ix):
    params = (
        ('version', '1.5'),
        ('flight', ix),
    )

    r = requests.get(
        'https://data-live.flightradar24.com/clickhandler/', headers=headers, params=params)

    try:
        j = r.json()
        arr = j['time']['estimated']['arrival']

        return arr
    except KeyError as e:
        pass


if __name__ == '__main__':
    # ix = '1cdc722e'
    # arr_time(ix)

    bounds = '71.81,-35.85,21.19,-82.17'
    # j = area(bounds)
    # print(j)
    ix = '234c2a8a'
    r = detail(bounds, ix)
    print(r)
