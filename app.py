from flask import Flask, request, jsonify
from binance.client import Client
from binance.enums import *
from dotenv import load_dotenv          # NEW
import os, logging, math

# ---------- cấu hình logging ----------
logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,                 # sẽ thấy cả INFO
    format="%(asctime)s - %(levelname)s - %(message)s"
)

load_dotenv()                           # NEW – nạp .env

app = Flask(__name__)

API_KEY    = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_SECRET_KEY")
ALERT_KEY  = os.getenv("ALERT_KEY", "123456")   # trùng trong alert
USE_TEST   = os.getenv("USE_TESTNET", "false").lower() == "true"

client = Client(API_KEY, API_SECRET, testnet=USE_TEST)
client.FUTURES_BASE_URL = (
    "https://testnet.binancefuture.com" if USE_TEST else "https://fapi.binance.com"
)

# ---------- endpoint nhận TradingView ----------
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    logging.info(f"Received alert: {data}")
    print("⌨️  Alert:", data)           # in thẳng ra console để dễ thấy

    # 1) bảo mật
    if data.get("key") != ALERT_KEY:
        return jsonify({"error": "wrong key"}), 403

    symbol = data["symbol"].upper()
    side   = data["side"].upper()                  # BUY / SELL
    usdt   = float(data["usdt_size"])              # số USDT muốn vào lệnh
    order_type = FUTURE_ORDER_TYPE_MARKET          # luôn MARKET

    # 2) chuyển USDT → quantity
    price = float(client.futures_symbol_ticker(symbol=symbol)["price"])
    step  = float(
        next(f["stepSize"]                         # filter LOT_SIZE
             for f in client.futures_exchange_info(symbol=symbol)["filters"]
             if f["filterType"] == "LOT_SIZE")
    )
    qty = math.floor((usdt / price) / step) * step
    if qty <= 0:
        return jsonify({"error": "qty too small"}), 400

    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type=order_type,
            quantity=str(qty)                      # phải là str nếu dùng python‑binance < 1.0
        )
        logging.info(f"Order OK: {order['orderId']}")
        print("✅ Order placed:", order["orderId"])
        return jsonify({"status": "filled", "qty": qty}), 200

    except Exception as e:
        logging.error(f"Order error: {e}")
        print("❌ Order error:", e)
        return jsonify({"error": str(e)}), 400

# ---------- (tuỳ chọn) luồng lấy giá ----------
if __name__ == "__main__":
    import threading, time
    symbols = ["AVAXUSDT", "XRPUSDT", "SOLUSDT","LINKUSDT","DOGEUSDT","SUIUSDT" ]
    def price_loop():
        while True:
            for s in symbols:
                try:
                    p = client.futures_symbol_ticker(symbol=s)["price"]
                    logging.info(f"{s}: {p}")
                    print(f"{s}: {p}")
                except Exception as e:
                    logging.error(f"Price error {s}: {e}")
            time.sleep(3)

    threading.Thread(target=price_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
