# 2021.09.09
# 將前面講的各種取得資料的方式全部整合為一個 API

import requests
import pandas as pd
import defs # our personal api
import utils

class OandaAPI():
    
    def __init__(self):
        self.session = requests.Session()
    
    def fetch_instruments(self):
        # refer to instrument.ipynb 
        # 列出我們可以交易的所有貨幣對資料
        url = f'{defs.OANDA_URL}accounts/{defs.ACCOUNT_ID}/instruments'
        response = self.session.get(url, params=None, headers=defs.SECURE_HEADER)
        
        return response.status_code, response.json() 

        
    
    def get_instruments_df(self):
        # 先從 fetch_instruments 取得可供交易的資料
        code, data = self.fetch_instruments()
        
        if code == 200:
            df = pd.DataFrame.from_dict(data['instruments']) 
            # name, type, pipLocation 等都是 df 的 columns
            return df[ ['name', 'type', 'displayName', 'pipLocation', 'marginRate'] ]

        else:
            return None

    def fetch_candles(self, pair_name, count=None, granularity='H1', date_from=None, date_to=None):
        # refer to save_candles.ipynb
        url = f'{defs.OANDA_URL}instruments/{pair_name}/candles'

        params = dict( 
            granularity = granularity,
            price = 'MBA' # M: midpoint, B: bid, A: ask
        )

        #20210926: 提供更詳細的所需資料
        if date_from is not None and date_to is not None:
            params['from'] = int(date_from.timestamp())
            params['to'] = int(date_to.timestamp())
        elif count is not None: # 不以時間段取 candle，而是直接給總共需要多少根 candles
            params['count'] = count
        else: # 不給時間也不給目標 candles 數，就直接取 300 根 candle
            params['count'] = 300 
        
        response = self.session.get(url, params=params, headers=defs.SECURE_HEADER)
        
        # 2021.09.28 更新 bug 的處理方式
        # 若狀態不是 200，則不要回傳資料 (因為裡面沒東西)
        if response.status_code != 200:
            return response.status_code, None

        return response.status_code, response.json() # response_json() is a dict
    
    def save_instruments(self):
        df = self.get_instruments_df()
        if df is not None:
            df.to_pickle(utils.get_instruments_data_filename())

if __name__ == '__main__':
    api = OandaAPI()
    #api.save_instruments()
    date_from = utils.get_utc_dt_from_string("2021-09-09 00:00:00")
    date_to = utils.get_utc_dt_from_string("2021-09-15 00:00:00")

    print(date_from)
    print(api.fetch_candles('EUR_USD', date_from=date_from, date_to=date_to))
    