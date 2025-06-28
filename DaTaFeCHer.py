"""import os.path
from SavePartialData import *
from ib_insync import *
import pandas as pd
from Configs import *
from datetime import datetime, timezone, timedelta
import time

MaxDuration = 20 #int(input("📅 Enter the Number of Months to Fetch: ").strip())

# زمان فعلی UTC با تایم‌زون درست
today = datetime.utcnow().replace(tzinfo=timezone.utc)

# شروع بازه زمانی مشخص
start = datetime(2024, 6, 17, tzinfo=timezone.utc)
end = today

# محاسبه اختلاف زمانی
delta_Time = end - start

delta_day =  int((end - start).total_seconds() // 86400)
RequestNumber_day = int(delta_day // MaxDuration)

print("Today UTC Time is  : " , today)

print("\nstart Time by UTCTime is  : " , start)
print("end Time is  :", end)

print("\ndelta_Time  is :" , delta_Time)
print("delta_day  is  :  " , delta_day)
print("MaxDuration is  :" , MaxDuration)
print("\nRequestNumber_day  :" , RequestNumber_day)


# ساخت شیء اصلی ارتباط با IB
ib = IB()


def Connect_With_IB():
    ib.connect("127.0.0.1", port=7497, clientId=1)
    # اگر بلافاصله بعد از دادن دستور اتصال،
    # درخواست دیتا بدی، ممکنه اتصال هنوز کامل آماده نباشه.....واسه اینکه رکوئست تاخیر بخوره سر هم نباشن و ban نشه
    time.sleep(1)


def Disconnect_With_IB():
    ib.disconnect()

def safe_Connect(max_Retries = 5 , delay = 5):
    for i in range(max_Retries):
        try:
            if not ib.isConnected():
                ib.connect(host= '127.0.0.1' , port= 7494 , clientid= 1)
                time.sleep(1)
            return
        except Exception as e:
            print(f" ❌❌❌ اتصال ناموفق، تلاش مجدد ({attempt + 1}/{max_retries}  )... خطا: {e}")
            time.sleep(delay)
    raise ConnectionError("🚫 اتصال به IB پس از چند تلاش ناموفق بود.")


def get_contract():
    return Contract(
        symbol= SYMBOL,
        secType= SECURITY_TYPE_STK,
        exchange= EXCHANGE,
        primaryExchange= 'NASDAQ',
        currency= CURRENCY
    )


def get_MaxDuration(bar_size):
    if bar_size == '1 sec':
        return '1800 S'   # 30 دقیقه
    elif bar_size == '1 min':
        return '30 D'     # حداکثر 30 روز
    elif bar_size == '5 mins':
        return '60 D'     # برای بارهای بزرگ‌تر
    else:
        return '20 D'      # پیش‌فرض



def fetch_data_Reconnect(timeframe, PRICE_TYPE_Trade , MaxDuration):
    contract = get_contract()
    all_data = []

    #print("⏰ Current UTC Time is : ", today)
    print(f"\n🕒 delta_day or Total Days: {delta_day:.1f}, Request Count: {RequestNumber_day}")

    duration = get_MaxDuration(timeframe)
    # حلقه‌ی گرفتن دیتای سیمبل مدنظرم از IB Broker در چند Chunk
    current_end_date = today
    chunk_end = today
#   if chunk_end > start:
    for i in range(RequestNumber_day):
        chunk_end = today - timedelta(days=i * MaxDuration)
        chunk_end_str = (today - timedelta(days=i * MaxDuration)).strftime('%Y%m%d %H:%M:%S')

        # محاسبه تاریخ پایان chunk
        chunk_start = chunk_end - timedelta(days=MaxDuration)
        end_str = current_end_date.strftime('%Y%m%d %H:%M:%S')

        print("🕓 TimeFrame is : ", timeframe)
        print("🕓 DurationStr is : ", duration)
        print(f"\n🔄 Chunk {i + 1}/{RequestNumber_day}")
        print(f"⏳ Chunk Range --> chunk_start: {chunk_start}   to chunk_end: {chunk_end}")
        #print(f"📤 Fetching data ending at :  {chunk_end}")

        try:
            bars = ib.reqHistoricalData(
                contract=contract,
                endDateTime=end_str,
                durationStr=duration,
                barSizeSetting=timeframe,
                whatToShow=PRICE_TYPE_Trade,
                useRTH=False,
                formatDate=1
            )
        except Exception as e:
            return e

        if not bars:
            print("⚠️ No bars received Iman. Breaking loop.")
            break

        df = util.df(bars)
        all_data.append(df)

        if not df.empty:
            current_end_date = df['date'].min() - timedelta(seconds=1)
        else:
            current_end_date = current_end_date - timedelta(days=MaxDuration)
        time.sleep(1.5)  # تاخیر 1.5 ثانیه ای در ارسال درخواست بعدی جهت جلوگیری از محدودیت API


    def save_partial_data(all_data, file_name='temp_backup.csv'):
        try:
            df_all = pd.concat(all_data)
            df_all.drop_duplicates(subset='date', inplace=True)
            df_all.to_csv(file_name, index=False)
            print(f"💾 فایل موقتی ذخیره شد: {file_name}")
        except Exception as e:
            print(f"⚠️ خطا در ذخیره‌سازی فایل موقتی: {e}")


    if not all_data:
        print("⚠️ No data collected at all.")
        return pd.DataFrame()

    # ادغام داده‌ها و تمیزکاری
    full_df = pd.concat(all_data)
    full_df.drop_duplicates(subset='date', inplace=True)
    full_df.sort_values(by='date', inplace=True)
    full_df.reset_index(drop=True, inplace=True)
    return full_df


#def Reconnect():
if os.path.exists(Myfilename):
    with open(Myfilename , r) as f:
        file = csv.load(f)
    if e:
        print("Data is Completed...")
    else:
        Connect_With_IB()

#fetch_data_for_1_month(timeframe = '1 min', PRICE_TYPE_Trade = 'TRADES' , MaxDuration=30)
"""

import os
import pandas as pd
import time
from ib_insync import *
from datetime import datetime, timezone, timedelta
from SavePartialData import *
from Configs import *

# اتصال به IB
ib = IB()


def safe_connect(max_retries=5, delay=5):
    for attempt in range(max_retries):
        try:
            if not ib.isConnected():
                ib.connect('127.0.0.1', 7497, clientId=1)
                time.sleep(1.5)
            return True
        except Exception as e:
            print(f" ❌❌❌ تلاش برای اتصال ({attempt + 1}/{max_retries}) ناموفق بود.  خطا :  {e}")
            time.sleep(delay)
    raise ConnectionError("🚫 اتصال به IB پس از چند تلاش ناموفق بود.")


def get_contract():
    return Contract(
        symbol=SYMBOL,
        secType=SECURITY_TYPE_STK,
        exchange=EXCHANGE,
        primaryExchange='NASDAQ',
        currency=CURRENCY
    )


def get_MaxDuration(bar_size):
    if bar_size == '1 sec':
        return '1800 S'
    elif bar_size == '1 min':
        return '30 D'
    elif bar_size == '5 mins':
        return '60 D'
    else:
        return '20 D'


def fetch_data_Reconnect(timeframe, PRICE_TYPE_Trade, MaxDuration):
    contract = get_contract()
    all_data = []

    today = datetime.utcnow().replace(tzinfo=timezone.utc)
    start = datetime(2024, 6, 17, tzinfo=timezone.utc)
    delta_day = int((today - start).total_seconds() // 86400)
    RequestNumber_day = delta_day // MaxDuration

    print(f"\n🔁 It is Fetching Data from startTime: {start} time to Endtime: {today}  | Total Days: {delta_day}, Requests: {RequestNumber_day}")
    current_end_date = today
    duration = get_MaxDuration(timeframe)

    for i in range(RequestNumber_day):
        chunk_end = today - timedelta(days=i * MaxDuration)
        chunk_start = chunk_end - timedelta(days=MaxDuration)
        end_str = current_end_date.strftime('%Y%m%d %H:%M:%S')

        print(f"\n🔄 Chunk {i + 1}/{RequestNumber_day}")
        print(f"⏳ Range: {chunk_start} to {chunk_end}")

        try:
            if not ib.isConnected():
                safe_connect()
            bars = ib.reqHistoricalData(
                contract=contract,
                endDateTime=end_str,
                durationStr=duration,
                barSizeSetting=timeframe,
                whatToShow=PRICE_TYPE_Trade,
                useRTH=False,
                formatDate=1
            )
        except Exception as e:
            print(f"⚠️ خطا هنگام دریافت دیتا: {e}")
            time.sleep(3)
            continue

        if not bars:
            print("⚠️ No bars received. Breaking loop.")
            break

        df = util.df(bars)
        all_data.append(df)

        if not df.empty:
            current_end_date = df['date'].min() - timedelta(seconds=1)
        else:
            current_end_date = current_end_date - timedelta(days=MaxDuration)

        time.sleep(1.5)

    if not all_data:
        print("⚠️ No data collected.")
        return pd.DataFrame()

    df_all = pd.concat(all_data)
    df_all.drop_duplicates(subset='date', inplace=True)
    df_all.sort_values(by='date', inplace=True)
    df_all.reset_index(drop=True, inplace=True)
    return df_all


# ========== MAIN ==========
if __name__ == "__main__":
    safe_connect()
    timeframe = '1 min'
    PRICE_TYPE_Trade = 'TRADES'
    MaxDuration = 20

    df = fetch_data_Reconnect(timeframe, PRICE_TYPE_Trade, MaxDuration)

    if not df.empty:
        filename = "output_data.csv"
        df.to_csv(filename, index=False)
        print(f"\n✅ دیتا با موفقیت ذخیره شد: {filename}")
    else:
        print("🚫 دیتایی برای ذخیره وجود نداشت.")
