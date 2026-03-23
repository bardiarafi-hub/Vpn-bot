import os
import time
import uuid
import requests

TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    raise ValueError("TOKEN environment variable is missing")

BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

SUPPORT_USERNAME = "@Natar100"

# ⭐ قیمت نهایی
STARS_PRICE = 4000

PRODUCT_TITLE = "Iran AnyConnect - 1 Month"
PRODUCT_DESC = "AnyConnect یک ماهه، حجم نامحدود"

KEYBOARD = {
    "keyboard": [
        [{"text": "خرید با کریپتو"}, {"text": "خرید با Stars"}],
        [{"text": "پشتیبانی"}]
    ],
    "resize_keyboard": True
}


def tg_post(method: str, data: dict):
    url = f"{BASE_URL}/{method}"
    r = requests.post(url, json=data, timeout=30)
    r.raise_for_status()
    return r.json()


def tg_get(method: str, params: dict | None = None):
    url = f"{BASE_URL}/{method}"
    r = requests.get(url, params=params or {}, timeout=70)
    r.raise_for_status()
    return r.json()


def send_message(chat_id: int, text: str, reply_markup=None):
    payload = {
        "chat_id": chat_id,
        "text": text,
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    tg_post("sendMessage", payload)


def answer_pre_checkout_query(query_id: str):
    tg_post("answerPreCheckoutQuery", {
        "pre_checkout_query_id": query_id,
        "ok": True
    })


def send_stars_invoice(chat_id: int, user_id: int):
    payload = f"vpn_{user_id}_{uuid.uuid4().hex[:8]}"

    tg_post("sendInvoice", {
        "chat_id": chat_id,
        "title": PRODUCT_TITLE,
        "description": PRODUCT_DESC,
        "payload": payload,
        "provider_token": "",
        "currency": "XTR",
        "prices": [
            {
                "label": "VPN 1 Month",
                "amount": STARS_PRICE
            }
        ]
    })


def handle_message(message: dict):
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    # ✅ بعد از پرداخت
    if "successful_payment" in message:
        payment = message["successful_payment"]

        send_message(
            chat_id,
            "✅ پرداخت با Stars انجام شد!\n\n"
            f"💰 مبلغ: {payment['total_amount']} Stars\n"
            f"🧾 کد سفارش: {payment['invoice_payload']}\n\n"
            f"📩 برای دریافت اکانت به پشتیبانی پیام بده:\n{SUPPORT_USERNAME}",
            reply_markup=KEYBOARD
        )
        return

    if text == "/start":
        send_message(
            chat_id,
            "🔥 Iran AnyConnect\n\nروش خرید رو انتخاب کن:",
            reply_markup=KEYBOARD
        )

    elif text == "خرید با کریپتو":
        send_message(
            chat_id,
            "🔐 اشتراک AnyConnect\n\n"
            "📅 1 ماهه\n"
            "⚡ نامحدود\n"
            "💰 12,000,000 تومان\n\n"
            "💳 پرداخت: ارز دیجیتال\n"
            f"📩 پیام بده:\n{SUPPORT_USERNAME}",
            reply_markup=KEYBOARD
        )

    elif text == "خرید با Stars":
        send_stars_invoice(chat_id, message["from"]["id"])

    elif text == "پشتیبانی":
        send_message(chat_id, f"{SUPPORT_USERNAME}", reply_markup=KEYBOARD)

    else:
        send_message(chat_id, "یکی از گزینه‌ها رو انتخاب کن", reply_markup=KEYBOARD)


def handle_update(update: dict):
    if "pre_checkout_query" in update:
        answer_pre_checkout_query(update["pre_checkout_query"]["id"])
        return

    if "message" in update:
        handle_message(update["message"])


def main():
    offset = None

    while True:
        try:
            params = {"timeout": 60}
            if offset:
                params["offset"] = offset

            res = tg_get("getUpdates", params)

            for upd in res.get("result", []):
                offset = upd["update_id"] + 1
                handle_update(upd)

        except Exception as e:
            print("Error:", e)
            time.sleep(5)


if __name__ == "__main__":
    main()
