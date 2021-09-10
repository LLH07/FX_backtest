# 不要用這份檔案，這份檔案的用途是方便觀察

import pandas as pd
import utils 

# refer to instrument.ipynb
# check new_ob in a for loop
class Instrument():
    def __init__(self, ob):
        self.name = ob['name']
        self.ins_type = ob['type'] # ins stands for instrument
        self.displayName = ob['displayName']
        self.pipLocation = pow(10, ob['popLocation']) # pow = power, popLocation 代表小數後第幾位
        # 這邊是將其轉為小數, eg: -4 -> 0.0001
        self.marginRate = ob['marginRate']

    def __repr__(self):
        return str(vars(self))
    
    @classmethod 
    def get_instrument_df(cls): # 查詢有哪些商品的資料可供查閱
        return pd.read_pickle(utils.get_instruments_data_filename())
        # read_pickle(): 將 pkl 檔轉為 data frame
    
    
if __name__ == '__main__':
    # print(Instrument.get_instrument_df()) # 去 Terminal 確認正常讀取資料
    df = Instrument.get_instrument_df()
    
    ll = df.to_dict(orient='records') # 回傳 list
    # ‘records’ : list like [{column -> value}, … , {column -> value}]
    # refer to: https://pandas.pydata.org/pandas-docs/dev/reference/api/pandas.DataFrame.to_dict.html

    for item in ll:
        print(item) # 成功將各商品及其性質各自列出