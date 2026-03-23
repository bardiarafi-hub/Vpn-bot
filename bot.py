from telegram import Update, LabeledPrice, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, PreCheckoutQueryHandler

TOKEN = "8658642141:AAHASLWEnVX6uGaAiBq55ENzhua11JXfW-k"

user_mode = {}

keyboard = [
    ["Stars با خرید", "خرید کریپتو"],
    ["خرید VPN", "پشتیبانی"]
]

reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# شروع
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 به ربات فروش خوش اومدی\n\nروش خرید رو انتخاب کن:",
        reply_markup=reply_markup
    )


# مدیریت پیام‌ها
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id

    # انتخاب استارز
    if text == "Stars با خرید":
        user_mode[user_id] = "stars"
        await update.message.reply_text("⭐️ پرداخت با Stars انتخاب شد")

    # خرید VPN
    elif text == "خرید VPN":
        if user_mode.get(user_id) == "stars":
            await update.message.reply_invoice(
                title="VPN AnyConnect 🔐",
                description="اشتراک 1 ماهه",
                payload="vpn_1",
                provider_token="",
                currency="XTR",
                prices=[LabeledPrice("اشتراک VPN", 4000)],
            )
        else:
            await update.message.reply_text(
                f"💳 پرداخت فقط با ارز دیجیتال\n\nبرای هماهنگی:\n{SUPPORT_USERNAME}"
            )

    # پشتیبانی
    elif text == "پشتیبانی":
        await update.message.reply_text(f"📩 {SUPPORT_USERNAME}")


# تایید قبل پرداخت
async def precheckout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.pre_checkout_query
    await query.answer(ok=True)


# بعد از پرداخت موفق
async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ پرداخت با موفقیت انجام شد\n\n📩 حالا برای دریافت اکانت به پشتیبانی پیام دهید:\n@Natar100"
    )


# اجرای بات
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(PreCheckoutQueryHandler(precheckout))
app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))

app.run_polling()
