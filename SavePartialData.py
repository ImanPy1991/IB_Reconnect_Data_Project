import pandas as pd

def save_partial_data(all_data, file_name='temp_backup.csv'):
    try:
        df_all = pd.concat(all_data)
        df_all.drop_duplicates(subset='date', inplace=True)
        df_all.to_csv(file_name, index=False)
        print(f"💾 فایل موقتی ذخیره شد: {file_name}")
    except Exception as e:
        print(f"⚠️ خطا در ذخیره‌سازی فایل موقتی: {e}")