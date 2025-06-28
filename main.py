from DaTaFeCHer import *
from Configs import *
from Formattering import convert_to_meta5_format
from Utilities import save_dataframe_to_csv
import pandas as pd
from ib_insync import util


def RunProject():
    # اتصال به Interactive Brokers
    Connect_With_IB()

    try:
        # گرفتن تعداد ماه‌ها از کاربر
        #number_month = int(input("📅 Enter the Number of Months to Fetch: ").strip())
        #MaxDuration = int(input("📅 Enter the Number of Months to Fetch: ").strip())

        for timeframe_key, timeframe_value in TIMEFRAME_1M.items():
            PRICE_TYPE = PRICE_TYPE_Trade
            #print(f"\n🔁 Fetching {number_month} months of data for '{SYMBOL}' [{PRICE_TYPE}] @ {timeframe_key}")
            print(f"\n🔁 Fetching {MaxDuration} days to ego from end... data for '{SYMBOL}' [{PRICE_TYPE}] @ {timeframe_key}")
            # دریافت داده
            #df = fetch_data_for_1_month(timeframe_value, PRICE_TYPE, number_month)
            df = fetch_data_Reconnect(timeframe_value, PRICE_TYPE, MaxDuration)

            if df.empty:
                print(f"⚠️ No data received for {SYMBOL} [{PRICE_TYPE}] @ {timeframe_key}")
                continue

            # تبدیل به فرمت متاتریدر 5
            formatted = convert_to_meta5_format(df)

            # ذخیره فایل CSV
            #Myfilename = f"{SYMBOL}_{PRICE_TYPE}_{timeframe_key}_{number_month}months.csv"
            Myfilename = f"{SYMBOL}_{PRICE_TYPE}_{timeframe_key}_MaxDuration{MaxDuration}days.csv"
            save_dataframe_to_csv(formatted, Myfilename)

            print(f"✅ Data saved successfully: {Myfilename}")

    except ValueError:
        print("❌ Invalid input! Please enter a valid number.")
    except Exception as e:
        print(f"❌ Unexpected error occurred: {e}")
    finally:
        # قطع ارتباط
        Disconnect_With_IB()
        print("🔌 Disconnected from IB")


if __name__ == '__main__':
    RunProject()