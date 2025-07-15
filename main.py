import requests
import time
import datetime

# Telegram Bot Setup
BOT_TOKEN = "8076273330:AAHspKk3po_YKOuxPhgBqOwQBJGQfzX_Gec"
CHAT_ID = "7663076151"
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# Alert Settings
plan_a_targets = {
    "btc": {"price": (100000, 103000), "rsi": 35},
    "arb": {"price": (0.30, 0.35), "rsi": 35},
    "aero": {"price": (0.65, 0.75), "rsi": 35},
    "stx": {"price": (0.55, 0.65), "rsi": 35},
    "ondo": {"price": (0.65, 0.75), "rsi": 35},
}
plan_b_targets = {
    "btc": 113000,
    "arb": {"price": (0.38, 0.42), "rsi": 55},
    "aero": {"price": (0.90, 1.00), "rsi": 55},
    "stx": {"price": (0.80, 0.90), "rsi": 55},
    "ondo": {"price": (0.95, 1.10), "rsi": 55},
}

allocations = {
    "arb": "20%",
    "aero": "20%",
    "stx": "20%",
    "ondo": "40%",
}

# Simulated price + RSI fetcher
def get_market_data():
    return {
        "btc": {"price": 120122, "rsi": 45},
        "arb": {"price": 0.4116, "rsi": 36.7},
        "aero": {"price": 0.92, "rsi": 48},
        "stx": {"price": 0.84, "rsi": 49},
        "ondo": {"price": 0.98, "rsi": 50},
        "cpi_soft": True
    }

# Send Telegram message
def send_alert(message):
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(TELEGRAM_API, data=payload)

# Check for valid entry
def check_signals():
    data = get_market_data()
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    btc_price = data["btc"]["price"]
    btc_rsi = data["btc"]["rsi"]
    cpi_ok = data["cpi_soft"]

    for coin in ["arb", "aero", "stx", "ondo"]:
        price = data[coin]["price"]
        rsi = data[coin]["rsi"]

        # PLAN A CONDITIONS
        if plan_a_targets["btc"]["price"][0] <= btc_price <= plan_a_targets["btc"]["price"][1] and btc_rsi < plan_a_targets["btc"]["rsi"]:
            if plan_a_targets[coin]["price"][0] <= price <= plan_a_targets[coin]["price"][1] and rsi < plan_a_targets[coin]["rsi"]:
                msg = f"🔻 *PLAN A BUY — {coin.upper()}*\n" \
                      f"• Price: ${price:.4f} (target {plan_a_targets[coin]['price'][0]}–{plan_a_targets[coin]['price'][1]})\n" \
                      f"• 4H RSI: {rsi}\n" \
                      f"• BTC: ${btc_price} (RSI {btc_rsi})\n" \
                      f"• Time: {now}\n\n" \
                      f"*Ideal entry triggered. Execute your full allocation now.* 💰"
                send_alert(msg)

        # PLAN B CONDITIONS
        elif btc_price > plan_b_targets["btc"] and price >= plan_b_targets[coin]["price"][0] and price <= plan_b_targets[coin]["price"][1] and rsi < plan_b_targets[coin]["rsi"] and cpi_ok:
            msg = f"🔔 *BUY SIGNAL — {coin.upper()}*\n" \
                  f"• Price: ${price:.4f} (zone {plan_b_targets[coin]['price'][0]}–{plan_b_targets[coin]['price'][1]})\n" \
                  f"• 4H RSI: {rsi}\n" \
                  f"• BTC: ${btc_price}  (Plan B)\n" \
                  f"• CPI soft: ✅\n" \
                  f"• Time: {now}\n\n" \
                  f"All conditions met → *High-confidence entry.*\nExecute your full allocation now. 📈"
            send_alert(msg)

# Repeat every 5 mins
while True:
    check_signals()
    time.sleep(300)  # 5 minutes
