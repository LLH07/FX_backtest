```pd.from_dict()``` 裡面除了以 ```dict``` 資料型態帶入外，```list``` 裡面有很多個  ```dict``` 同樣也可以。

eg: 

```
[
{'pair': 'EUR_CHF', 'num_trades': 148, 'total_gain': 137.59999999997768, 'mean_gain': 0.9360544217685557, 'min_gain': -43.50000000000076, 'max_gain': 211.59999999999846, 'mashort': 8, 'malong': 32}, 

{'pair': 'EUR_CHF', 'num_trades': 128, 'total_gain': 202.2000000000123, 'mean_gain': 1.5921259842520654, 'min_gain': -44.39999999999999, 'max_gain': 207.9999999999993, 'mashort': 16, 'malong': 32},
....

]
```

---

## 2021.09.20 在 excel 上畫出交易圖

參考資料: [The Chart Class — XlsxWriter Documentation](https://xlsxwriter.readthedocs.io/chart.html)

## 2021.09.26 dt.utcnow() 無法回傳正確時區問題

[參考資料](https://stackoverflow.com/questions/2331592/why-does-datetime-datetime-utcnow-not-contain-timezone-information)

[參考資料 2](https://stackoverflow.com/questions/35462876/python-pytz-timezone-function-returns-a-timezone-that-is-off-by-9-minutes)

