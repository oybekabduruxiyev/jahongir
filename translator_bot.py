from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from deep_translator import GoogleTranslator

BOT_TOKEN = "8436543045:AAFEdKJ829OHQHIG8nB3XiGWijXrcdZATSA"  # 👉 bu yerga tokeningni qo'y

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [KeyboardButton("🇺🇿 O'zbek → Ingliz"), KeyboardButton("🇬🇧 Ingliz → O'zbek")]
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    
    await update.message.reply_text(
        "👋 Salom! Men *Tarjimon Bot*man.\n\n"
        "Men quyidagi tillar orasida tarjima qila olaman:\n"
        "🇺🇿 O'zbek tili ↔ 🇬🇧 Ingliz tili\n\n"
        "Tarjima qilish uchun matn yuboring yoki yo'nalishni tanlang.",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def translate_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    direction = context.user_data.get("direction", "uz_en")

    if text == "🇺🇿 O'zbek → Ingliz":
        context.user_data["direction"] = "uz_en"
        await update.message.reply_text("✅ Endi O'zbek tilidan Ingliz tiliga tarjima qilaman.")
        return
    elif text == "🇬🇧 Ingliz → O'zbek":
        context.user_data["direction"] = "en_uz"
        await update.message.reply_text("✅ Endi Ingliz tilidan O'zbek tiliga tarjima qilaman.")
        return

    if direction == "uz_en":
        result = GoogleTranslator(source="uz", target="en").translate(text)
    else:
        result = GoogleTranslator(source="en", target="uz").translate(text)

    await update.message.reply_text(
        f"🔤 *Tarjima natijasi:*\n{result}\n\n👨‍💻 *Tarjimon yaratuvchisi:* Jahongir 💫",
        parse_mode="Markdown"
    )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate_message))
    app.run_polling()

if __name__ == "__main__":
    main()
