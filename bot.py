import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot
import requests

# Получаем ключи из настроек Render
BOT_TOKEN = os.environ.get("BOT_TOKEN")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

# Веб-сервер для удержания порта Render
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Здорово, Максим! Джарвис на связи и готов к работе. Задавай любой вопрос.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Отправляем сообщение пользователя в DeepSeek API
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Ты — Джарвис, толковый и прямой помощник."},
            {"role": "user", "content": message.text}
        ],
        "stream": False
    }
    
    try:
        response = requests.post("https://api.deepseek.com/chat/completions", headers=headers, json=payload, timeout=30)
        res_json = response.json()
        
        # Достаем ответ от нейросети
        bot_reply = res_json['choices'][0]['message']['content']
        bot.reply_to(message, bot_reply)
    except Exception as e:
        bot.reply_to(message, f"Брат, что-то пошло не так с запросом к DeepSeek: {e}")

if __name__ == "__main__":
    bot.infinity_polling()
