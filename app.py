import os, time, logging
from dotenv import load_dotenv          # ← nạp .env
from binance.client import Client

# ── cấu hình ghi log ra bot.log ──────────────────────────
logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
# ─────────────────────────────────────────────────────────

load_dotenv()                           # ← đọc BINANCE_API_KEY, BINANCE_SECRET_KEY

api_key    = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_SECRET_KEY")

client = Client(api_key, api_secret)

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
