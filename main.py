
# You should not modify this part.
def config():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--consumption", default="./sample_data/consumption.csv", help="input the consumption data path")
    parser.add_argument("--generation", default="./sample_data/generation.csv", help="input the generation data path")
    parser.add_argument("--bidresult", default="./sample_data/bidresult.csv", help="input the bids result path")
    parser.add_argument("--output", default="output.csv", help="output the bids path")

    return parser.parse_args()


def output(path, data):
    import pandas as pd

    df = pd.DataFrame(data, columns=["time", "action", "target_price", "target_volume"])
    df.to_csv(path, index=False)

    return


import numpy as np
import pandas as pd
from scipy.stats import skew
from scipy.stats import kurtosis

import random

if __name__ == "__main__":
    args = config()

    import joblib
    clf = joblib.load("gbm.pkl")

    dd1 = pd.read_csv(args.consumption, index_col=None)
    dd2 = pd.read_csv(args.generation, index_col=None)

    dd1['generation'] = dd2['generation'].copy()
    dd1['time'] = pd.to_datetime(dd1['time'])
    dd1.set_index('time', inplace=True)

    df_all = []
    for i in range( 24 ):
        df_all.append( dd1.loc[dd1.index.to_series().dt.hour == i] )

    dataset_x = []
    for t in range( 24 ):
        tmp_x = []
        atmp = df_all[t].reset_index().drop('time', axis=1).iloc[:]
        aatmp = atmp.groupby(atmp.index // 7 ).agg({'min', 'max', 'sum', skew, kurtosis}).values
        tmp_x.append(aatmp)

        dataset_x.append(tmp_x)

    for i in range( 24 ):
        dataset_x[i] = np.asarray(dataset_x[i])

        
    cmd = []
    for t in range(24):
        one_col = []
        h_vol = 0
        l_vol = 0
        pred = clf[t].predict(dataset_x[t][0])[0]
        # Time
        one_col.append(str(dd1.index[-1] + pd.DateOffset(hours=t+1)))
        # buy or sell
        haha_price = 0
        haha_value = 0

        if pred >= 0:
            one_col.append("buy")

            # one third
            h_vol = round(pred / random.randint(3, 6), 2)
            l_vol = round(pred - h_vol, 2)

            # prices
            if ((t+1) <= 6) or ((t+1) >= 18):
                haha_price = round(random.randint(253,350) / 100, 2)
                haha_value = h_vol
                one_col.append(round(haha_price, 2))

            else:
                one_col.append(round(random.randint(255,260) / 100, 2))
            # volume
            #one_col.append(round(pred, 2))
            one_col.append(round(h_vol, 2))
            
        else:
            one_col.append("sell")
            # prices
            # one_col.append(0.01)
            h_vol = round((pred * -1) / random.randint(6, 12), 2)
            l_vol = round((pred * -1) - h_vol, 2)
            
            one_col.append(0.01)
            #one_col.append(random.randint(180,240) / 100)
            # volumn
            one_col.append(round(h_vol, 2))

        print(one_col)
        cmd.append(one_col)

        #---------------------------------------------------

        one_col = []
        one_col.append(str(dd1.index[-1] + pd.DateOffset(hours=t+1)))
        # buy or sell
        if pred >= 0:
            one_col.append("buy")

            # one third
            #h_vol = round(pred / random.randint(3, 6), 2)
            #l_vol = round(pred - h_vol, 2)

            # prices
            one_col.append(2.52)
            # volume
            #one_col.append(round(pred, 2))
            one_col.append(round(l_vol, 2))
            print(one_col)
            cmd.append(one_col)
        else:
            one_col.append("sell")
            # prices
            # one_col.append(0.01)
            #pred = pred * -1
            #h_vol = round(pred / random.randint(3, 6), 2)
            #l_vol = round(pred - h_vol, 2)
            
            #one_col.append(0.01)
            one_col.append(random.randint(240,253) / 100)
            # volumn
            one_col.append(round(l_vol, 2))
            print(one_col)
            cmd.append(one_col)

        #---------------------------------------------------

        one_col = []
        # Time
        one_col.append(str(dd1.index[-1] + pd.DateOffset(hours=t+1)))
        # buy or sell
        if pred >= 0:
            one_col.append("buy")
            one_col.append(0.01)
            one_col.append(random.randint(1,2) / 100)
        else:
            one_col.append("sell")
            one_col.append(round(random.randint(254,270) / 100, 2))
            one_col.append(random.randint(300, 1000) / 100)
        
        print(one_col)
        cmd.append(one_col)

        #---------------------------------------------------

        one_col = []
        # Time
        one_col.append(str(dd1.index[-1] + pd.DateOffset(hours=t+1)))
        # buy or sell
        if pred >= 0:
            if ((t+1) <= 6) or ((t+1) >= 18):
                one_col.append("sell")
                one_col.append(0.01)
                one_col.append(round(haha_value, 2))
            
            else:
                one_col.append("sell")
                one_col.append(round(random.randint(254,270) / 100, 2))
                one_col.append(random.randint(1000,2000) / 100)
        else:
            one_col.append("sell")
            one_col.append(2.53)
            one_col.append(random.randint(300, 1000) / 100)
        
        print(one_col)
        cmd.append(one_col)


    print(cmd)
    #output(args.output, data)

    output(args.output, cmd)
