
# پارامترهای ثابتمون اینا باید باشن
SYMBOL = 'AAPL'
SECURITY_TYPE_CDF = 'CDF'
SECURITY_TYPE_STK = 'STK'
EXCHANGE = 'SMART'
CURRENCY = 'USD'
TIMEZONE = 'GMT'


# تریدز قیمتیه که واقعا اون سهام یا طلا یا نفت خرید و فروش میشه و بید قیمتی هستش که
# خریدار حاضره بالاترین پیشنهاد پرداخت رو بده و اسک قیمتیه که فروشنده حاضره بعنوان کمترین قیمت بفروش برسونه
PRICE_TYPE_Trade = 'TRADES'
PRICE_TYPE_Bid   = 'BID'
PRICE_TYPE_Ask   = 'ASK'

TIMEFRAME_1M = {
    "1m": "1 min"
}

TIMEFRAME_1H = {
    "60m" : "1 hour"
}

# تایم فریم فقط یک ثانیه
TIMEFRAME_1S = {
    "1s" : "1 secs"
}

# تایم فریم از یک ثانیه تا 43200 دقیقه معادل یک ماه
TIMEFRAMES_all = {
    "1s" : "1 secs",
    "1m" : "1 min",
    "5m" : "5 mins",
    "15m" : "15 mins",
    "30m" : "30 mins",
    "60m" : "1 hour",
    "240m" : "4 hours",
    "1440m" : "1 day",
    "10080m" : "1W",
    "43200m" : "1M"
}
