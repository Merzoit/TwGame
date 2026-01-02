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
        # Отправляем ссылку на веб-интерфейс игры
        keyboard = [
            [InlineKeyboardButton("🎮 Открыть игру", url="https://twgame-production.up.railway.app/")],
            [InlineKeyboardButton("⬅️ Назад", callback_data='back_to_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text="🎯 TwGame готова к игре!\n\n"
                 "Нажмите кнопку ниже, чтобы открыть игровой интерфейс:",
            reply_markup=reply_markup
        )

    elif query.data == 'back_to_menu':
        keyboard = [
            [InlineKeyboardButton("🎮 Играть", callback_data='play_game')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text="Добро пожаловать в TwGame! 🚀\n\n"
                 "Нажмите кнопку ниже, чтобы начать игру:",
            reply_markup=reply_markup
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
