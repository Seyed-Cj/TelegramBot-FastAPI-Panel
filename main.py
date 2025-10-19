import os
import threading
import uvicorn

from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import telebot

STATUS_FILE = "bot_status.txt"
ADMIN_TOKEN = "1"  # admin password
TELEGRAM_TOKEN = "7789655247:AAEXe7TdjR3D3vN5E9xrUJylO8RDEih0niA"

def load_status() -> bool:
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as f:
            return f.read().strip() == "active"
    return False

def save_status(active: bool):
    with open(STATUS_FILE, "w") as f:
        f.write("active" if active else "inactive")

class BotStatus:
    def __init__(self):
        self._lock = threading.Lock()
        self._active = load_status()
        self._polling_thread = None
        self.bot = telebot.TeleBot(TELEGRAM_TOKEN)
        self._register_handlers()

    def _register_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start_handler(message):
            if self.is_active():
                self.bot.reply_to(message, "Bot is active!")

        @self.bot.message_handler(func=lambda m: True)
        def echo_handler(message):
            if self.is_active():
                self.bot.reply_to(message, message.text)

    def is_active(self) -> bool:
        with self._lock:
            return self._active

    def set_active(self, active: bool):
        with self._lock:
            if self._active == active:
                return
            self._active = active
            save_status(active)

            if active:
                if not self._polling_thread or not self._polling_thread.is_alive():
                    self._polling_thread = threading.Thread(target=self._start_polling, daemon=True)
                    self._polling_thread.start()
            else:
                try:
                    self.bot.stop_polling()
                except Exception:
                    pass
                self._polling_thread = None

    def _start_polling(self):
        try:
            self.bot.polling(non_stop=True, interval=0, timeout=10)
        except Exception:
            pass

bot_status = BotStatus()

app = FastAPI()
security = HTTPBearer()

class StatusResponse(BaseModel):
    status: str

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.credentials != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")
    return credentials.credentials

@app.get("/bot/status", response_model=StatusResponse)
def get_status():
    return {"status": "active" if bot_status.is_active() else "inactive"}

@app.post("/bot/on")
def turn_on(token: str = Depends(verify_token)):
    bot_status.set_active(True)
    return {"message": "Bot turned on"}

@app.post("/bot/off")
def turn_off(token: str = Depends(verify_token)):
    bot_status.set_active(False)
    return {"message": "Bot turned off"}

app.mount("/", StaticFiles(directory=".", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)