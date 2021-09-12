## 將 ma_crsoo_strgy.py 交易結果部分結構化，並提供更多資訊
## 2021.09.11

import pandas as pd
import utils
import instrument

import ma_res 

from dateutil.parser import *

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
    final_df.to_pickle('ma_test_res.pkl')
    
    print(final_df.shape, final_df.num_trades.sum())
    # print(final_df.info())
    # print(final_df.head())

# 6
def evaluate_pair(i_pair, mashort, malong, price_data):

    price_data = price_data[ ['time', 'mid_c', get_ma_col(mashort), get_ma_col(malong)]].copy()

    price_data['DIFF'] = price_data[get_ma_col(mashort)] - price_data[get_ma_col(malong)]
    price_data['DIFF_PREV'] = price_data['DIFF'].shift(1)
    price_data['IS_TRADE'] = price_data.apply(is_trade, axis=1)


    df_trades = price_data[price_data['IS_TRADE'] != 0].copy()
    df_trades['DELTA'] = ( df_trades['mid_c'].diff() / i_pair.pipLocation ).shift(-1)
    df_trades['GAIN'] = df_trades['DELTA'] * df_trades['IS_TRADE']

    df_trades["PAIR"] = i_pair.name
    df_trades["MASHORT"] = mashort # max short
    df_trades["MALONG"] = malong # max long

    # 2021.09.12 
    ## 不需要 MA 的 column，因為等下做迴圈時，不同組合會導致 NA 值很多
    del df_trades[get_ma_col(mashort)]
    del df_trades[get_ma_col(malong)]

    df_trades['time'] = [parse(x) for x in df_trades['time'] ]
    df_trades['DURATION'] = df_trades["time"].diff().shift(-1) # 跟 GAIN 一樣，需要上移一格
    df_trades['DURATION'] = [ x.total_seconds() / 3600 for x in df_trades['DURATION'] ]
    df_trades.dropna(inplace=True) # 去掉"最後一個"time

    return ma_res.MAResult(
        df_trades = df_trades,
        pairname = i_pair.name,
        params = {'mashort': mashort, 'malong' : malong}
        )

# 9
def store_trades(results):
    all_trade_df_list = [x.df_trades for x in results] # result 裡面有許多貨幣對與 MA 組成的 df_trades
    all_trade_df = pd.concat(all_trade_df_list)
    all_trade_df.to_pickle("all_trades.pkl")

# 8
def get_test_pairs(pair_str): # 找出可供交易的貨幣對
    existing_pairs = instrument.Instrument.get_instruments_dict().keys() # OANDA 允許我們交易的商品
    pairs = pair_str.split(",") # 將使用者欲交易的商品轉成 list

    test_list = [] 
    for p1 in pairs:
        for p2 in pairs:
            p = f'{p1}_{p2}'
            if p not in existing_pairs:
                continue
            test_list.append(p)

    return test_list

# 2
def run():
    currencies = "GBP,EUR,USD,CAD,JPY,NZD,CHF" # 欲交易的貨幣對
    # 注意: currencies 等一下要轉成 list，所以不要放空格

    
    granularity = "H1"
    
    # 給定各種長短 MA 組合
    ma_short = [4, 8, 16, 24, 32, 64]
    ma_long = [8, 16, 32, 64, 96, 128, 256]

    

    results = [] # 用一個 list 來放入各種週期 MA 的組合

    trade_list = get_test_pairs(currencies)
    print(trade_list)
    for t in trade_list:
        print("running..", t)

        i_pair = instrument.Instrument.get_instruments_dict()[t]
        price_data = get_price_data(t, granularity)
        price_data = process_data(ma_short, ma_long, price_data)

        for _malong in ma_long:
            for _mashort in ma_short:
                if _mashort >= _malong: # 慢線不能大於快線
                    continue

                results.append(evaluate_pair(i_pair, _mashort, _malong, price_data))

    process_result(results)

    store_trades(results)
    # 在 ma_cross_strgy_res_strc_2.png 可以看到總共交易了 87528 次，並使用了 840 種 MA 組合


if __name__ == "__main__":
    run()