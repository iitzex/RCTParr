import time
from collections import OrderedDict
from datetime import date, datetime
from operator import itemgetter
from json import JSONDecodeError

import fr24


def main():
    total = 0
    TPE = {}
    try:
        bound = '38.00,20.50,103.50,142.60'
        j = fr24.area(bound)
        for k, v in j.items():
            if k == 'full_count' or k == 'version' or k == 'stats' or k == 'visible' or k == 'selected-aircraft':
                continue

            level = int(v[4])
            dst = v[12]
            if level == 0:
                continue

            if dst == 'TPE':
                lat = float(v[1])
                lon = float(v[2])
                level = int(v[4])
                src = v[11]
                callsign = v[16]

                total += 1
                ts = fr24.arr_time(k)
                if ts:
                    t = {callsign: int(ts)}
                    print(t)
                    TPE.update(t)
                    # print('.', end='')

        print(total)
        with open('log', 'w') as f:
            TPE = OrderedDict(sorted(TPE.items(), key=itemgetter(1)))
            for k, v in TPE.items():
                arr = datetime.fromtimestamp(v)
                print("%8s %02d:%02d" % (k, arr.hour, arr.minute))
                msg = "%8s %02d:%02d" % (k, arr.hour, arr.minute)
                f.write(msg+'\n')

    except JSONDecodeError as e:
        print(e)


if __name__ == '__main__':
    while True:
        main()
        time.sleep(60)
