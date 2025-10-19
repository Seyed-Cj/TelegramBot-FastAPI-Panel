# Telegram Bot Control Panel

A simple FastAPI-based web panel to manage a Telegram bot (turn on/off) with persistent status.

## Features
- Start/stop the bot via HTTP endpoints
- Check current bot status
- Simple web panel via static files

## Installation
1. Clone the repository:
```bash
git clone [https://github.com/Seyed-Cj/TelegramBot-FastAPI-Panel.git](https://github.com/Seyed-Cj/TelegramBot-FastAPI-Panel.git)
cd TelegramBot-FastAPI-Panel
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

4. Access the web panel at [http://127.0.0.1:8000](http://127.0.0.1:8000)

## API Endpoints
- `GET /bot/status` – Check bot status (`active`/`inactive`)
- `POST /bot/on` – Turn the bot on (requires admin token)
- `POST /bot/off` – Turn the bot off (requires admin token)