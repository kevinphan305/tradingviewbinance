from flask import Flask, request, jsonify
from binance.client import Client
import os, logging

app = Flask(__name__)

# --- nạp API key ---
api_key    = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_SECRET_KEY")
client     = Client(api_key, api_secret)

# --- endpoint nhận TradingView ---
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    logging.info(f"Received alert: {data}")

    # kiểm tra key bảo mật (nếu cần)
    if data.get("key") != os.getenv("ALERT_KEY"):
        return jsonify({"error": "wrong key"}), 403

    symbol  = data["symbol"].upper()
    side    = data["side"].upper()      # BUY / SELL
    order_type = data.get("type", "MARKET").upper()
    qty     = float(data["qty"])

    try:
        order = client.create_order(
            symbol=symbol,
            side=side,
            type=order_type,
            quantity=qty
        )
        logging.info(f"Order OK: {order}")
        return jsonify({"status": "filled"}), 200

    except Exception as e:
        logging.error(f"Order error: {e}")
        return jsonify({"error": str(e)}), 400

# --- chạy cả 2 chức năng trong cùng app ---
if __name__ == "__main__":
    # 1) bật luồng lấy giá (nếu vẫn muốn)
    import threading, time
    symbols = ["AVAXUSDT","XRPUSDT","SOLUSDT"]
    def price_loop():
        while True:
            for s in symbols:
                try:
                    p = client.get_symbol_ticker(symbol=s)["price"]
                    logging.info(f"{s}: {p}")
                except Exception as e:
                    logging.error(f"Lỗi giá {s}: {e}")
            time.sleep(3)

    threading.Thread(target=price_loop, daemon=True).start()

    # 2) chạy Flask ở cổng 80
    app.run(host="0.0.0.0", port=80)
