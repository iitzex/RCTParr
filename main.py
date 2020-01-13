import time
from collections import OrderedDict
from datetime import date, datetime
from json import JSONDecodeError
from operator import itemgetter

import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters

import fr24

import numpy as np

register_matplotlib_converters()


def main():
    TPE = {}
    Tarray = []
    try:
        bounds = '71.81,-35.85,21.19,-82.17'
        j = fr24.area(bounds)
        # j = {**north, **south}
        # print(len(j))

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
                direction = 'N' if lat > 25.08 else 'S'
                row = {'cs': callsign,
                       'ts': pd.to_datetime(ts, unit='s'), 'lvl': level, 'lat': lat, 'lon': lon,
                       'direction': direction}
                Tarray.append(row)

                print('.', end='', flush=True)
        print('')

        with open('log', 'w') as f:
            TPE = OrderedDict(
                sorted(TPE.items(), key=itemgetter(1), reverse=True))
            # print(TPE)
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

            df = pd.DataFrame(Tarray)
            df.sort_values(by=['ts'], inplace=True)
            df = df[df['ts'] < df.iloc[0]['ts']+np.timedelta64(3600*4, 's')]
            north = df[df['direction'] == 'N']
            south = df[df['direction'] == 'S']

            plt.figure(figsize=(20, 5))
            plt.plot(df['ts'], len(df)*[0], marker='.', alpha=0.1)
            plt.scatter(north['ts'], len(north)*[0.1], marker='v', alpha=0.33)
            plt.scatter(south['ts'], len(south) *
                        [-0.1], marker='^', alpha=0.33)
            plt.gca().set_ylim([-5, 5])
            plt.savefig('timeline.png', bbox_inches='tight')

    except JSONDecodeError as e:
        print(e)


if __name__ == '__main__':
    while(True):
        main()
        # time.sleep(100)
