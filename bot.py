import os
import time
import requests

TOKEN = os.environ.get("TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

KEYBOARD = {
    "keyboard": [
        [{"text": "خرید VPN"}, {"text": "پشتیبانی"}]
    ],
    "resize_keyboard": True
}

def send_message(chat_id, text, reply_markup=None):
    data = {
        "chat_id": chat_id,
        "text": text,
    }
    if reply_markup:
        data["reply_markup"] = reply_markup
    requests.post(f"{BASE_URL}/sendMessage", json=data, timeout=30)

def handle_message(message):
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text == "/start":
        send_message(chat_id, "به ربات فروش خوش اومدی 🔥", reply_markup=KEYBOARD)

    elif text == "خرید VPN":
        send_message(
            chat_id,
            "🔐 اشتراک AnyConnect\n\n"
            "📅 مدت: 1 ماهه\n"
            "⚡ حجم: نامحدود\n"
            "💰 قیمت: 12,000,000 تومان\n\n"
            "💳 پرداخت فقط با ارز دیجیتال\n"
            "📩 برای پرداخت با پشتیبانی هماهنگ کنید:\n"
            "@Natar100"
        )

    elif text == "پشتیبانی":
        send_message(chat_id, "آیدی پشتیبانی: @Natar100")

    else:
        send_message(chat_id, "یکی از دکمه‌ها را انتخاب کن.", reply_markup=KEYBOARD)

def main():
    if not TOKEN:
        raise ValueError("TOKEN environment variable is missing")

    offset = None

    while True:
        try:
            params = {"timeout": 60}
            if offset is not None:
                params["offset"] = offset

            response = requests.get(f"{BASE_URL}/getUpdates", params=params, timeout=70)
            response.raise_for_status()
            data = response.json()

            if data.get("ok"):
                for update in data.get("result", []):
                    offset = update["update_id"] + 1
                    if "message" in update:
                        handle_message(update["message"])

        except Exception as e:
            print("Error:", e)
            time.sleep(5)

if __name__ == "__main__":
    main()
