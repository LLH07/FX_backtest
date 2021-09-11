# 將 ma_cross_strgy_eval.ipynb 轉為 function 形式
# 2021.09.11

import pandas as pd
import utils
import instrument

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

# 6
def evaluate_pair(i_pair, mashort, malong, price_data):
    price_data['DIFF'] = price_data[get_ma_col(mashort)] - price_data[get_ma_col(malong)]
    price_data['DIFF_PREV'] = price_data['DIFF'].shift(1)
    price_data['IS_TRADE'] = price_data.apply(is_trade, axis=1)


    df_trades = price_data[price_data['IS_TRADE'] != 0].copy()
    df_trades['DELTA'] = ( df_trades['mid_c'].diff() / i_pair.pipLocation ).shift(-1)
    df_trades['GAIN'] = df_trades['DELTA'] * df_trades['IS_TRADE']

    print(f"{i_pair.name} {mashort} {malong} 交易次數: {df_trades.shape[0]} 損益:{df_trades['GAIN'].sum() :.0f}")


    return df_trades['GAIN'].sum()

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

    # 開始回測
    best = -1000000.0 # 單位: pips，作用: 每次有更好的結果就更新
    b_mashort = 0 # 找出最好的慢線
    b_malong = 0 # 找出最好的快線

    for _malong in ma_long:
        for _mashort in ma_short:
            if _mashort >= _malong: # 慢線不能大於快線
                continue
            res = evaluate_pair(i_pair, _mashort, _malong, price_data.copy()) # 紀錄該 MA 組合的總損益

            if res > best:
                b_mashort = _mashort
                b_malong = _malong
                best = res
    print(f"最佳損益: {best:.0f} 最佳慢線: {b_mashort:.0f} 最佳快線: {b_malong:0f}")

if __name__ == "__main__":
    run()