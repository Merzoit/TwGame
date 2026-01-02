#!/usr/bin/env python3
"""
Telegram Bot for TwGame
Бот для открытия игрового интерфейса в Telegram
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Настройки логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен бота
TOKEN = '8567389465:AAGf6VKykyl6REaiDz-Vqu2QTacQbvURS7k'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    keyboard = [
        [InlineKeyboardButton("🎮 Играть", callback_data='play_game')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Добро пожаловать в TwGame! 🚀\n\n"
        "Нажмите кнопку ниже, чтобы начать игру:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    await query.answer()

    if query.data == 'play_game':
        # Пока просто показываем сообщение, позже здесь будет ссылка на веб-интерфейс
        await query.edit_message_text(
            text="🎯 Игра запускается...\n\n"
                 "В ближайшее время здесь появится ссылка на игровой интерфейс!"
        )

def main() -> None:
    """Запуск бота"""
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Запускаем бота
    logger.info("Бот запущен!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
