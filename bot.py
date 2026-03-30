import os
import time
import requests

TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    raise ValueError("TOKEN environment variable is missing")

BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

SUPPORT_USERNAME = os.environ.get("SUPPORT_USERNAME", "@Natar100")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID", "")
USDT_TRC20 = os.environ.get("USDT_TRC20", "SET_USDT_TRC20_ADDRESS")
USDT_ERC20 = os.environ.get("USDT_ERC20", "SET_USDT_ERC20_ADDRESS")
BTC_WALLET = os.environ.get("BTC_WALLET", "SET_BTC_ADDRESS")
ETH_WALLET = os.environ.get("ETH_WALLET", "SET_ETH_ADDRESS")

MAIN_MENU = "main"

WALLETS = {
    "USDT (TRC20)": USDT_TRC20,
    "USDT (ERC20)": USDT_ERC20,
    "BTC": BTC_WALLET,
    "ETH": ETH_WALLET,
}

user_state = {}


def tg_post(method: str, data: dict):
    r = requests.post(f"{BASE_URL}/{method}", json=data, timeout=30)
    r.raise_for_status()
    return r.json()


def tg_get(method: str, params=None):
    r = requests.get(f"{BASE_URL}/{method}", params=params or {}, timeout=70)
    r.raise_for_status()
    return r.json()


def send_message(chat_id: int, text: str, buttons=None):
    payload = {
        "chat_id": chat_id,
        "text": text,
    }
    if buttons:
        payload["reply_markup"] = make_keyboard(buttons)
    tg_post("sendMessage", payload)


def send_photo(chat_id: int, file_id: str, caption: str = ""):
    tg_post("sendPhoto", {
        "chat_id": chat_id,
        "photo": file_id,
        "caption": caption
    })


def make_keyboard(buttons):
    rows = []
    row = []
    for btn in buttons:
        row.append({"text": btn})
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)

    return {
        "keyboard": rows,
        "resize_keyboard": True
    }


def reset_user(chat_id: int):
    user_state[chat_id] = {
        "menu": MAIN_MENU,
        "selected_product": None,
        "selected_currency": None,
        "awaiting": None,
    }


def get_user(chat_id: int):
    if chat_id not in user_state:
        reset_user(chat_id)
    return user_state[chat_id]


CATALOG = {
    MAIN_MENU: {
        "title": "👋 مرحباً بك في NetArabia\nاختر القسم الذي تريده:",
        "buttons": [
            "اشتراكات ChatGPT",
            "إنشاء حسابات ChatGPT",
            "VPN",
            "Telegram Stars",
            "Apple iTunes",
            "PSN",
            "Steam",
            "Amazon",
            "Roblox",
            "الدعم"
        ],
    },

    "اشتراكات ChatGPT": {
        "title": "🤖 تجديد اشتراكات ChatGPT 5.4 (أحدث إصدار)\nاختر المنتج:",
        "buttons": [
            "ChatGPT Plus - 1 شهر - بدون تسجيل دخول - $12.5",
            "ChatGPT Plus - 12 شهر - بدون تسجيل دخول - $113",
            "ChatGPT Pro - 1 شهر - بدون تسجيل دخول - $158",
            "ChatGPT Plus - 1 شهر - مع تسجيل دخول - $8.5",
            "ChatGPT Plus - 12 شهر - مع تسجيل دخول - $99",
            "⬅️ رجوع"
        ],
    },

    "إنشاء حسابات ChatGPT": {
        "title": "🆕 إنشاء حساب ChatGPT 5.4 + اشتراك\nاختر المنتج:",
        "buttons": [
            "حساب جاهز ChatGPT Plus - 1 شهر - $10.5",
            "ChatGPT Plus على بريدك - 1 شهر - $17",
            "حساب جاهز ChatGPT Plus - 12 شهر - $98",
            "ChatGPT Plus على بريدك - 12 شهر - $118",
            "حساب جاهز ChatGPT Pro - 12 شهر - $442",
            "ChatGPT Pro على بريدك - 12 شهر - $476",
            "⬅️ رجوع"
        ],
    },

    "VPN": {
        "title": "🌐 خدمات VPN\nاختر النوع:",
        "buttons": [
            "WireGuard",
            "VLESS مع 10 مواقع IP",
            "⬅️ رجوع"
        ],
    },

    "WireGuard": {
        "title": "🌐 WireGuard\nاختر الخطة:",
        "buttons": [
            "WireGuard - 1 شهر - $5",
            "WireGuard - 3 أشهر - $9",
            "WireGuard - 6 أشهر - $16",
            "⬅️ رجوع"
        ],
    },

    "VLESS مع 10 مواقع IP": {
        "title": "🌐 VLESS مع 10 مواقع IP\nاختر الخطة:",
        "buttons": [
            "VLESS - 1 شهر - $6",
            "VLESS - 3 أشهر - $15",
            "⬅️ رجوع"
        ],
    },

    "Telegram Stars": {
        "title": "⭐ Telegram Stars (توصيل تلقائي)\nاختر الكمية:",
        "buttons": [
            "50 Stars - $1.5",
            "100 Stars - $3",
            "250 Stars - $6",
            "500 Stars - $11.5",
            "1000 Stars - $22",
            "2000 Stars - $40",
            "3000 Stars - $60",
            "5000 Stars - $90",
            "⬅️ رجوع"
        ],
    },

    "Apple iTunes": {
        "title": "🍎 Apple iTunes Gift Card\nاختر المنطقة:",
        "buttons": [
            "Apple iTunes - USA",
            "Apple iTunes - Saudi Arabia",
            "Apple iTunes - UAE",
            "⬅️ رجوع"
        ],
    },

    "Apple iTunes - USA": {
        "title": "🍎 Apple iTunes - الولايات المتحدة\nاختر البطاقة:",
        "buttons": [
            "Apple USA - $2 - $3",
            "Apple USA - $3 - $4",
            "Apple USA - $4 - $5.5",
            "Apple USA - $5 - $6.70",
            "Apple USA - $10 - $12",
            "Apple USA - $20 - $23",
            "Apple USA - $25 - $28.5",
            "Apple USA - $50 - $56.5",
            "Apple USA - $100 - $112",
            "Apple USA - $200 - $225",
            "Apple USA - $500 - $540",
            "⬅️ رجوع"
        ],
    },

    "Apple iTunes - Saudi Arabia": {
        "title": "🍎 Apple iTunes - السعودية\nاختر البطاقة:",
        "buttons": [
            "Apple KSA - 50 SAR - $16",
            "Apple KSA - 100 SAR - $32",
            "Apple KSA - 200 SAR - $62",
            "Apple KSA - 500 SAR - $150",
            "Apple KSA - 1000 SAR - $298",
            "⬅️ رجوع"
        ],
    },

    "Apple iTunes - UAE": {
        "title": "🍎 Apple iTunes - الإمارات\nاختر البطاقة:",
        "buttons": [
            "Apple UAE - 50 AED - $17.60",
            "Apple UAE - 100 AED - $35",
            "Apple UAE - 200 AED - $68",
            "Apple UAE - 500 AED - $166",
            "Apple UAE - 1000 AED - $327",
            "⬅️ رجوع"
        ],
    },

    "PSN": {
        "title": "🎮 PlayStation Gift Card\nاختر المنطقة:",
        "buttons": [
            "PSN - UAE",
            "PSN - USA",
            "⬅️ رجوع"
        ],
    },

    "PSN - UAE": {
        "title": "🎮 PSN - الإمارات\nاختر البطاقة:",
        "buttons": [
            "PSN UAE - $10 - $13",
            "PSN UAE - $20 - $25",
            "PSN UAE - $30 - $37",
            "PSN UAE - $50 - $57",
            "PSN UAE - $70 - $79",
            "PSN UAE - $100 - $108",
            "⬅️ رجوع"
        ],
    },

    "PSN - USA": {
        "title": "🎮 PSN - أمريكا\nاختر البطاقة:",
        "buttons": [
            "PSN USA - $10 - $15",
            "PSN USA - $20 - $30",
            "PSN USA - $50 - $70",
            "PSN USA - $100 - $130",
            "⬅️ رجوع"
        ],
    },

    "Steam": {
        "title": "🎮 Steam Gift Card\nاختر المنطقة:",
        "buttons": [
            "Steam - Saudi Arabia",
            "Steam - UAE",
            "⬅️ رجوع"
        ],
    },

    "Steam - Saudi Arabia": {
        "title": "🎮 Steam - السعودية\nاختر البطاقة:",
        "buttons": [
            "Steam KSA - 5 SAR - $3.5",
            "Steam KSA - 10 SAR - $6.5",
            "Steam KSA - 20 SAR - $11",
            "Steam KSA - 50 SAR - $22",
            "Steam KSA - 100 SAR - $40",
            "Steam KSA - 200 SAR - $64",
            "⬅️ رجوع"
        ],
    },

    "Steam - UAE": {
        "title": "🎮 Steam - الإمارات\nاختر البطاقة:",
        "buttons": [
            "Steam UAE - 1.40 AED - $1",
            "Steam UAE - 2.80 AED - $1.8",
            "Steam UAE - 18.60 AED - $7.5",
            "Steam UAE - 37.50 AED - $15",
            "Steam UAE - 46.80 AED - $18.5",
            "Steam UAE - 93.88 AED - $34.5",
            "Steam UAE - 140.80 AED - $51",
            "Steam UAE - 234.60 AED - $84",
            "Steam UAE - 469.40 AED - $166",
            "Steam UAE - 938.90 AED - $326",
            "⬅️ رجوع"
        ],
    },

    "Amazon": {
        "title": "🛒 Amazon Gift Card\nاختر المنطقة:",
        "buttons": [
            "Amazon - Saudi Arabia",
            "Amazon - UAE",
            "⬅️ رجوع"
        ],
    },

    "Amazon - Saudi Arabia": {
        "title": "🛒 Amazon - السعودية\nاختر البطاقة:",
        "buttons": [
            "Amazon KSA - 100 SAR - $35",
            "Amazon KSA - 200 SAR - $70",
            "Amazon KSA - 300 SAR - $100",
            "Amazon KSA - 400 SAR - $130",
            "Amazon KSA - 500 SAR - $160",
            "Amazon KSA - 1000 SAR - $310",
            "Amazon KSA - 2000 SAR - $613",
            "Amazon KSA - 5000 SAR - $1550",
            "⬅️ رجوع"
        ],
    },

    "Amazon - UAE": {
        "title": "🛒 Amazon - الإمارات\nاختر البطاقة:",
        "buttons": [
            "Amazon UAE - 100 AED - $32",
            "Amazon UAE - 150 AED - $46.70",
            "Amazon UAE - 200 AED - $61.5",
            "Amazon UAE - 250 AED - $75.5",
            "Amazon UAE - 300 AED - $91",
            "Amazon UAE - 400 AED - $157",
            "⬅️ رجوع"
        ],
    },

    "Roblox": {
        "title": "🎮 Roblox Gift Card - الإمارات\nاختر البطاقة:",
        "buttons": [
            "Roblox UAE - 20 AED - $7.5",
            "Roblox UAE - 50 AED - $16",
            "Roblox UAE - 100 AED - $31.5",
            "Roblox UAE - 200 AED - $60",
            "Roblox UAE - 500 AED - $142",
            "⬅️ رجوع"
        ],
    },
}

PARENT = {
    "اشتراكات ChatGPT": MAIN_MENU,
    "إنشاء حسابات ChatGPT": MAIN_MENU,
    "VPN": MAIN_MENU,
    "WireGuard": "VPN",
    "VLESS مع 10 مواقع IP": "VPN",
    "Telegram Stars": MAIN_MENU,
    "Apple iTunes": MAIN_MENU,
    "Apple iTunes - USA": "Apple iTunes",
    "Apple iTunes - Saudi Arabia": "Apple iTunes",
    "Apple iTunes - UAE": "Apple iTunes",
    "PSN": MAIN_MENU,
    "PSN - UAE": "PSN",
    "PSN - USA": "PSN",
    "Steam": MAIN_MENU,
    "Steam - Saudi Arabia": "Steam",
    "Steam - UAE": "Steam",
    "Amazon": MAIN_MENU,
    "Amazon - Saudi Arabia": "Amazon",
    "Amazon - UAE": "Amazon",
    "Roblox": MAIN_MENU,
}

PRODUCTS = {
    "ChatGPT Plus - 1 شهر - بدون تسجيل دخول - $12.5": {
        "text": "🤖 تجديد اشتراك ChatGPT 5.4\n📦 الخطة: Plus\n📅 المدة: 1 شهر\n🔐 بدون تسجيل دخول\n💵 السعر: $12.5",
        "flow": "chatgpt"
    },
    "ChatGPT Plus - 12 شهر - بدون تسجيل دخول - $113": {
        "text": "🤖 تجديد اشتراك ChatGPT 5.4\n📦 الخطة: Plus\n📅 المدة: 12 شهر\n🔐 بدون تسجيل دخول\n💵 السعر: $113",
        "flow": "chatgpt"
    },
    "ChatGPT Pro - 1 شهر - بدون تسجيل دخول - $158": {
        "text": "🤖 تجديد اشتراك ChatGPT 5.4\n📦 الخطة: Pro\n📅 المدة: 1 شهر\n🔐 بدون تسجيل دخول\n💵 السعر: $158",
        "flow": "chatgpt"
    },
    "ChatGPT Plus - 1 شهر - مع تسجيل دخول - $8.5": {
        "text": "🤖 تجديد اشتراك ChatGPT 5.4\n📦 الخطة: Plus\n📅 المدة: 1 شهر\n📧 مع تسجيل دخول\n💵 السعر: $8.5",
        "flow": "chatgpt"
    },
    "ChatGPT Plus - 12 شهر - مع تسجيل دخول - $99": {
        "text": "🤖 تجديد اشتراك ChatGPT 5.4\n📦 الخطة: Plus\n📅 المدة: 12 شهر\n📧 مع تسجيل دخول\n💵 السعر: $99",
        "flow": "chatgpt"
    },

    "حساب جاهز ChatGPT Plus - 1 شهر - $10.5": {
        "text": "🆕 إنشاء حساب ChatGPT 5.4\n📦 الخطة: Plus\n📅 المدة: 1 شهر\n✅ حساب جاهز\n💵 السعر: $10.5",
        "flow": "chatgpt"
    },
    "ChatGPT Plus على بريدك - 1 شهر - $17": {
        "text": "🆕 إنشاء حساب ChatGPT 5.4\n📦 الخطة: Plus\n📅 المدة: 1 شهر\n📧 على بريدك الإلكتروني\n💵 السعر: $17",
        "flow": "chatgpt"
    },
    "حساب جاهز ChatGPT Plus - 12 شهر - $98": {
        "text": "🆕 إنشاء حساب ChatGPT 5.4\n📦 الخطة: Plus\n📅 المدة: 12 شهر\n✅ حساب جاهز\n💵 السعر: $98",
        "flow": "chatgpt"
    },
    "ChatGPT Plus على بريدك - 12 شهر - $118": {
        "text": "🆕 إنشاء حساب ChatGPT 5.4\n📦 الخطة: Plus\n📅 المدة: 12 شهر\n📧 على بريدك الإلكتروني\n💵 السعر: $118",
        "flow": "chatgpt"
    },
    "حساب جاهز ChatGPT Pro - 12 شهر - $442": {
        "text": "🆕 إنشاء حساب ChatGPT 5.4\n📦 الخطة: Pro\n📅 المدة: 12 شهر\n✅ حساب جاهز\n💵 السعر: $442",
        "flow": "chatgpt"
    },
    "ChatGPT Pro على بريدك - 12 شهر - $476": {
        "text": "🆕 إنشاء حساب ChatGPT 5.4\n📦 الخطة: Pro\n📅 المدة: 12 شهر\n📧 على بريدك الإلكتروني\n💵 السعر: $476",
        "flow": "chatgpt"
    },

    "WireGuard - 1 شهر - $5": {"text": "🌐 WireGuard\n📅 المدة: 1 شهر\n💵 السعر: $5", "flow": "proof"},
    "WireGuard - 3 أشهر - $9": {"text": "🌐 WireGuard\n📅 المدة: 3 أشهر\n💵 السعر: $9", "flow": "proof"},
    "WireGuard - 6 أشهر - $16": {"text": "🌐 WireGuard\n📅 المدة: 6 أشهر\n💵 السعر: $16", "flow": "proof"},
    "VLESS - 1 شهر - $6": {"text": "🌐 VLESS مع 10 مواقع IP\n📅 المدة: 1 شهر\n💵 السعر: $6", "flow": "proof"},
    "VLESS - 3 أشهر - $15": {"text": "🌐 VLESS مع 10 مواقع IP\n📅 المدة: 3 أشهر\n💵 السعر: $15", "flow": "proof"},

    "50 Stars - $1.5": {"text": "⭐ Telegram Stars\n📦 الكمية: 50 Stars\n💵 السعر: $1.5", "flow": "stars"},
    "100 Stars - $3": {"text": "⭐ Telegram Stars\n📦 الكمية: 100 Stars\n💵 السعر: $3", "flow": "stars"},
    "250 Stars - $6": {"text": "⭐ Telegram Stars\n📦 الكمية: 250 Stars\n💵 السعر: $6", "flow": "stars"},
    "500 Stars - $11.5": {"text": "⭐ Telegram Stars\n📦 الكمية: 500 Stars\n💵 السعر: $11.5", "flow": "stars"},
    "1000 Stars - $22": {"text": "⭐ Telegram Stars\n📦 الكمية: 1000 Stars\n💵 السعر: $22", "flow": "stars"},
    "2000 Stars - $40": {"text": "⭐ Telegram Stars\n📦 الكمية: 2000 Stars\n💵 السعر: $40", "flow": "stars"},
    "3000 Stars - $60": {"text": "⭐ Telegram Stars\n📦 الكمية: 3000 Stars\n💵 السعر: $60", "flow": "stars"},
    "5000 Stars - $90": {"text": "⭐ Telegram Stars\n📦 الكمية: 5000 Stars\n💵 السعر: $90", "flow": "stars"},
}

PRODUCT_TEXTS_EXTRA = {
    "Apple USA - $2 - $3": "🍎 Apple iTunes USA\n📦 القيمة: $2\n💵 السعر: $3",
    "Apple USA - $3 - $4": "🍎 Apple iTunes USA\n📦 القيمة: $3\n💵 السعر: $4",
    "Apple USA - $4 - $5.5": "🍎 Apple iTunes USA\n📦 القيمة: $4\n💵 السعر: $5.5",
    "Apple USA - $5 - $6.70": "🍎 Apple iTunes USA\n📦 القيمة: $5\n💵 السعر: $6.70",
    "Apple USA - $10 - $12": "🍎 Apple iTunes USA\n📦 القيمة: $10\n💵 السعر: $12",
    "Apple USA - $20 - $23": "🍎 Apple iTunes USA\n📦 القيمة: $20\n💵 السعر: $23",
    "Apple USA - $25 - $28.5": "🍎 Apple iTunes USA\n📦 القيمة: $25\n💵 السعر: $28.5",
    "Apple USA - $50 - $56.5": "🍎 Apple iTunes USA\n📦 القيمة: $50\n💵 السعر: $56.5",
    "Apple USA - $100 - $112": "🍎 Apple iTunes USA\n📦 القيمة: $100\n💵 السعر: $112",
    "Apple USA - $200 - $225": "🍎 Apple iTunes USA\n📦 القيمة: $200\n💵 السعر: $225",
    "Apple USA - $500 - $540": "🍎 Apple iTunes USA\n📦 القيمة: $500\n💵 السعر: $540",

    "Apple KSA - 50 SAR - $16": "🍎 Apple iTunes السعودية\n📦 القيمة: 50 SAR\n💵 السعر: $16",
    "Apple KSA - 100 SAR - $32": "🍎 Apple iTunes السعودية\n📦 القيمة: 100 SAR\n💵 السعر: $32",
    "Apple KSA - 200 SAR - $62": "🍎 Apple iTunes السعودية\n📦 القيمة: 200 SAR\n💵 السعر: $62",
    "Apple KSA - 500 SAR - $150": "🍎 Apple iTunes السعودية\n📦 القيمة: 500 SAR\n💵 السعر: $150",
    "Apple KSA - 1000 SAR - $298": "🍎 Apple iTunes السعودية\n📦 القيمة: 1000 SAR\n💵 السعر: $298",

    "Apple UAE - 50 AED - $17.60": "🍎 Apple iTunes الإمارات\n📦 القيمة: 50 AED\n💵 السعر: $17.60",
    "Apple UAE - 100 AED - $35": "🍎 Apple iTunes الإمارات\n📦 القيمة: 100 AED\n💵 السعر: $35",
    "Apple UAE - 200 AED - $68": "🍎 Apple iTunes الإمارات\n📦 القيمة: 200 AED\n💵 السعر: $68",
    "Apple UAE - 500 AED - $166": "🍎 Apple iTunes الإمارات\n📦 القيمة: 500 AED\n💵 السعر: $166",
    "Apple UAE - 1000 AED - $327": "🍎 Apple iTunes الإمارات\n📦 القيمة: 1000 AED\n💵 السعر: $327",

    "PSN UAE - $10 - $13": "🎮 PSN الإمارات\n📦 القيمة: $10\n💵 السعر: $13",
    "PSN UAE - $20 - $25": "🎮 PSN الإمارات\n📦 القيمة: $20\n💵 السعر: $25",
    "PSN UAE - $30 - $37": "🎮 PSN الإمارات\n📦 القيمة: $30\n💵 السعر: $37",
    "PSN UAE - $50 - $57": "🎮 PSN الإمارات\n📦 القيمة: $50\n💵 السعر: $57",
    "PSN UAE - $70 - $79": "🎮 PSN الإمارات\n📦 القيمة: $70\n💵 السعر: $79",
    "PSN UAE - $100 - $108": "🎮 PSN الإمارات\n📦 القيمة: $100\n💵 السعر: $108",

    "PSN USA - $10 - $15": "🎮 PSN أمريكا\n📦 القيمة: $10\n💵 السعر: $15",
    "PSN USA - $20 - $30": "🎮 PSN أمريكا\n📦 القيمة: $20\n💵 السعر: $30",
    "PSN USA - $50 - $70": "🎮 PSN أمريكا\n📦 القيمة: $50\n💵 السعر: $70",
    "PSN USA - $100 - $130": "🎮 PSN أمريكا\n📦 القيمة: $100\n💵 السعر: $130",

    "Steam KSA - 5 SAR - $3.5": "🎮 Steam السعودية\n📦 القيمة: 5 SAR\n💵 السعر: $3.5",
    "Steam KSA - 10 SAR - $6.5": "🎮 Steam السعودية\n📦 القيمة: 10 SAR\n💵 السعر: $6.5",
    "Steam KSA - 20 SAR - $11": "🎮 Steam السعودية\n📦 القيمة: 20 SAR\n💵 السعر: $11",
    "Steam KSA - 50 SAR - $22": "🎮 Steam السعودية\n📦 القيمة: 50 SAR\n💵 السعر: $22",
    "Steam KSA - 100 SAR - $40": "🎮 Steam السعودية\n📦 القيمة: 100 SAR\n💵 السعر: $40",
    "Steam KSA - 200 SAR - $64": "🎮 Steam السعودية\n📦 القيمة: 200 SAR\n💵 السعر: $64",

    "Steam UAE - 1.40 AED - $1": "🎮 Steam الإمارات\n📦 القيمة: 1.40 AED\n💵 السعر: $1",
    "Steam UAE - 2.80 AED - $1.8": "🎮 Steam الإمارات\n📦 القيمة: 2.80 AED\n💵 السعر: $1.8",
    "Steam UAE - 18.60 AED - $7.5": "🎮 Steam الإمارات\n📦 القيمة: 18.60 AED\n💵 السعر: $7.5",
    "Steam UAE - 37.50 AED - $15": "🎮 Steam الإمارات\n📦 القيمة: 37.50 AED\n💵 السعر: $15",
    "Steam UAE - 46.80 AED - $18.5": "🎮 Steam الإمارات\n📦 القيمة: 46.80 AED\n💵 السعر: $18.5",
    "Steam UAE - 93.88 AED - $34.5": "🎮 Steam الإمارات\n📦 القيمة: 93.88 AED\n💵 السعر: $34.5",
    "Steam UAE - 140.80 AED - $51": "🎮 Steam الإمارات\n📦 القيمة: 140.80 AED\n💵 السعر: $51",
    "Steam UAE - 234.60 AED - $84": "🎮 Steam الإمارات\n📦 القيمة: 234.60 AED\n💵 السعر: $84",
    "Steam UAE - 469.40 AED - $166": "🎮 Steam الإمارات\n📦 القيمة: 469.40 AED\n💵 السعر: $166",
    "Steam UAE - 938.90 AED - $326": "🎮 Steam الإمارات\n📦 القيمة: 938.90 AED\n💵 السعر: $326",

    "Amazon KSA - 100 SAR - $35": "🛒 Amazon السعودية\n📦 القيمة: 100 SAR\n💵 السعر: $35",
    "Amazon KSA - 200 SAR - $70": "🛒 Amazon السعودية\n📦 القيمة: 200 SAR\n💵 السعر: $70",
    "Amazon KSA - 300 SAR - $100": "🛒 Amazon السعودية\n📦 القيمة: 300 SAR\n💵 السعر: $100",
    "Amazon KSA - 400 SAR - $130": "🛒 Amazon السعودية\n📦 القيمة: 400 SAR\n💵 السعر: $130",
    "Amazon KSA - 500 SAR - $160": "🛒 Amazon السعودية\n📦 القيمة: 500 SAR\n💵 السعر: $160",
    "Amazon KSA - 1000 SAR - $310": "🛒 Amazon السعودية\n📦 القيمة: 1000 SAR\n💵 السعر: $310",
    "Amazon KSA - 2000 SAR - $613": "🛒 Amazon السعودية\n📦 القيمة: 2000 SAR\n💵 السعر: $613",
    "Amazon KSA - 5000 SAR - $1550": "🛒 Amazon السعودية\n📦 القيمة: 5000 SAR\n💵 السعر: $1550",

    "Amazon UAE - 100 AED - $32": "🛒 Amazon الإمارات\n📦 القيمة: 100 AED\n💵 السعر: $32",
    "Amazon UAE - 150 AED - $46.70": "🛒 Amazon الإمارات\n📦 القيمة: 150 AED\n💵 السعر: $46.70",
    "Amazon UAE - 200 AED - $61.5": "🛒 Amazon الإمارات\n📦 القيمة: 200 AED\n💵 السعر: $61.5",
    "Amazon UAE - 250 AED - $75.5": "🛒 Amazon الإمارات\n📦 القيمة: 250 AED\n💵 السعر: $75.5",
    "Amazon UAE - 300 AED - $91": "🛒 Amazon الإمارات\n📦 القيمة: 300 AED\n💵 السعر: $91",
    "Amazon UAE - 400 AED - $157": "🛒 Amazon الإمارات\n📦 القيمة: 400 AED\n💵 السعر: $157",

    "Roblox UAE - 20 AED - $7.5": "🎮 Roblox الإمارات\n📦 القيمة: 20 AED\n💵 السعر: $7.5",
    "Roblox UAE - 50 AED - $16": "🎮 Roblox الإمارات\n📦 القيمة: 50 AED\n💵 السعر: $16",
    "Roblox UAE - 100 AED - $31.5": "🎮 Roblox الإمارات\n📦 القيمة: 100 AED\n💵 السعر: $31.5",
    "Roblox UAE - 200 AED - $60": "🎮 Roblox الإمارات\n📦 القيمة: 200 AED\n💵 السعر: $60",
    "Roblox UAE - 500 AED - $142": "🎮 Roblox الإمارات\n📦 القيمة: 500 AED\n💵 السعر: $142",
}

for k, v in PRODUCT_TEXTS_EXTRA.items():
    PRODUCTS[k] = {"text": v, "flow": "proof"}


def admin_notify(text: str):
    if ADMIN_CHAT_ID:
        try:
            send_message(int(ADMIN_CHAT_ID), text)
        except Exception as e:
            print("Admin notify error:", e)


def admin_notify_photo(file_id: str, caption: str):
    if ADMIN_CHAT_ID:
        try:
            send_photo(int(ADMIN_CHAT_ID), file_id, caption)
        except Exception as e:
            print("Admin photo notify error:", e)


def show_menu(chat_id: int, menu_key: str):
    st = get_user(chat_id)
    st["menu"] = menu_key
    st["selected_product"] = None
    st["selected_currency"] = None
    st["awaiting"] = None
    menu = CATALOG[menu_key]
    send_message(chat_id, menu["title"], menu["buttons"])


def show_currency_menu(chat_id: int, product_key: str):
    st = get_user(chat_id)
    st["selected_product"] = product_key
    st["selected_currency"] = None
    st["awaiting"] = None
    product = PRODUCTS[product_key]

    text = f"""{product['text']}

💳 اختر العملة التي تريد الدفع بها:"""

    buttons = [
        "USDT (TRC20)",
        "USDT (ERC20)",
        "BTC",
        "ETH",
        "⬅️ رجوع إلى المنتجات"
    ]
    send_message(chat_id, text, buttons)


def show_wallet_and_next_step(chat_id: int, currency: str):
    st = get_user(chat_id)
    product_key = st.get("selected_product")
    if not product_key:
        send_message(chat_id, "اختر المنتج أولاً.", CATALOG[MAIN_MENU]["buttons"])
        return

    st["selected_currency"] = currency
    product = PRODUCTS[product_key]
    wallet = WALLETS.get(currency, "NOT_SET")

    base_text = f"""{product['text']}

💳 طريقة الدفع: {currency}
📮 عنوان المحفظة:
{wallet}
"""

    flow = product["flow"]

    if flow == "chatgpt":
        text = f"""{base_text}
بعد إتمام الدفع، يرجى إرسال رسالة إلى الدعم مع صورة الدفع أو TXID:

👉 {SUPPORT_USERNAME}

🟢 نحن متاحون للرد 24/7
⚡ جميع الطلبات يتم تسليمها خلال 5 إلى 10 دقائق كحد أقصى"""
        send_message(chat_id, text, ["⬅️ رجوع إلى المنتجات", "الدعم"])

    elif flow == "stars":
        st["awaiting"] = "telegram_username"
        text = f"""{base_text}
بعد الدفع، أرسل يوزر تيليجرام الخاص بك هنا داخل البوت.

مثال:
@username

⚡ سيتم تنفيذ الطلب خلال 5 إلى 10 دقائق"""
        send_message(chat_id, text, ["⬅️ رجوع إلى المنتجات"])

    else:
        text = f"""{base_text}
بعد الدفع، اختر إحدى الطرق التالية لإرسال إثبات الدفع:"""
        st["awaiting"] = None
        send_message(chat_id, text, ["إرسال TXID", "إرسال صورة الدفع", "⬅️ رجوع إلى المنتجات"])


def show_product(chat_id: int, product_key: str):
    show_currency_menu(chat_id, product_key)


def handle_proof_text(message: dict):
    chat_id = message["chat"]["id"]
    st = get_user(chat_id)
    text = (message.get("text") or "").strip()
    username = message.get("from", {}).get("username", "")
    first_name = message.get("from", {}).get("first_name", "")
    selected_product = st.get("selected_product", "")
    selected_currency = st.get("selected_currency", "")

    if st.get("awaiting") == "txid":
        admin_notify(
            f"""📥 إثبات دفع جديد (TXID)

👤 الاسم: {first_name}
🆔 user_id: {chat_id}
🔗 username: @{username if username else 'none'}

📦 المنتج:
{selected_product}

💳 العملة:
{selected_currency}

🧾 TXID:
{text}"""
        )
        st["awaiting"] = None
        send_message(
            chat_id,
            """✅ تم استلام TXID بنجاح.
سيتم مراجعة الدفع وإرسال الطلب لك في أقرب وقت ممكن.""",
            ["⬅️ رجوع إلى القائمة الرئيسية", "الدعم"]
        )
        return True

    if st.get("awaiting") == "telegram_username":
        admin_notify(
            f"""📥 طلب Telegram Stars جديد

👤 الاسم: {first_name}
🆔 user_id: {chat_id}
🔗 username داخل تيليجرام: @{username if username else 'none'}

📦 المنتج:
{selected_product}

💳 العملة:
{selected_currency}

📨 يوزر المستلم:
{text}"""
        )
        st["awaiting"] = None
        send_message(
            chat_id,
            """✅ تم استلام يوزر تيليجرام بنجاح.
سيتم تنفيذ طلبك خلال 5 إلى 10 دقائق.""",
            ["⬅️ رجوع إلى القائمة الرئيسية", "الدعم"]
        )
        return True

    return False


def handle_proof_photo(message: dict):
    chat_id = message["chat"]["id"]
    st = get_user(chat_id)

    if st.get("awaiting") != "photo":
        return False

    photos = message.get("photo", [])
    if not photos:
        return False

    biggest = photos[-1]
    file_id = biggest["file_id"]

    username = message.get("from", {}).get("username", "")
    first_name = message.get("from", {}).get("first_name", "")
    selected_product = st.get("selected_product", "")
    selected_currency = st.get("selected_currency", "")

    caption = f"""📥 صورة إثبات دفع جديدة

👤 الاسم: {first_name}
🆔 user_id: {chat_id}
🔗 username: @{username if username else 'none'}

📦 المنتج:
{selected_product}

💳 العملة:
{selected_currency}"""

    admin_notify_photo(file_id, caption)

    st["awaiting"] = None
    send_message(
        chat_id,
        """✅ تم استلام صورة الدفع بنجاح.
سيتم مراجعة الدفع وإرسال الطلب لك في أقرب وقت ممكن.""",
        ["⬅️ رجوع إلى القائمة الرئيسية", "الدعم"]
    )
    return True


def handle_admin_command(message: dict):
    chat_id = message["chat"]["id"]
    text = (message.get("text") or "").strip()

    if not ADMIN_CHAT_ID:
        return False

    if str(chat_id) != str(ADMIN_CHAT_ID):
        return False

    if text.startswith("/send "):
        parts = text.split(" ", 2)
        if len(parts) < 3:
            send_message(chat_id, "استخدم هكذا:\n/send user_id الرسالة")
            return True

        try:
            target_user = int(parts[1])
        except ValueError:
            send_message(chat_id, "user_id غير صحيح")
            return True

        msg = parts[2]
        send_message(target_user, f"📩 رسالة من الإدارة:\n\n{msg}", ["⬅️ رجوع إلى القائمة الرئيسية"])
        send_message(chat_id, "✅ تم الإرسال")
        return True

    return False


def handle_message(message: dict):
    chat_id = message["chat"]["id"]
    text = (message.get("text") or "").strip()

    if handle_admin_command(message):
        return

    st = get_user(chat_id)

    if handle_proof_text(message):
        return

    if text == "/start":
        show_menu(chat_id, MAIN_MENU)
        return

    if text == "الدعم":
        send_message(
            chat_id,
            f"""📩 للتواصل المباشر:
{SUPPORT_USERNAME}""",
            ["⬅️ رجوع إلى القائمة الرئيسية"]
        )
        return

    if text == "⬅️ رجوع":
        current = st.get("menu", MAIN_MENU)
        parent = PARENT.get(current, MAIN_MENU)
        show_menu(chat_id, parent)
        return

    if text == "⬅️ رجوع إلى المنتجات":
        current = st.get("menu", MAIN_MENU)
        show_menu(chat_id, current)
        return

    if text == "⬅️ رجوع إلى القائمة الرئيسية":
        show_menu(chat_id, MAIN_MENU)
        return

    if text in WALLETS:
        show_wallet_and_next_step(chat_id, text)
        return

    if text == "إرسال TXID":
        st["awaiting"] = "txid"
        send_message(chat_id, "أرسل TXID هنا الآن.", ["⬅️ رجوع إلى المنتجات"])
        return

    if text == "إرسال صورة الدفع":
        st["awaiting"] = "photo"
        send_message(chat_id, "أرسل صورة الدفع هنا الآن.", ["⬅️ رجوع إلى المنتجات"])
        return

    if text in CATALOG:
        show_menu(chat_id, text)
        return

    if text in PRODUCTS:
        show_product(chat_id, text)
        return

    send_message(chat_id, "اختر من القائمة من فضلك.", CATALOG[MAIN_MENU]["buttons"])


def handle_update(update: dict):
    if "message" in update:
        message = update["message"]

        if "photo" in message:
            if handle_proof_photo(message):
                return

        handle_message(message)


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
