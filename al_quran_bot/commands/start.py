from telebot import TeleBot
from telebot.types import Message


def register(bot: TeleBot) -> None:
    @bot.message_handler(commands=["start"])
    def send_welcome(message: Message):
        bot.reply_to(message, "Assalomu alaykum!\n/random bosib tasodifiy oyat oling.")
