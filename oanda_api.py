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

    def fetch_candles(self, pair_name, count, granularity):
        # refer to save_candles.ipynb
        url = f'{defs.OANDA_URL}instruments/{pair_name}/candles'

        params = dict(
            count = count, 
            granularity = granularity,
            price = 'MBA' # M: midpoint, B: bid, A: ask
        )
        
        response = self.session.get(url, params=params, headers=defs.SECURE_HEADER)
        
        return response.status_code, response.json() # response_json() is a dict
    
    def save_instruments(self):
        df = self.get_instruments_df()
        if df is not None:
            df.to_pickle(utils.get_instruments_data_filename())

if __name__ == '__main__':
    api = OandaAPI()
    api.save_instruments()