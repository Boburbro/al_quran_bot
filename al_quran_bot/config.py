import os

from dotenv import load_dotenv


def load_env() -> None:
    """Load environment variables from `.env` if present."""

    load_dotenv()


def get_bot_token() -> str:
    token = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN yoki TELEGRAM_BOT_TOKEN .env faylida topilmadi")
    return token


def get_channel_id() -> int | str | None:
    """Optional Telegram channel/chat id for daily posting.

    Examples:
    - -100123... (private channel id)
    - @my_channel (public username)
    """

    raw = (
        os.getenv("TELEGRAM_CHANNEL_ID")
        or os.getenv("CHANNEL_ID")
        or os.getenv("TELEGRAM_CHAT_ID")
    )
    if not raw:
        return None

    raw = raw.strip()
    if raw.lstrip("-").isdigit():
        return int(raw)
    return raw


def get_admin_id() -> int | None:
    """Telegram ID of the admin who approves posts."""
    raw = os.getenv("ADMIN")
    if not raw:
        return None
    raw = raw.strip()
    if raw.isdigit():
        return int(raw)
    return None
