# 修改自 instrument_comp.py
# 將主程式部分用 classmethod 方式寫出

import pandas as pd
import utils 

# refer to instrument.ipynb
# check new_ob in a for loop
class Instrument():
    def __init__(self, ob):
        self.name = ob['name']
        self.ins_type = ob['type'] # ins stands for instrument
        self.displayName = ob['displayName']
        self.pipLocation = pow(10, ob['pipLocation']) # pow = power, popLocation 代表小數後第幾位
        # 這邊是將其轉為小數, eg: -4 -> 0.0001
        self.marginRate = ob['marginRate']

    def __repr__(self):
        return str(vars(self))
    
    @classmethod 
    def get_instrument_df(cls): # 查詢有哪些商品的資料可供查閱
        return pd.read_pickle(utils.get_instruments_data_filename())
        # read_pickle(): 將 pkl 檔轉為 data frame
    
    @classmethod
    def get_instrument_list(cls): # cls stands for class
        df = cls.get_instrument_df()
        return [Instrument(x) for x in df.to_dict(orient='records')]
        # 別忘了把轉成 Instrument class!!!

    # 2021.09.11 We need a function to get specific candle:
    @classmethod
    def get_instruments_dict(cls):
        # dictionary comprehension:
        i_list = cls.get_instrument_list() # i_list 裡面的元素皆是 Instrument 物件
        i_keys = [x.name for x in i_list]
        return {k:v for (k,v) in zip(i_keys, i_list)} # create a dict

    # 2021.09.11 再寫個 function，從 get_instrument_dict 取得資料
    @classmethod
    def get_instrument_by_name(cls, pairname):
        d = cls.get_instruments_dict()
        if pairname in d:
            return d[pairname]
        else:
            return None

    # 2021.09.27 更新: 過濾所有貨幣對
    @classmethod
    def get_pairs_from_strings(cls, pair_str):
        existing_pairs =cls.get_instruments_dict().keys()
        pairs = pair_str.split(",")
        
        pair_list = []
        for p1 in pairs:
            for p2 in pairs:
                p = f'{p1}_{p2}'
                if p in existing_pairs:
                    pair_list.append(p) # 將真實存在的貨幣對加入 pair_list 中

        return pair_list

if __name__ == '__main__':
    # print(Instrument.get_instrument_df()) # 去 Terminal 確認正常讀取資料
    # print(Instrument.get_instrument_list())

    # test get_instruments_dict():
    #for k,v in Instrument.get_instruments_dict().items():
     #   print(k, v)
    
    print(Instrument.get_instrument_by_name("EUR_USD"))
    print(Instrument.get_pairs_from_strings("GBP,EUR,USD,CAD,NZD,CHF,JPY"))