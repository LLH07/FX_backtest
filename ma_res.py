## for the use of ma_cross_strgy_res_strc.py
## 2021.09.11 

# Define a class to store the result
# 希望裡面可以包含: 各種統計值、MA_short 週期、MA_long 週期
class MAResult():
    def __init__(self, df_trades, pairname, params):
        self.pairname = pairname
        self.df_trades = df_trades
        self.params = params
    
    def result_ob(self):
        d = {
            'pair' : self.pairname,
            'num_trades' : self.df_trades.shape[0], # 忘記定義可以看 ma_cross_strgy.py
            'total_gain' : self.df_trades.GAIN.sum(),
            'mean_gain' : self.df_trades.GAIN.mean(),
            'min_gain': self.df_trades.GAIN.min(),
            'max_gain': self.df_trades.GAIN.max()
        }

        for k,v in self.params.items(): # 存放短長線的週期 (MA short, MA long)
            d[k] = v
        
        return d


# previous code:
