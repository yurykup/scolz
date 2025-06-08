from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")  # безопасно тянем токен из переменных

menu = {
    "🍔 Еда": [
        ("Пицца", "3 поцелуя"),
        ("Блинчики", "2 обнимашки"),
        ("Шоколадка", "1 щечку поцеловать")
    ],
    "💆 Услуги": [
        ("Массаж спины", "5 поцелуев"),
        ("Погладить волосы", "3 обнимашки"),
        ("Усыпить под сериал", "4 обнимашки")
    ],
    "🎁 Бонусы": [
        ("Сюрприз", "7 обнимашек и 5 поцелуев"),
        ("Плед + чай", "4 обнимашки"),
        ("Желание", "10 поцелуев ❤️")
    ]
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(cat, callback_data=f"category|{cat}")]
        for cat in menu
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привет, солнышко 💖\nВыбери, что хочешь сегодня 😊", reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    if data.startswith("category|"):
        cat = data.split("|")[1]
        items = menu[cat]
        keyboard = [
            [InlineKeyboardButton(f"{name} — {price}", callback_data=f"item|{name}|{price}")]
            for name, price in items
        ]
        keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="back")])
        await query.edit_message_text(
            text=f"📋 {cat}:\nВыбери, что хочешь 💞",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif data.startswith("item|"):
        name, price = data.split("|")[1:]
        await query.edit_message_text(
            text=f"Ты выбрала *{name}* 🥰\nСтоимость: _{price}_\n\nОплата принимается прямо сейчас! 💋",
            parse_mode="Markdown"
        )
    elif data == "back":
        await start(update, context)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()
