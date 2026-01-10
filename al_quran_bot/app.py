import telebot

from al_quran_bot.commands import register_random, register_start
from al_quran_bot.config import get_admin_id, get_bot_token, get_channel_id, load_env
from al_quran_bot.daily_poster import (
    DailyPosterConfig,
    register_daily_poster_callbacks,
    start_daily_poster,
)
from al_quran_bot.quran_client import QuranClient


def create_bot() -> telebot.TeleBot:
    load_env()

    bot = telebot.TeleBot(get_bot_token(), parse_mode="HTML")
    client = QuranClient()

    register_start(bot)
    register_random(bot, client)

    channel_id = get_channel_id()
    admin_id = get_admin_id()
    if channel_id is not None:
        config = DailyPosterConfig(channel_id=channel_id, admin_id=admin_id)
        start_daily_poster(bot, client, config)
        register_daily_poster_callbacks(bot, client, config)

    return bot


def run() -> None:
    bot = create_bot()
    bot.infinity_polling(skip_pending=True)
