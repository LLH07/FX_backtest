# 2021.09.21 parse utc time
import datetime as dt
from dateutil.parser import *

def get_his_data_filename(pair, granularity):
    return f'his_data\{pair}_{granularity}.pkl'

def get_instruments_data_filename():
    return 'instruments.pkl'

# 2021.09.21 取得目前 utc 時間並在其後增加 utc 時區
def time_utc():
    return dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc)

# 2021.09.21 將字串轉為時間 datetime 
def get_utc_dt_from_string(data_str):
    d = parse(data_str)
    return d.replace(tzinfo=dt.timezone.utc)

if __name__ == "__main__":
    print(get_his_data_filename("EUR_USD", "H1"))
    print(get_instruments_data_filename())
    print(dt.datetime.utcnow())
    print(time_utc())
    print(get_utc_dt_from_string('2021-09-21 20:00:00'))