import threading
import time
from dataclasses import dataclass

from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from al_quran_bot.quran_client import QuranClient
from al_quran_bot.verse import build_random_verse_payload


@dataclass(frozen=True)
class DailyPosterConfig:
    channel_id: int | str
    admin_id: int | None = None
    interval_seconds: int = 60 * 60 * 14
    retry_delay_seconds: int = 5


def _send_once(bot: TeleBot, client: QuranClient, config: DailyPosterConfig) -> None:
    caption, image_url = build_random_verse_payload(client)

    target_id = config.admin_id or config.channel_id
    reply_markup = None

    if config.admin_id:
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("Tasdiqlash ✅", callback_data="approve_post"),
            InlineKeyboardButton("Rad etish ❌", callback_data="reject_post"),
        )
        reply_markup = markup

    if image_url:
        bot.send_photo(
            target_id,
            image_url,
            caption=caption,
            parse_mode=None,
            reply_markup=reply_markup,
        )
    else:
        bot.send_message(target_id, caption, reply_markup=reply_markup)


def start_daily_poster(
    bot: TeleBot, client: QuranClient, config: DailyPosterConfig
) -> None:
    def loop() -> None:
        while True:
            sent = False
            while not sent:
                try:
                    _send_once(bot, client, config)
                    sent = True
                except Exception as exc:
                    print("Daily poster error:", exc)
                    time.sleep(1)

            time.sleep(max(60, int(config.interval_seconds)))

    thread = threading.Thread(target=loop, name="daily_poster", daemon=True)
    thread.start()


def register_daily_poster_callbacks(
    bot: TeleBot, client: QuranClient, config: DailyPosterConfig
) -> None:
    @bot.callback_query_handler(
        func=lambda call: call.data in ["approve_post", "reject_post"]
    )
    def handle_approval(call):
        if config.admin_id and call.from_user.id != config.admin_id:
            bot.answer_callback_query(call.id, "Siz admin emassiz!", show_alert=True)
            return

        if call.data == "approve_post":
            try:
                bot.copy_message(
                    config.channel_id,
                    call.message.chat.id,
                    call.message.message_id,
                )
                bot.edit_message_reply_markup(
                    call.message.chat.id, call.message.message_id, reply_markup=None
                )
                bot.answer_callback_query(call.id, "Kanalga yuborildi ✅")
                bot.send_message(
                    call.message.chat.id,
                    "Tasdiqlandi va kanalga yuborildi.",
                    reply_to_message_id=call.message.message_id,
                )
            except Exception as exc:
                bot.answer_callback_query(call.id, f"Xato: {exc}", show_alert=True)

        elif call.data == "reject_post":
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
                bot.answer_callback_query(
                    call.id, "Rad etildi ❌. Yangisi olinmoqda..."
                )
                _send_once(bot, client, config)
            except Exception as exc:
                bot.answer_callback_query(call.id, f"Xato: {exc}", show_alert=True)
