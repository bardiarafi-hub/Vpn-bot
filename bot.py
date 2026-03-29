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
        "title": "👋 مرحباً\nاختر القسم الذي تريده:",
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
    "ChatGPT Plus - 1 شهر - بدون تسجيل دخول - $12.5": "🤖 تجديد اشتراك ChatGPT 5.4\n📦 الخطة: Plus\n📅 المدة: 1 شهر\n🔐 بدون تسجيل دخول\n💵 السعر: $12.5",
    "ChatGPT Plus - 12 شهر - بدون تسجيل دخول - $113": "🤖 تجديد اشتراك ChatGPT 5.4\n📦 الخطة: Plus\n📅 المدة: 12 شهر\n🔐 بدون تسجيل دخول\n💵 السعر: $113",
    "ChatGPT Pro - 1 شهر - بدون تسجيل دخول - $158": "🤖 تجديد اشتراك ChatGPT 5.4\n📦 الخطة: Pro\n📅 المدة: 1 شهر\n🔐 بدون تسجيل دخول\n💵 السعر: $158",
    "ChatGPT Plus - 1 شهر - مع تسجيل دخول - $8.5": "🤖 تجديد اشتراك ChatGPT 5.4\n📦 الخطة: Plus\n📅 المدة: 1 شهر\n📧 مع تسجيل دخول\n💵 السعر: $8.5",
    "ChatGPT Plus - 12 شهر - مع تسجيل دخول - $99": "🤖 تجديد اشتراك ChatGPT 5.4\n📦 الخطة: Plus\n📅 المدة: 12 شهر\n📧 مع تسجيل دخول\n💵 السعر: $99",

    "حساب جاهز ChatGPT Plus - 1 شهر - $10.5": "🆕 إنشاء حساب ChatGPT 5.4\n📦 الخطة: Plus\n📅 المدة: 1 شهر\n✅ حساب جاهز\n💵 السعر: $10.5",
    "ChatGPT Plus على بريدك - 1 شهر - $17": "🆕 إنشاء حساب ChatGPT 5.4\n📦 الخطة: Plus\n📅 المدة: 1 شهر\n📧 على بريدك الإلكتروني\n💵 السعر: $17",
    "حساب جاهز ChatGPT Plus - 12 شهر - $98": "🆕 إنشاء حساب ChatGPT 5.4\n📦 الخطة: Plus\n📅 المدة: 12 شهر\n✅ حساب جاهز\n💵 السعر: $98",
    "ChatGPT Plus على بريدك - 12 شهر - $118": "🆕 إنشاء حساب ChatGPT 5.4\n📦 الخطة: Plus\n📅 المدة: 12 شهر\n📧 على بريدك الإلكتروني\n💵 السعر: $118",
    "حساب جاهز ChatGPT Pro - 12 شهر - $442": "🆕 إنشاء حساب ChatGPT 5.4\n📦 الخطة: Pro\n📅 المدة: 12 شهر\n✅ حساب جاهز\n💵 السعر: $442",
    "ChatGPT Pro على بريدك - 12 شهر - $476": "🆕 إنشاء حساب ChatGPT 5.4\n📦 الخطة: Pro\n📅 المدة: 12 شهر\n📧 على بريدك الإلكتروني\n💵 السعر: $476",

    "WireGuard - 1 شهر - $5": "🌐 WireGuard\n📅 المدة: 1 شهر\n💵 السعر: $5",
    "WireGuard - 3 أشهر - $9": "🌐 WireGuard\n📅 المدة: 3 أشهر\n💵 السعر: $9",
    "WireGuard - 6 أشهر - $16": "🌐 WireGuard\n📅 المدة: 6 أشهر\n💵 السعر: $16",
    "VLESS - 1 شهر - $6": "🌐 VLESS مع 10 مواقع IP\n📅 المدة: 1 شهر\n💵 السعر: $6",
    "VLESS - 3 أشهر - $15": "🌐 VLESS مع 10 مواقع IP\n📅 المدة: 3 أشهر\n💵 السعر: $15",

    "50 Stars - $1.5": "⭐ Telegram Stars\n📦 الكمية: 50 Stars\n💵 السعر: $1.5\n⚡ التوصيل: فوري",
    "100 Stars - $3": "⭐ Telegram Stars\n📦 الكمية: 100 Stars\n💵 السعر: $3\n⚡ التوصيل: فوري",
    "250 Stars - $6": "⭐ Telegram Stars\n📦 الكمية: 250 Stars\n💵 السعر: $6\n⚡ التوصيل: فوري",
    "500 Stars - $11.5": "⭐ Telegram Stars\n📦 الكمية: 500 Stars\n💵 السعر: $11.5\n⚡ التوصيل: فوري",
    "1000 Stars - $22": "⭐ Telegram Stars\n📦 الكمية: 1000 Stars\n💵 السعر: $22\n⚡ التوصيل: فوري",
    "2000 Stars - $40": "⭐ Telegram Stars\n📦 الكمية: 2000 Stars\n💵 السعر: $40\n⚡ التوصيل: فوري",
    "3000 Stars - $60": "⭐ Telegram Stars\n📦 الكمية: 3000 Stars\n💵 السعر: $60\n⚡ التوصيل: فوري",
    "5000 Stars - $90": "⭐ Telegram Stars\n📦 الكمية: 5000 Stars\n💵 السعر: $90\n⚡ التوصيل: فوري",

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
    rows = []
    row = []
    for button in buttons:
        row.append({"text": button})
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)

    return {
        "keyboard": rows,
        "resize_keyboard": True
    }


def send_message(chat_id: int, text: str, buttons=None):
    payload = {"chat_id": chat_id, "text": text}
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
        send_message(
            chat_id,
            f"📩 للتواصل المباشر:\n{SUPPORT_USERNAME}",
            ["⬅️ رجوع إلى القائمة الرئيسية"]
        )
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
