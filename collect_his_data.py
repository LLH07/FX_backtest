# 2021.09.27 取得更多 granularity 資料
# 本次目標跟之前差不多，主要就是找出可供交易的貨幣對，只是這次我們同時考慮不同的 granularity

import pandas as pd
import datetime as dt

#自定義 方法
from instrument import Instrument
import utils
from oanda_api import OandaAPI

INCREMENTS = {
    'M5' : 5,
    'H1' : 60,
    'H4' : 240
}

# 2021.09.27 收集更多 candles 
def create_file(pair, granularity, api): # 之後會放在 run_collection() 的迴圈內 (for every graunlarity)
    candle_count = 2000 # Oanda 一次最多可以查詢 5000 個 分鐘 candle，這邊設定一次取 2000 個
    time_step = INCREMENTS[granularity] * 2000 # eg: 如果是 M5，代表本次取得的 candle 可回朔到 2000*5 = 1000 (分鐘，大約一天)

    end_date = utils.get_utc_dt_from_string("2020-12-31 23:59:59")
    date_from = utils.get_utc_dt_from_string("2018-01-01 00:00:00")

    candles_df = [] # 存放 candle 資料
    date_to = date_from # 開始計時

    while date_to < end_date:
        date_to = date_from + dt.timedelta(minutes=time_step)
        if date_to > end_date:
            date_to = end_date

        print(date_from, date_to)
        date_from = date_to # 更新每筆資料的資料起始日期
    # 可以看到左方，H4 candle 每次呼叫 API 取得的資料範圍約是 11 個月，其算法是:
    # 4 * 60 * 2000 = 480,000 (mins) = 11 months

def run_collection():
    pair_list = "GBP,EUR,USD,CAD,JPY,NZD,CHF"
    api = OandaAPI()

    for g in INCREMENTS:
        for i in Instrument.get_pairs_from_strings(pair_list):
            print(g, i)
            create_file(i, g, api)

if __name__ == "__main__":
    run_collection()
