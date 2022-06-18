
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
        pred = clf[t].predict(dataset_x[t][0])[0]

        # Time
        one_col.append(str(dd1.index[-1] + pd.DateOffset(hours=t+1)))
        # buy or sell
        if pred >= 0:
            one_col.append("buy")
            # prices
            one_col.append(2.51)
            # volume
            one_col.append(round(pred, 2))
        else:
            one_col.append("sell")
            # prices
            one_col.append(0.01)
            # volumn
            one_col.append(round(pred * -1, 2))

        print(one_col)
        cmd.append(one_col)

    print(cmd)
    #output(args.output, data)

    output(args.output, cmd)
