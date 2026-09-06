import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 6585612596
CHANNEL = "@mehrban91191"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 ثبت سفارش تبلیغ", callback_data="order")],
        [InlineKeyboardButton("💰 تعرفه تبلیغات", callback_data="price")],
        [InlineKeyboardButton("☎️ پشتیبانی", callback_data="support")]
    ]

    await update.message.reply_text(
        "سلام 🌹\n"
        "به ربات تبلیغات خوش آمدید.\n\n"
        "یکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "order":
        context.user_data["ordering"] = True
        await query.message.reply_text(
            "📝 متن تبلیغ خود را ارسال کنید.\n"
            "سپس عکس یا ویدئو و لینک را بفرستید.\n\n"
            "برای پایان سفارش بنویسید: پایان سفارش"
        )

    elif query.data == "price":
        await query.message.reply_text(
            "💰 تعرفه تبلیغات\n\n"
            "تعرفه‌ها به‌زودی اعلام می‌شود."
        )

    elif query.data == "support":
        await query.message.reply_text(
            "☎️ برای پشتیبانی پیام خود را ارسال کنید."
        )

async def receive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("ordering"):
        return

    if update.message.text and update.message.text == "پایان سفارش":
        context.user_data["ordering"] = False
        await update.message.reply_text(
            "✅ سفارش شما دریافت شد.\n"
            "پس از بررسی، نتیجه به شما اعلام می‌شود."
        )
        return

    await update.message.forward(chat_id=ADMIN_ID)
    await update.message.reply_text("✅ دریافت شد.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.ALL, receive))

    app.run_polling()

if __name__ == "__main__":
    main()
