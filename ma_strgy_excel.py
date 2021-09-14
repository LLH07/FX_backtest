import pandas as pd
import xlsxwriter

# 2 
def add_pair_sheets(ma_test_res, writer):

    for p in ma_test_res.pair.unique():
        temp_df = ma_test_res[ma_test_res.pair==p]
        temp_df.to_excel(writer, sheet_name=p, index=False)

# 3 
# 2021.09.14 
## 目標: 藉 all_trades.pkl 的資料畫出每個 sheet (每組貨幣對)表現最好的 MA 組合的 cumsum
def add_pair_charts(ma_test_res, all_trades, writer):
    cols = ['time', 'CUM_GAIN']
    # step 1: 取得每一貨幣對的最佳 MA 組合
    # 注意到，在 create_excel() 裡，ma_test_res 檔案已經依照 total_gain 由最高到最低排了
    # 也就是說，只需取得每一個 sheet 的第一 row，可以用 pd 提供的 drop_duplicate()
    df_temp = ma_test_res.drop_duplicates(subset=['pair'])
   

    # step 2: 根據 df_temp 的 row (各貨幣對)，找出每個 row 的詳細交易資料
    for index, row in df_temp.iterrows(): # not the quickest way
        print(index)
        print(row)
        all_trades_temp = all_trades[ (all_trades['PAIR'] == row.pair) & (all_trades['CROSS'] == row.CROSS) ].copy()
        all_trades_temp['CUM_GAIN'] = all_trades_temp['GAIN'].cumsum()
        # print(all_trades_temp[ ['GAIN', 'CUMSUM']].tail(5)) 確認無誤

    # step 3: 將各 row 詳細資料儲存於 excel
        all_trades_temp[cols].to_excel(writer, sheet_name=row.pair, startrow=0, startcol=7)
   

# 1
def create_excel(ma_test_res, all_trades):
    filename = "ma_results.xlsx"
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')

    ma_test_res = ma_test_res[['pair', 'num_trades', 'total_gain','mashort', 'malong']].copy()
    ma_test_res["CROSS"] = "MA_" + ma_test_res.mashort.map(str) + "_" + ma_test_res.malong.map(str)

    ma_test_res.sort_values(by=["pair", "total_gain"], ascending=[True,False], inplace=True)

    all_trades["CROSS"] = "MA_" + all_trades['MASHORT'].map(str) + "_" + all_trades['MALONG'].map(str)

    # 接著要修改 all_trades 時間的顯示方式:
    all_trades['time'] = [x.replace(tzinfo=None) for x in all_trades['time']]

    add_pair_sheets(ma_test_res, writer)

    add_pair_charts(ma_test_res, all_trades, writer)

    writer.save()


if __name__ == "__main__":
    ma_test_res = pd.read_pickle("ma_test_res.pkl")

    all_trades = pd.read_pickle("all_trades.pkl")

    create_excel(ma_test_res, all_trades)
    print('succeed')