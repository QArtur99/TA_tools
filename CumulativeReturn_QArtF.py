import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from time import sleep
import requests
import time


def timeStamp():
    return int(round(time.time()))


def returnChartData(tag):
    parameters = {"command": "returnChartData",
                  "currencyPair": tag,
                  "start": timeStamp() - 60 * 60 * 24 * 7,
                  "end": timeStamp(),
                  "period": "7200"
                  }
    return publicMethod(parameters)


def returnTicker():
    parameters = {"command": "returnTicker"}
    return publicMethod(parameters)


def publicMethod(parameters):
    response = requests.get("https://poloniex.com/public", params=parameters)
    data = response.json()
    return pd.DataFrame(data)


pd.options.display.float_format = '{:.8f}'.format
#ccList = ["BTC_DCR", "BTC_MAID", "BTC_POT"]
df2 = pd.DataFrame()
highestValueDf = pd.DataFrame()
df = returnTicker()
ccList = []
stocks = pd.DataFrame()
for column in df.columns:
#for column in ccList:
    if "BTC_" in column:
        sleep(0.2)
        ccList.append(column)
        df2 = returnChartData(column)
        stocks = pd.concat([stocks, df2['close']], axis=1)

stocks.fillna(method="ffill", inplace=True)
stocks['total'] = stocks.sum(axis=1)
ccList.append('total')
stocks.columns = ccList

cumulative = pd.DataFrame()
for x in range(len(ccList)):
    cumulative[ccList[x]] = stocks[ccList[x]] / stocks[ccList[x]].iloc[0]

# set EMA instead of SMA
mean_df = pd.DataFrame(cumulative.apply(np.nanmean).to_dict(),index=[cumulative.index.values[-1]])
mean_df.columns = ccList
print(mean_df.head())

highestValue = np.argsort(-mean_df.iloc[[0]].values, axis=1)[:, :6]
highestValue = np.array(highestValue).tolist()[0]
for x in highestValue:
    highestValueDf = pd.concat([highestValueDf, cumulative[ccList[x]]], axis=1)

highestValueDf = pd.concat([highestValueDf, cumulative['total']], axis=1)
highestValueDf['date'] = pd.to_datetime(df2['date'], unit='s')
highestValueDf.fillna(method="ffill", inplace=True)
# highestValueDf = highestValueDf.loc[(highestValueDf['date'].notnull()), :]
highestValueDf.set_index('date', inplace=True)
highestValueDf.plot(figsize=(12, 8))
print(highestValueDf.tail())
plt.axhline(1.0, color='black', linestyle='--')

plt.show()
