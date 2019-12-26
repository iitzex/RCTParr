import time
from collections import OrderedDict
from datetime import date, datetime
from json import JSONDecodeError
from operator import itemgetter

import fr24


def main():
    TPE = {}
    try:
        bounds = '71.81,-35.85,21.19,-82.17'
        j = fr24.area(bounds)
        # j = {**north, **south}
        print(len(j))

        for k, v in j.items():
            if k == 'full_count' or k == 'version' or k == 'stats' or k == 'visible' or k == 'selected-aircraft':
                continue

            level = int(v[4])
            if level == 0:
                continue

            dst = v[12]
            lat = float(v[1])
            lon = float(v[2])
            src = v[11]
            callsign = v[16]

            ts = fr24.arrtime(k)
            if ts:
                t = {callsign: [int(ts), level, lat, lon]}
                TPE.update(t)
                # print(t)
                print('.', end='', flush=True)
        print('')

        with open('log', 'w') as f:
            TPE = OrderedDict(
                sorted(TPE.items(), key=itemgetter(1), reverse=True))

            for k, v in TPE.items():
                arr = datetime.fromtimestamp(v[0])
                msg = ''
                if v[2] > 25.08:
                    direction = 'N'
                    msg = f'{"":9s}|{k:<9s} {arr.time()}, {direction} :{v[1], v[2], v[3]}'
                else:
                    direction = 'S'
                    msg = f'{k:>9s}|{"":9s} {arr.time()}, {direction} :{v[1], v[2], v[3]}'
                f.write(msg+'\n')
                print(msg)

    except JSONDecodeError as e:
        print(e)


if __name__ == '__main__':
    while(True):
        main()
        # time.sleep(100)
