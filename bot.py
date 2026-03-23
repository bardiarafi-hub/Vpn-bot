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
            "✅ پرداخت با موفقیت انجام شد.\n\n"
            "🔐 پلن
