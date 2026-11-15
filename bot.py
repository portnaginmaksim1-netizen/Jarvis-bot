import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot

# Получаем ключи из настроек Render
BOT_TOKEN = os.environ.get("BOT_TOKEN")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

# Веб-сервер, чтобы Render был доволен портом и не вырубал бота
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

# Запускаем сервер в фоне
server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

# Твои команды бота
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Здорово! Я на связи и готов работать.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Здесь логика общения с DeepSeek
    bot.reply_to(message, f"Ты написал: {message.text}")

if __name__ == "__main__":
    bot.infinity_polling()
