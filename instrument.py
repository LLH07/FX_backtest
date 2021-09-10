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
    
if __name__ == '__main__':
    # print(Instrument.get_instrument_df()) # 去 Terminal 確認正常讀取資料
    print(Instrument.get_instrument_list())