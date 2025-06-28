import pandas as pd

def convert_to_meta5_format(df):
    # تغییر نام انگلیسی ستون‌ها در صورت وجود
    df = df.rename(columns={
        'date': 'datetime',
        'open': 'open',
        'high': 'high',
        'low': 'low',
        'close': 'close',
        'volume': 'volume',
        'tick volume': 'tick volume',
        'Spread': 'Spread'
    })
    # ایجاد ستون‌های اضافی پیش از انتخاب
    df["tick volume"] = df["volume"]
    df["Spread"] = '007'  # مقدار دلخواه برای اسپرد

    # زمان رو فرمت‌ میلی‌ثانیه نمایش میدم
    df['datetime'] = df['datetime'].dt.strftime('%d.%m.%Y %H:%M:%S.%f').str.slice(0, -3)

    # انتخاب فقط ستون‌های مورد نظر
    df = df[['datetime', 'open', 'high', 'low', 'close', 'volume', 'tick volume' , 'Spread']] #, 'Volume Tick' , 'Spread'
    df["tick volume"] = df["volume"]
    df["Spread"] = 8

    return df
