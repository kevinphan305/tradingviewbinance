import os
from binance.client import Client

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_SECRET_KEY")

client = Client(api_key, api_secret)

def get_price(symbol="AVAXUSDT,SOLUSDT,XRPUSDT,ADAUSDT,LINKUSDT,LTCUSDT,DOTUSDT,DOGEUSDT"):
    ticker = client.get_symbol_ticker(symbol=symbol)
    return ticker

if __name__ == "__main__":
    print(get_price())
