from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

TOKEN = os.environ.get("TOKEN")

keyboard = [["خرید VPN", "پشتیبانی"]]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("به ربات فروش خوش اومدی 🔥", reply_markup=reply_markup)

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "خرید VPN":
        await update.message.reply_text(
            "🔐 اشتراک AnyConnect\n\n"
            "📅 مدت: 1 ماهه\n"
            "⚡ حجم: نامحدود\n"
            "💰 قیمت: 12,000,000 تومان\n\n"
            "💳 پرداخت: فقط ارز دیجیتال\n"
            "📩 برای خرید پیام بده:\n"
            "@Natar100"
        )

    elif text == "پشتیبانی":
        await update.message.reply_text("آیدی پشتیبانی: @Natar100")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

app.run_polling()
