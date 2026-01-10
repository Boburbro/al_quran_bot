# Al Quran Bot

A Telegram bot that provides random Quran verses and supports automated daily posting to a channel with an admin approval workflow. The bot interface is currently in Uzbek.

## Features

- **Random Verse**: Get a random verse from the Quran using the `/random` command.
- **Daily Posting**: Automatically posts a random verse to a configured Telegram channel every ~14 hours.
- **Admin Approval**: (Optional) If an Admin ID is configured, daily posts are sent to the admin for approval (Approve/Reject) before being posted to the channel.
- **Image Support**: Sends an image of the verse if available, otherwise sends text.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/al_quran_bot.git
   cd al_quran_bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Create a `.env` file in the root directory (or rename a copy of `.env.example` if available) and add the following environment variables:

| Variable | Description | Required |
|----------|-------------|----------|
| `BOT_TOKEN` | Your Telegram Bot API Token (from @BotFather) | Yes |
| `CHANNEL_ID` | Channel ID (e.g., `-100...`) or Username (`@channel`) for auto-posting | No (required for auto-posting) |
| `ADMIN` | Telegram User ID of the admin who approves posts | No (optional) |

### Example `.env` file
```dotenv
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
CHANNEL_ID=@my_quran_channel
ADMIN=987654321
```

## Usage

Run the bot:

```bash
python bot.py
```

### Commands

- `/start` - Start the bot and receive a welcome message.
- `/random` - Receive a random Quran verse.

## Development

The main entry point is `bot.py`. The core logic is within the `al_quran_bot/` package.
- `app.py`: Bot initialization and configuration.
- `daily_poster.py`: Logic for the background thread that handles daily posts.
- `commands/`: Handler functions for bot commands.

## License

[MIT](LICENSE)
