import pandas as pd
import matplotlib.pyplot as plt
import requests
import time


def timeStamp():
    return int(round(time.time()))


def returnChartData(tag):
    parameters = {"command": "returnChartData",
                  "currencyPair": tag,
                  "start": timeStamp() - 60 * 60 * 24 * 180,
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
df = returnTicker()
# print(df.head())
columns = []
stocks = pd.DataFrame()
for column in df.columns:
    if "BTC_" in column:
        columns.append(column)
        df = returnChartData(column)
        stocks = pd.concat([stocks, df['close']], axis=1)


stocks.columns = columns
stocks['Total'] = stocks.sum(axis=1)
x = stocks.pct_change(1).corr()
print(x)

plt.show()
