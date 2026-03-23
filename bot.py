import os
import time
import uuid
import requests

TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    raise ValueError("TOKEN environment variable is missing")

BASE_URL = f"https://api.telegram.org/bot{TOKEN}"
SUPPORT_USERNAME = "@Natar100"
STARS_PRICE = 4000

KEYBOARD = {
    "keyboard": [
        [{"text": "خرید با کریپتو"}, {"text": "خرید با Stars"}],
        [{"text": "خرید VPN"}],
        [{"text": "پشتیبانی"}]
    ],
    "resize_keyboard": True
}

user_mode = {}


def tg_post(method: str, data: dict):
    r = requests.post(f"{BASE_URL}/{method}", json=data, timeout=30)
    r.raise_for_status()
    return r.json()


def tg_get(method: str, params=None):
    r = requests.get(f"{BASE_URL}/{method}", params=params or {}, timeout=70)
    r.raise_for_status()
    return r.json()


def send_message(chat_id: int, text: str, reply_markup=None):
    payload = {"chat_id": chat_id, "text": text}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    tg_post("sendMessage", payload)


def send_invoice(chat_id: int, user_id: int):
    payload = f"vpn_{user_id}_{uuid.uuid4().hex[:8]}"
    tg_post("sendInvoice", {
        "chat_id": chat_id,
        "title": "Iran AnyConnect - 1 Month",
        "description": "اشتراک 1 ماهه دو کاربره AnyConnect - حجم نامحدود",
        "payload": payload,
        "provider_token": "",
        "currency": "XTR",
        "prices": [
            {"label": "VPN 1 Month - 2 Users", "amount": STARS_PRICE}
        ]
    })


def answer_pre_checkout_query(query_id: str):
    tg_post("answerPreCheckoutQuery", {
        "pre_checkout_query_id": query_id,
        "ok": True
    })


def normalize_text(text: str) -> str:
    return (text or "").strip()


def handle_message(message: dict):
    chat_id = message["chat"]["id"]
    user_id = message.get("from", {}).get("id", 0)
    text = normalize_text(message.get("text", ""))

    if "successful_payment" in message:
        payment = message["successful_payment"]
        send_message(
            chat_id,
            f"""✅ پرداخت با موفقیت انجام شد.

🔐 پلن خریداری‌شده: AnyConnect دو کاربره
📅 مدت: 1 ماهه
⚡ حجم: نامحدود
💰 مبلغ: {payment.get('total_amount')} Stars

📩 حالا برای دریافت اکانت به پشتیبانی پیام دهید:
{SUPPORT_USERNAME}""",
            reply_markup=KEYBOARD
        )
        return

    if text == "/start":
        user_mode.pop(user_id, None)
        send_message(
            chat_id,
            """🔥 به ربات Iran AnyConnect خوش اومدی

اول روش خریدت رو انتخاب کن:""",
            reply_markup=KEYBOARD
        )

    elif text == "خرید با کریپتو":
        user_mode[user_id] = "crypto"
        send_message(
            chat_id,
            """💳 پرداخت با کریپتو انتخاب شد.
حالا روی «خرید VPN» بزن.""",
            reply_markup=KEYBOARD
        )

    elif text == "خرید با Stars":
        user_mode[user_id] = "stars"
        send_message(
            chat_id,
            """⭐️ پرداخت با Stars انتخاب شد.
حالا روی «خرید VPN» بزن.""",
            reply_markup=KEYBOARD
        )

    elif text == "خرید VPN":
        mode = user_mode.get(user_id)

        if mode == "stars":
            send_invoice(chat_id, user_id)

        elif mode == "crypto":
            send_message(
                chat_id,
                f"""🔐 اشتراک AnyConnect دو کاربره

📅 مدت: 1 ماهه
⚡ حجم: نامحدود
💰 قیمت: 12,000,000 تومان

💳 پرداخت فقط با ارز دیجیتال
📩 برای پرداخت با پشتیبانی هماهنگ کنید:
{SUPPORT_USERNAME}""",
                reply_markup=KEYBOARD
            )

        else:
            send_message(
                chat_id,
                """اول روش خریدت رو انتخاب کن:
«خرید با کریپتو» یا «خرید با Stars»""",
                reply_markup=KEYBOARD
            )

    elif text == "پشتیبانی":
        send_message(
            chat_id,
            f"📩 {SUPPORT_USERNAME}",
            reply_markup=KEYBOARD
        )

    else:
        send_message(
            chat_id,
            "یکی از دکمه‌ها را انتخاب کن.",
            reply_markup=KEYBOARD
        )


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
            if offset is not None:
                params["offset"] = offset

            data = tg_get("getUpdates", params)
            if data.get("ok"):
                for update in data.get("result", []):
                    offset = update["update_id"] + 1
                    handle_update(update)

        except Exception as e:
            print("Error:", e)
            time.sleep(5)


if __name__ == "__main__":
    main()
