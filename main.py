import requests
import time
from datetime import datetime

# === CONFIGURATION ===
BOT_TOKEN = '8076273330:AAHspKk3po_YKOuxPhgBqOwQBJGQfzX_Gec'
CHAT_ID = '7663076151'

# Price + RSI values (you can later pull live data from APIs if needed)
coins = {
    'arb': {'price': 0.4116, 'rsi': 36.7, 'zone': (0.38, 0.42)},
    'aero': {'price': 0.92, 'rsi': 40.3, 'zone': (0.90, 1.00)},
    'stx': {'price': 0.86, 'rsi': 43.2, 'zone': (0.80, 0.90)},
    'ondo': {'price': 1.01, 'rsi': 45.9, 'zone': (0.95, 1.10)},
}

btc_price = 120122
btc_plan = "Plan B" if btc_price > 113000 else "Plan A"
cpi_soft = True

# === ALERT LOGIC ===
def send_alert(coin, data):
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
    price = data['price']
    rsi = data['rsi']
    low, high = data['zone']

    if low <= price <= high and rsi < 55 and btc_plan == "Plan B" and cpi_soft:
        message = (
            f"🔔 **BUY SIGNAL — {coin.upper()}**\n"
            f"• Price: ${price:.4f} (zone {low}-{high})\n"
            f"• 4H RSI: {rsi}\n"
            f"• BTC: ${btc_price}  ({btc_plan})\n"
            f"• CPI soft: ✅\n"
            f"• Time: {now}\n\n"
            f"All conditions met → **High-confidence entry**.\n"
            f"Execute your full allocation now. 📈"
        )
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})

# === LOOP (every 60 seconds for example) ===
while True:
    for coin, data in coins.items():
        send_alert(coin, data)
    time.sleep(60)
