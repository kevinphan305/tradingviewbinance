print("API KEY:", os.environ.get("BINANCE_API_KEY"))
print("SECRET KEY:", os.environ.get("BINANCE_SECRET_KEY"))
print("TESTNET:", os.environ.get("USE_TESTNET"))

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

symbols = ["AVAXUSDT", "XRPUSDT", "SOLUSDT", "ADAUSDT", "LINKUSDT", "LTCUSDT", "DOTUSDT", "DOGEUSDT"]


def get_price(sym):
    symbol = str(sym).strip().upper()
    return client.get_symbol_ticker(symbol=symbol)

if __name__ == "__main__":
    while True:
        for sym in symbols:
            try:
                ticker = get_price(sym)
                price  = ticker["price"]
                logging.info(f"{sym}: {price}")      # <── ghi log
                print(f"{sym}: {price}")             # (giữ lại để xem trực tiếp)
            except Exception as e:
                logging.error(f"Lỗi lấy giá {sym}: {e}")  # <── ghi lỗi
                print(f"❌ Lỗi lấy giá {sym}: {e}")
        time.sleep(3)

