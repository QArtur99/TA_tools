import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
import time


def timeStamp():
    return int(round(time.time()))


def returnChartData(tag):
    parameters = {"command": "returnChartData",
                  "currencyPair": tag,
                  "start": timeStamp() - 60 * 60 * 24 * 3,
                  "end": timeStamp(),
                  "period": "900"
                  }
    return publicMethod(parameters)


def returnTicker():
    parameters = {"command": "returnTicker"}
    return publicMethod(parameters)


def publicMethod(parameters):
    response = requests.get("https://poloniex.com/public", params=parameters)
    data = response.json()
    return pd.DataFrame(data)


def sharpRatio(tag):
    if "BTC_" not in tag:
        return False

    df = returnChartData(tag)
    df['Normed Return'] = df['close'] / df.iloc[0]['close']
    df['Daily Return'] = df['Normed Return'] -1

    cumulative_return = 100 * (df['Normed Return'].iloc[-1] / df['Normed Return'].iloc[0] - 1)
    if cumulative_return > 5:
        row_cr = ["Cumulative return: ", str(tag), str(cumulative_return)]
        print("{: >20} {: >20} {: >20}".format(*row_cr))

    SR = df['Daily Return'].mean() / df['Daily Return'].std()
    # print("Sharpe Ratio: " + str(tag) + str(SR))
    ASR = ((3 * 24 * 4) ** 0.5) * SR
    # print("Annual Sharpe Ratio: " + str(tag) + " " + str(ASR))
    if ASR > 2:
        row = ["Annual Sharpe Ratio:", str(tag), str(ASR)]
        print("{: >20} {: >20} {: >20}".format(*row))


pd.options.display.float_format = '{:.8f}'.format
df = returnTicker()
# print(df.head())
for column in df.columns:
    sharpRatio(column)

plt.show()
