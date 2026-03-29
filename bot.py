import os
import time
import requests

TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    raise ValueError("TOKEN environment variable is missing")

BASE_URL = f"https://api.telegram.org/bot{TOKEN}"
SUPPORT_USERNAME = "@Natar100"

PAYMENT_TEXT = f"""💳 الدفع عبر العملات الرقمية فقط

📩 للتواصل والدفع:
{SUPPORT_USERNAME}

🟢 نحن متاحون للرد 24/7
⚡ جميع الطلبات يتم تسليمها خلال 5 إلى 10 دقائق كحد أقصى"""

MAIN_MENU = "main"

CATALOG = {
    MAIN_MENU: {
        "title": "مرحباً 👋\nاختر القسم الذي تريده:",
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
            "Plus شهر - بدون دخول - $12.5",
            "Plus سنة - بدون دخول - $113",
            "Pro شهر - بدون دخول - $158",
            "Plus شهر - مع دخول - $8.5",
            "Plus سنة - مع دخول - $99",
            "⬅️ رجوع"
        ],
    },

    "إنشاء حسابات ChatGPT": {
        "title": "🆕 إنشاء حساب ChatGPT 5.4 + اشتراك\nاختر المنتج:",
        "buttons": [
            "حساب جاهز Plus شهر - $10.5",
            "على بريدك Plus شهر - $17",
            "حساب جاهز Plus سنة - $98",
            "على بريدك Plus سنة - $118",
            "حساب جاهز Pro سنة - $442",
            "على بريدك Pro سنة - $476",
            "⬅️ رجوع"
        ],
    },

    "VPN": {
        "title": "🌐 خدمات VPN\nاختر النوع:",
        "buttons": [
            "WireGuard",
            "VLESS",
            "⬅️ رجوع"
        ],
    },

    "WireGuard": {
        "title": "🌐 WireGuard\nاختر الخطة:",
        "buttons": [
            "WireGuard شهر - $5",
            "WireGuard 3 أشهر - $9",
            "WireGuard 6 أشهر - $16",
            "⬅️ رجوع"
        ],
    },

    "VLESS": {
        "title": "🌐 VLESS مع 10 مواقع IP\nاختر الخطة:",
        "buttons": [
            "VLESS شهر - $6",
            "VLESS 3 أشهر - $15",
            "⬅️ رجوع"
        ],
    },

    "Telegram Stars": {
        "title": "⭐ Telegram Stars (توصيل فوري)\nاختر الكمية:",
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
            "Apple USA",
            "Apple KSA",
            "Apple UAE",
            "⬅️ رجوع"
        ],
    },

    "Apple USA": {
        "title": "🍎 Apple iTunes - الولايات المتحدة\nاختر البطاقة:",
        "buttons": [
            "Apple USA $2 - $3",
            "Apple USA $3 - $4",
            "Apple USA $4 - $5.5",
            "Apple USA $5 - $6.70",
            "Apple USA $10 - $12",
            "Apple USA $20 - $23",
            "Apple USA $25 - $28.5",
            "Apple USA $50 - $56.5",
            "Apple USA $100 - $112",
            "Apple USA $200 - $225",
            "Apple USA $500 - $540",
            "⬅️ رجوع"
        ],
    },

    "Apple KSA": {
        "title": "🍎 Apple iTunes - السعودية\nاختر البطاقة:",
        "buttons": [
            "Apple KSA 50 SAR - $16",
            "Apple KSA 100 SAR - $32",
            "Apple KSA 200 SAR - $62",
            "Apple KSA 500 SAR - $150",
            "Apple KSA 1000 SAR - $298",
            "⬅️ رجوع"
        ],
    },

    "Apple UAE": {
        "title": "🍎 Apple iTunes - الإمارات\nاختر البطاقة:",
        "buttons": [
            "Apple UAE 50 AED - $17.60",
            "Apple UAE 100 AED - $35",
            "Apple UAE 200 AED - $68",
            "Apple UAE 500 AED - $166",
            "Apple UAE 1000 AED - $327",
            "⬅️ رجوع"
        ],
    },

    "PSN": {
        "title": "🎮 PlayStation Gift Card\nاختر المنطقة:",
        "buttons": [
            "PSN UAE",
            "PSN USA",
            "⬅️ رجوع"
        ],
    },

    "PSN UAE": {
        "title": "🎮 PSN - الإمارات\nاختر البطاقة:",
        "buttons": [
            "PSN UAE $10 - $13",
            "PSN UAE $20 - $25",
            "PSN UAE $30 - $37",
            "PSN UAE $50 - $57",
            "PSN UAE $70 - $79",
            "PSN UAE $100 - $108",
            "⬅️ رجوع"
        ],
    },

    "PSN USA": {
        "title": "🎮 PSN - أمريكا\nاختر البطاقة:",
        "buttons": [
            "PSN USA $10 - $15",
            "PSN USA $20 - $30",
            "PSN USA $50 - $70",
            "PSN USA $100 - $130",
            "⬅️ رجوع"
        ],
    },

    "Steam": {
        "title": "🎮 Steam Gift Card\nاختر المنطقة:",
        "buttons": [
            "Steam KSA",
            "Steam UAE",
            "⬅️ رجوع"
        ],
    },

    "Steam KSA": {
        "title": "🎮 Steam - السعودية\nاختر البطاقة:",
        "buttons": [
            "Steam KSA 5 SAR - $3.5",
            "Steam KSA 10 SAR - $6.5",
            "Steam KSA 20 SAR - $11",
            "Steam KSA 50 SAR - $22",
            "Steam KSA 100 SAR - $40",
            "Steam KSA 200 SAR - $64",
            "⬅️ رجوع"
        ],
    },

    "Steam UAE": {
        "title": "🎮 Steam - الإمارات\nاختر البطاقة:",
        "buttons": [
            "Steam UAE 1.40 AED - $1",
            "Steam UAE 2.80 AED - $1.8",
            "Steam UAE 18.60 AED - $7.5",
            "Steam UAE 37.50 AED - $15",
            "Steam UAE 46.80 AED - $18.5",
            "Steam UAE 93.88 AED - $34.5",
            "Steam UAE 140.80 AED - $51",
            "Steam UAE 234.60 AED - $84",
            "Steam UAE 469.40 AED - $166",
            "Steam UAE 938.90 AED - $326",
            "⬅️ رجوع"
        ],
    },

    "Amazon": {
        "title": "🛒 Amazon Gift Card\nاختر المنطقة:",
        "buttons": [
            "Amazon KSA",
            "Amazon UAE",
            "⬅️ رجوع"
        ],
    },

    "Amazon KSA": {
        "title": "🛒 Amazon - السعودية\nاختر البطاقة:",
        "buttons": [
            "Amazon KSA 100 SAR - $35",
            "Amazon KSA 200 SAR - $70",
            "Amazon KSA 300 SAR - $100",
            "Amazon KSA 400 SAR - $130",
            "Amazon KSA 500 SAR - $160",
            "Amazon KSA 1000 SAR - $310",
            "Amazon KSA 2000 SAR - $613",
            "Amazon KSA 5000 SAR - $1550",
            "⬅️ رجوع"
        ],
    },

    "Amazon UAE": {
        "title": "🛒 Amazon - الإمارات\nاختر البطاقة:",
        "buttons": [
            "Amazon UAE 100 AED - $32",
            "Amazon UAE 150 AED - $46.70",
            "Amazon UAE 200 AED - $61.5",
            "Amazon UAE 250 AED - $75.5",
            "Amazon UAE 300 AED - $91",
            "Amazon UAE 400 AED - $157",
            "⬅️ رجوع"
        ],
    },

    "Roblox": {
        "title": "🎮 Roblox Gift Card - الإمارات\nاختر البطاقة:",
        "buttons": [
            "Roblox UAE 20 AED - $7.5",
            "Roblox UAE 50 AED - $16",
            "Roblox UAE 100 AED - $31.5",
            "Roblox UAE 200 AED - $60",
            "Roblox UAE 500 AED - $142",
            "⬅️ رجوع"
        ],
    },
}

PARENT = {
    "اشتراكات ChatGPT": MAIN_MENU,
    "إنشاء حسابات ChatGPT": MAIN_MENU,
    "VPN": MAIN_MENU,
    "WireGuard": "VPN",
    "VLESS": "VPN",
    "Telegram Stars": MAIN_MENU,
    "Apple iTunes": MAIN_MENU,
    "Apple USA": "Apple iTunes",
    "Apple KSA": "Apple iTunes",
    "Apple UAE": "Apple iTunes",
    "PSN": MAIN_MENU,
    "PSN UAE": "PSN",
    "PSN USA": "PSN",
    "Steam": MAIN_MENU,
    "Steam KSA": "Steam",
    "Steam UAE": "Steam",
    "Amazon": MAIN_MENU,
    "Amazon KSA": "Amazon",
    "Amazon UAE": "Amazon",
    "Roblox": MAIN_MENU,
}

PRODUCTS = {
    "Plus شهر - بدون دخول - $12.5": "🤖 تجديد اشتراك ChatGPT 5.4\n📦 Plus لمدة شهر\n🔐 بدون تسجيل دخول\n💵 السعر: $12.5",
    "Plus سنة - بدون دخول - $113": "🤖 تجديد اشتراك ChatGPT 5.4\n📦 Plus لمدة 12 شهر\n🔐 بدون تسجيل دخول\n💵 السعر: $113",
    "Pro شهر - بدون دخول - $158": "🤖 تجديد اشتراك ChatGPT 5.4\n📦 Pro لمدة شهر\n🔐 بدون تسجيل دخول\n💵 السعر: $158",
    "Plus شهر - مع دخول - $8.5": "🤖 تجديد اشتراك ChatGPT 5.4\n📦 Plus لمدة شهر\n📧 مع الإيميل وكلمة المرور\n💵 السعر: $8.5",
    "Plus سنة - مع دخول - $99": "🤖 تجديد اشتراك ChatGPT 5.4\n📦 Plus لمدة 12 شهر\n📧 مع الإيميل وكلمة المرور\n💵 السعر: $99",

    "حساب جاهز Plus شهر - $10.5": "🆕 إنشاء حساب ChatGPT 5.4\n📦 حساب جاهز Plus لمدة شهر\n💵 السعر: $10.5",
    "على بريدك Plus شهر - $17": "🆕 إنشاء حساب ChatGPT 5.4\n📦 Plus لمدة شهر على بريدك الإلكتروني\n💵 السعر: $17",
    "حساب جاهز Plus سنة - $98": "🆕 إنشاء حساب ChatGPT 5.4\n📦 حساب جاهز Plus لمدة 12 شهر\n💵 السعر: $98",
    "على بريدك Plus سنة - $118": "🆕 إنشاء حساب ChatGPT 5.4\n📦 Plus لمدة 12 شهر على بريدك الإلكتروني\n💵 السعر: $118",
    "حساب جاهز Pro سنة - $442": "🆕 إنشاء حساب ChatGPT 5.4\n📦 حساب جاهز Pro لمدة 12 شهر\n💵 السعر: $442",
    "على بريدك Pro سنة - $476": "🆕 إنشاء حساب ChatGPT 5.4\n📦 Pro لمدة 12 شهر على بريدك الإلكتروني\n💵 السعر: $476",

    "WireGuard شهر - $5": "🌐 WireGuard\n📦 مدة شهر\n💵 السعر: $5",
    "WireGuard 3 أشهر - $9": "🌐 WireGuard\n📦 مدة 3 أشهر\n💵 السعر: $9",
    "WireGuard 6 أشهر - $16": "🌐 WireGuard\n📦 مدة 6 أشهر\n💵 السعر: $16",
    "VLESS شهر - $6": "🌐 VLESS مع 10 مواقع IP\n📦 مدة شهر\n💵 السعر: $6",
    "VLESS 3 أشهر - $15": "🌐 VLESS مع 10 مواقع IP\n📦 مدة 3 أشهر\n💵 السعر: $15",

    "50 Stars - $1.5": "⭐ Telegram Stars\n📦 50 Stars\n💵 السعر: $1.5\n⚡ توصيل تلقائي",
    "100 Stars - $3": "⭐ Telegram Stars\n📦 100 Stars\n💵 السعر: $3\n⚡ توصيل تلقائي",
    "250 Stars - $6": "⭐ Telegram Stars\n📦 250 Stars\n💵 السعر: $6\n⚡ توصيل تلقائي",
    "500 Stars - $11.5": "⭐ Telegram Stars\n📦 500 Stars\n💵 السعر: $11.5\n⚡ توصيل تلقائي",
    "1000 Stars - $22": "⭐ Telegram Stars\n📦 1000 Stars\n💵 السعر: $22\n⚡ توصيل تلقائي",
    "2000 Stars - $40": "⭐ Telegram Stars\n📦 2000 Stars\n💵 السعر: $40\n⚡ توصيل تلقائي",
    "3000 Stars - $60": "⭐ Telegram Stars\n📦 3000 Stars\n💵 السعر: $60\n⚡ توصيل تلقائي",
    "5000 Stars - $90": "⭐ Telegram Stars\n📦 5000 Stars\n💵 السعر: $90\n⚡ توصيل تلقائي",

    "Apple USA $2 - $3": "🍎 Apple iTunes USA\n📦 بطاقة $2\n💵 السعر: $3",
    "Apple USA $3 - $4": "🍎 Apple iTunes USA\n📦 بطاقة $3\n💵 السعر: $4",
    "Apple USA $4 - $5.5": "🍎 Apple iTunes USA\n📦 بطاقة $4\n💵 السعر: $5.5",
    "Apple USA $5 - $6.70": "🍎 Apple iTunes USA\n📦 بطاقة $5\n💵 السعر: $6.70",
    "Apple USA $10 - $12": "🍎 Apple iTunes USA\n📦 بطاقة $10\n💵 السعر: $12",
    "Apple USA $20 - $23": "🍎 Apple iTunes USA\n📦 بطاقة $20\n💵 السعر: $23",
    "Apple USA $25 - $28.5": "🍎 Apple iTunes USA\n📦 بطاقة $25\n💵 السعر: $28.5",
    "Apple USA $50 - $56.5": "🍎 Apple iTunes USA\n📦 بطاقة $50\n💵 السعر: $56.5",
    "Apple USA $100 - $112": "🍎 Apple iTunes USA\n📦 بطاقة $100\n💵 السعر: $112",
    "Apple USA $200 - $225": "🍎 Apple iTunes USA\n📦 بطاقة $200\n💵 السعر: $225",
    "Apple USA $500 - $540": "🍎 Apple iTunes USA\n📦 بطاقة $500\n💵 السعر: $540",

    "Apple KSA 50 SAR - $16": "🍎 Apple iTunes السعودية\n📦 بطاقة 50 SAR\n💵 السعر: $16",
    "Apple KSA 100 SAR - $32": "🍎 Apple iTunes السعودية\n📦 بطاقة 100 SAR\n💵 السعر: $32",
    "Apple KSA 200 SAR - $62": "🍎 Apple iTunes السعودية\n📦 بطاقة 200 SAR\n💵 السعر: $62",
    "Apple KSA 500 SAR - $150": "🍎 Apple iTunes السعودية\n📦 بطاقة 500 SAR\n💵 السعر: $150",
    "Apple KSA 1000 SAR - $298": "🍎 Apple iTunes السعودية\n📦 بطاقة 1000 SAR\n💵 السعر: $298",

    "Apple UAE 50 AED - $17.60": "🍎 Apple iTunes الإمارات\n📦 بطاقة 50 AED\n💵 السعر: $17.60",
    "Apple UAE 100 AED - $35": "🍎 Apple iTunes الإمارات\n📦 بطاقة 100 AED\n💵 السعر: $35",
    "Apple UAE 200 AED - $68": "🍎 Apple iTunes الإمارات\n📦 بطاقة 200 AED\n💵 السعر: $68",
    "Apple UAE 500 AED - $166": "🍎 Apple iTunes الإمارات\n📦 بطاقة 500 AED\n💵 السعر: $166",
    "Apple UAE 1000 AED - $327": "🍎 Apple iTunes الإمارات\n📦 بطاقة 1000 AED\n💵 السعر: $327",

    "PSN UAE $10 - $13": "🎮 PSN الإمارات\n📦 بطاقة $10\n💵 السعر: $13",
    "PSN UAE $20 - $25": "🎮 PSN الإمارات\n📦 بطاقة $20\n💵 السعر: $25",
    "PSN UAE $30 - $37": "🎮 PSN الإمارات\n📦 بطاقة $30\n💵 السعر: $37",
    "PSN UAE $50 - $57": "🎮 PSN الإمارات\n📦 بطاقة $50\n💵 السعر: $57",
    "PSN UAE $70 - $79": "🎮 PSN الإمارات\n📦 بطاقة $70\n💵 السعر: $79",
    "PSN UAE $100 - $108": "🎮 PSN الإمارات\n📦 بطاقة $100\n💵 السعر: $108",

    "PSN USA $10 - $15": "🎮 PSN أمريكا\n📦 بطاقة $10\n💵 السعر: $15",
    "PSN USA $20 - $30": "🎮 PSN أمريكا\n📦 بطاقة $20\n💵 السعر: $30",
    "PSN USA $50 - $70": "🎮 PSN أمريكا\n📦 بطاقة $50\n💵 السعر: $70",
    "PSN USA $100 - $130": "🎮 PSN أمريكا\n📦 بطاقة $100\n💵 السعر: $130",

    "Steam KSA 5 SAR - $3.5": "🎮 Steam السعودية\n📦 بطاقة 5 SAR\n💵 السعر: $3.5",
    "Steam KSA 10 SAR - $6.5": "🎮 Steam السعودية\n📦 بطاقة 10 SAR\n💵 السعر: $6.5",
    "Steam KSA 20 SAR - $11": "🎮 Steam السعودية\n📦 بطاقة 20 SAR\n💵 السعر: $11",
    "Steam KSA 50 SAR - $22": "🎮 Steam السعودية\n📦 بطاقة 50 SAR\n💵 السعر: $22",
    "Steam KSA 100 SAR - $40": "🎮 Steam السعودية\n📦 بطاقة 100 SAR\n💵 السعر: $40",
    "Steam KSA 200 SAR - $64": "🎮 Steam السعودية\n📦 بطاقة 200 SAR\n💵 السعر: $64",

    "Steam UAE 1.40 AED - $1": "🎮 Steam الإمارات\n📦 بطاقة 1.40 AED\n💵 السعر: $1",
    "Steam UAE 2.80 AED - $1.8": "🎮 Steam الإمارات\n📦 بطاقة 2.80 AED\n💵 السعر: $1.8",
    "Steam UAE 18.60 AED - $7.5": "🎮 Steam الإمارات\n📦 بطاقة 18.60 AED\n💵 السعر: $7.5",
    "Steam UAE 37.50 AED - $15": "🎮 Steam الإمارات\n📦 بطاقة 37.50 AED\n💵 السعر: $15",
    "Steam UAE 46.80 AED - $18.5": "🎮 Steam الإمارات\n📦 بطاقة 46.80 AED\n💵 السعر: $18.5",
    "Steam UAE 93.88 AED - $34.5": "🎮 Steam الإمارات\n📦 بطاقة 93.88 AED\n💵 السعر: $34.5",
    "Steam UAE 140.80 AED - $51": "🎮 Steam الإمارات\n📦 بطاقة 140.80 AED\n💵 السعر: $51",
    "Steam UAE 234.60 AED - $84": "🎮 Steam الإمارات\n📦 بطاقة 234.60 AED\n💵 السعر: $84",
    "Steam UAE 469.40 AED - $166": "🎮 Steam الإمارات\n📦 بطاقة 469.40 AED\n💵 السعر: $166",
    "Steam UAE 938.90 AED - $326": "🎮 Steam الإمارات\n📦 بطاقة 938.90 AED\n💵 السعر: $326",

    "Amazon KSA 100 SAR - $35": "🛒 Amazon السعودية\n📦 بطاقة 100 SAR\n💵 السعر: $35",
    "Amazon KSA 200 SAR - $70": "🛒 Amazon السعودية\n📦 بطاقة 200 SAR\n💵 السعر: $70",
    "Amazon KSA 300 SAR - $100": "🛒 Amazon السعودية\n📦 بطاقة 300 SAR\n💵 السعر: $100",
    "Amazon KSA 400 SAR - $130": "🛒 Amazon السعودية\n📦 بطاقة 400 SAR\n💵 السعر: $130",
    "Amazon KSA 500 SAR - $160": "🛒 Amazon السعودية\n📦 بطاقة 500 SAR\n💵 السعر: $160",
    "Amazon KSA 1000 SAR - $310": "🛒 Amazon السعودية\n📦 بطاقة 1000 SAR\n💵 السعر: $310",
    "Amazon KSA 2000 SAR - $613": "🛒 Amazon السعودية\n📦 بطاقة 2000 SAR\n💵 السعر: $613",
    "Amazon KSA 5000 SAR - $1550": "🛒 Amazon السعودية\n📦 بطاقة 5000 SAR\n💵 السعر: $1550",

    "Amazon UAE 100 AED - $32": "🛒 Amazon الإمارات\n📦 بطاقة 100 AED\n💵 السعر: $32",
    "Amazon UAE 150 AED - $46.70": "🛒 Amazon الإمارات\n📦 بطاقة 150 AED\n💵 السعر: $46.70",
    "Amazon UAE 200 AED - $61.5": "🛒 Amazon الإمارات\n📦 بطاقة 200 AED\n💵 السعر: $61.5",
    "Amazon UAE 250 AED - $75.5": "🛒 Amazon الإمارات\n📦 بطاقة 250 AED\n💵 السعر: $75.5",
    "Amazon UAE 300 AED - $91": "🛒 Amazon الإمارات\n📦 بطاقة 300 AED\n💵 السعر: $91",
    "Amazon UAE 400 AED - $157": "🛒 Amazon الإمارات\n📦 بطاقة 400 AED\n💵 السعر: $157",

    "Roblox UAE 20 AED - $7.5": "🎮 Roblox الإمارات\n📦 بطاقة 20 AED\n💵 السعر: $7.5",
    "Roblox UAE 50 AED - $16": "🎮 Roblox الإمارات\n📦 بطاقة 50 AED\n💵 السعر: $16",
    "Roblox UAE 100 AED - $31.5": "🎮 Roblox الإمارات\n📦 بطاقة 100 AED\n💵 السعر: $31.5",
    "Roblox UAE 200 AED - $60": "🎮 Roblox الإمارات\n📦 بطاقة 200 AED\n💵 السعر: $60",
    "Roblox UAE 500 AED - $142": "🎮 Roblox الإمارات\n📦 بطاقة 500 AED\n💵 السعر: $142",
}

user_state = {}


def tg_post(method: str, data: dict):
    response = requests.post(f"{BASE_URL}/{method}", json=data, timeout=30)
    response.raise_for_status()
    return response.json()


def tg_get(method: str, params=None):
    response = requests.get(f"{BASE_URL}/{method}", params=params or {}, timeout=70)
    response.raise_for_status()
    return response.json()


def make_keyboard(buttons):
    keyboard_rows = []
    row = []
    for i, button in enumerate(buttons, start=1):
        row.append({"text": button})
        if len(row) == 2:
            keyboard_rows.append(row)
            row = []
    if row:
        keyboard_rows.append(row)

    return {
        "keyboard": keyboard_rows,
        "resize_keyboard": True
    }


def send_message(chat_id: int, text: str, buttons=None):
    payload = {
        "chat_id": chat_id,
        "text": text,
    }
    if buttons:
        payload["reply_markup"] = make_keyboard(buttons)
    tg_post("sendMessage", payload)


def show_menu(chat_id: int, menu_key: str):
    user_state[chat_id] = menu_key
    menu = CATALOG[menu_key]
    send_message(chat_id, menu["title"], menu["buttons"])


def show_product(chat_id: int, product_key: str):
    text = f"""{PRODUCTS[product_key]}

{PAYMENT_TEXT}"""
    send_message(chat_id, text, ["⬅️ رجوع إلى القائمة الرئيسية", "الدعم"])


def handle_message(message: dict):
    chat_id = message["chat"]["id"]
    text = (message.get("text") or "").strip()

    if text == "/start":
        show_menu(chat_id, MAIN_MENU)
        return

    if text == "الدعم":
        send_message(chat_id, f"📩 للتواصل المباشر:\n{SUPPORT_USERNAME}", ["⬅️ رجوع إلى القائمة الرئيسية"])
        return

    if text == "⬅️ رجوع":
        current = user_state.get(chat_id, MAIN_MENU)
        parent = PARENT.get(current, MAIN_MENU)
        show_menu(chat_id, parent)
        return

    if text == "⬅️ رجوع إلى القائمة الرئيسية":
        show_menu(chat_id, MAIN_MENU)
        return

    if text in CATALOG:
        show_menu(chat_id, text)
        return

    if text in PRODUCTS:
        show_product(chat_id, text)
        return

    send_message(chat_id, "اختر من القائمة من فضلك.", CATALOG[MAIN_MENU]["buttons"])


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
                    if "message" in update:
                        handle_message(update["message"])

        except Exception as e:
            print("Error:", e)
            time.sleep(5)


if __name__ == "__main__":
    main()
