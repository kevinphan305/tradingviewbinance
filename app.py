import logging

logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

from binance.client import Client
import os, time

api_key    = os.environ["BINANCE_API_KEY"]
api_secret = os.environ["BINANCE_SECRET_KEY"]

client = Client(api_key, api_secret)

# Danh sách cặp muốn lấy giá / trade
symbols = ["BTCUSDT", "AVAXUSDT", "XRPUSDT", "SOLUSDT", "ADAUSDT"]

def get_price(sym):
    # Làm sạch và bảo đảm là chuỗi in hoa
    symbol = str(sym).strip().upper()
    return client.get_symbol_ticker(symbol=symbol)

if __name__ == "__main__":
    while True:
        for sym in symbols:
            try:
                ticker = get_price(sym)
                print(f"{sym}: {ticker['price']}")
            except Exception as e:
                print(f"❌ Lỗi lấy giá {sym}: {e}")
        time.sleep(3)
