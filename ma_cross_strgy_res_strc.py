## 將 ma_crsoo_strgy.py 交易結果部分結構化，並提供更多資訊
## 2021.09.11

import pandas as pd
import utils
import instrument

import ma_res 

# 算完一堆 MA 後，console 會隱藏許多資料，可以用指令修改:
pd.set_option('display.max_columns', None)

# 1
def is_trade(row):
    if row.DIFF >= 0 and row.DIFF_PREV < 0: # 進場做多
        return 1
    if row.DIFF <= 0 and row.DIFF_PREV > 0: # 進場做空
        return -1 
    else:  # 否則就不進場
        return 0

# 3 
def get_ma_col(ma): # get ma column
    return f"MA_{ma}"

# 4 
def get_price_data(pairname, granularity):
    df = pd.read_pickle(utils.get_his_data_filename(pairname, granularity))

    non_cols  = ['time', 'volume']
    mod_cols = [x for x in df.columns if x not in non_cols]
    df[mod_cols] = df[mod_cols].apply(pd.to_numeric)

    return df[ ['time', 'mid_c'] ].copy() # 這次不用視覺化，因此只須保留重要資訊

# 5 
def process_data(ma_short, ma_long, price_data):
    ma_list = set(ma_short + ma_long) # 因為 ma_short 與 ma_long 有重複的地方，因此用 set 將 unique 值取出

    for ma in ma_list:
        price_data[get_ma_col(ma)] = price_data['mid_c'].rolling(window=ma).mean()

    return price_data

# 7 
def process_result(results): # 將 MAResult 的字典轉為 data frame
    results_list = [r.result_ob() for r in results] # 回傳的結果 results_list 是一個 dictionary!
    #print(results_list)

    final_df = pd.DataFrame.from_dict(results_list)

    print(final_df.info())
    print(final_df.head())

# 6
def evaluate_pair(i_pair, mashort, malong, price_data):
    price_data['DIFF'] = price_data[get_ma_col(mashort)] - price_data[get_ma_col(malong)]
    price_data['DIFF_PREV'] = price_data['DIFF'].shift(1)
    price_data['IS_TRADE'] = price_data.apply(is_trade, axis=1)


    df_trades = price_data[price_data['IS_TRADE'] != 0].copy()
    df_trades['DELTA'] = ( df_trades['mid_c'].diff() / i_pair.pipLocation ).shift(-1)
    df_trades['GAIN'] = df_trades['DELTA'] * df_trades['IS_TRADE']

    return ma_res.MAResult(
        df_trades = df_trades,
        pairname = i_pair.name,
        params = {'mashort': mashort, 'malong' : malong}
        )

# 2
def run():

    pairname = "EUR_CHF"
    granularity = "H1"
    
    # 給定各種長短 MA 組合
    ma_short = [8, 16, 32, 64]
    ma_long = [32, 64, 128, 256]

    # 取得 instrument 資訊
    i_pair = instrument.Instrument.get_instrument_by_name(pairname)
    
    # 加入 MA 與其他資料
    price_data = get_price_data(pairname, granularity)
    price_data = process_data(ma_short, ma_long, price_data)

    results = [] # 用一個 list 來放入各種週期 MA 的組合

    for _malong in ma_long:
        for _mashort in ma_short:
            if _mashort >= _malong: # 慢線不能大於快線
                continue

            results.append(evaluate_pair(i_pair, _mashort, _malong, price_data))

    process_result(results)


if __name__ == "__main__":
    run()