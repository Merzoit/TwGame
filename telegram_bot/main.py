#!/usr/bin/env python3
"""
Telegram Bot for TwGame
Бот для открытия игрового интерфейса в Telegram
"""

import logging
import os
import sys
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Инициализация Django
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'game_app'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twgame.settings')

import django
django.setup()

from django.utils import asyncio as django_asyncio
from asgiref.sync import sync_to_async
from game.services import PlayerService

# Настройки логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Логируем доступные переменные окружения (для диагностики)
import os
db_vars = {k: v for k, v in os.environ.items() if 'database' in k.lower() or 'db' in k.lower() or 'railway' in k.lower()}
if db_vars:
    logger.info(f"Database-related environment variables: {db_vars}")
else:
    logger.info("No database-related environment variables found")

# Проверяем подключение к базе данных
try:
    from django.db import connection
    cursor = connection.cursor()
    logger.info("Database connection successful")
except Exception as e:
    logger.error(f"Database connection failed: {e}")

# Логируем DATABASE_URL и другие возможные варианты
database_url = os.environ.get('DATABASE_URL')
railway_db_url = os.environ.get('RAILWAY_DATABASE_URL')
postgres_url = os.environ.get('POSTGRES_URL')

if database_url:
    logger.info(f"DATABASE_URL is set (length: {len(database_url)})")
elif railway_db_url:
    logger.info(f"RAILWAY_DATABASE_URL is set (length: {len(railway_db_url)})")
    # Устанавливаем DATABASE_URL для Django
    os.environ['DATABASE_URL'] = railway_db_url
elif postgres_url:
    logger.info(f"POSTGRES_URL is set (length: {len(postgres_url)})")
    os.environ['DATABASE_URL'] = postgres_url
else:
    logger.warning("No database URL variables found")

# Токен бота
TOKEN = '8567389465:AAGf6VKykyl6REaiDz-Vqu2QTacQbvURS7k'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    user = update.effective_user

    # Создаем или получаем игрока из базы данных
    try:
        # Используем sync_to_async для работы с Django ORM в асинхронном контексте
        player, created = await sync_to_async(PlayerService.get_or_create_player)(
            telegram_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )

        if created:
            welcome_message = (
                f"🎉 Добро пожаловать в TwGame, {user.first_name or 'игрок'}!\n\n"
                "Вы успешно зарегистрированы в игре!\n"
                "Ваш профиль создан, и вы готовы начать приключение.\n\n"
            )
        else:
            profile = player.profile
            welcome_message = (
                f"🎮 С возвращением в TwGame, {user.first_name or 'игрок'}!\n\n"
                f"📊 Ваш уровень: {profile.level}\n"
                f"💰 Золото: {profile.gold}\n"
                f"🏆 Побед: {profile.wins}/{profile.total_games}\n\n"
            )

        keyboard = [
            [InlineKeyboardButton("🎮 Играть", callback_data='play_game')],
            [InlineKeyboardButton("👤 Профиль", callback_data='show_profile')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        welcome_message += "Выберите действие:"

        await update.message.reply_text(
            welcome_message,
            reply_markup=reply_markup
        )

    except Exception as e:
        logger.error(f"Ошибка при создании игрока: {e}")
        await update.message.reply_text(
            "❌ Произошла ошибка при регистрации. Попробуйте позже."
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    await query.answer()

    user = query.from_user

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

    elif query.data == 'show_profile':
        # Показываем профиль игрока
        try:
            profile = await sync_to_async(PlayerService.get_player_profile)(user.id)
            if profile:
                profile_text = (
                    f"👤 Ваш профиль:\n\n"
                    f"📊 Уровень: {profile.level}\n"
                    f"⭐ Опыт: {profile.experience}\n"
                    f"💰 Золото: {profile.gold}\n"
                    f"🎮 Игр сыграно: {profile.total_games}\n"
                    f"🏆 Побед: {profile.wins}\n"
                    f"❌ Поражений: {profile.losses}\n"
                    f"📈 Процент побед: {profile.win_rate}%\n\n"
                    f"🕐 Последний вход: {profile.last_login.strftime('%d.%m.%Y %H:%M')}"
                )
            else:
                profile_text = "❌ Профиль не найден. Попробуйте перезапустить бота командой /start"

            keyboard = [
                [InlineKeyboardButton("⬅️ Назад", callback_data='back_to_menu')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(
                text=profile_text,
                reply_markup=reply_markup
            )

        except Exception as e:
            logger.error(f"Ошибка при получении профиля: {e}")
            await query.edit_message_text(
                text="❌ Ошибка при загрузке профиля. Попробуйте позже.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("⬅️ Назад", callback_data='back_to_menu')
                ]])
            )

    elif query.data == 'back_to_menu':
        # Возвращаемся в главное меню
        try:
            player = await sync_to_async(PlayerService.get_player_by_telegram_id)(user.id)
            if player:
                profile = player.profile
                welcome_message = (
                    f"🎮 С возвращением в TwGame, {user.first_name or 'игрок'}!\n\n"
                    f"📊 Ваш уровень: {profile.level}\n"
                    f"💰 Золото: {profile.gold}\n\n"
                )
            else:
                welcome_message = "Добро пожаловать в TwGame! 🚀\n\n"

            keyboard = [
                [InlineKeyboardButton("🎮 Играть", callback_data='play_game')],
                [InlineKeyboardButton("👤 Профиль", callback_data='show_profile')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            welcome_message += "Выберите действие:"

            await query.edit_message_text(
                text=welcome_message,
                reply_markup=reply_markup
            )

        except Exception as e:
            logger.error(f"Ошибка при возврате в меню: {e}")
            keyboard = [
                [InlineKeyboardButton("🎮 Играть", callback_data='play_game')],
                [InlineKeyboardButton("👤 Профиль", callback_data='show_profile')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(
                text="Добро пожаловать в TwGame! 🚀\n\nВыберите действие:",
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
