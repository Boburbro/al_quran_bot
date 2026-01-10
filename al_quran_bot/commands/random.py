from telebot import TeleBot
from telebot.types import Message

from al_quran_bot.quran_client import QuranClient
from al_quran_bot.verse import build_random_verse_payload


def register(bot: TeleBot, client: QuranClient) -> None:
    @bot.message_handler(commands=["random"])
    def send_random(message: Message):
        try:
            caption, image_url = build_random_verse_payload(client)

            if image_url:
                bot.send_photo(
                    message.chat.id,
                    image_url,
                    caption=caption,
                    parse_mode=None,
                )
            else:
                bot.send_message(message.chat.id, caption)
        except Exception as exc:
            print("Xato yuz berdi:", exc)
