import os
import telebot
import requests

# Берем токен из переменных окружения на Render (BOT_TOKEN)
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Ты — Джарвис, умный и верный помощник."},
            {"role": "user", "content": message.text}
        ],
        "stream": False
    }

    try:
        response = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=payload)
        res_json = response.json()
        
        if "choices" in res_json:
            bot_reply = res_json['choices'][0]['message']['content']
            bot.reply_to(message, bot_reply)
        else:
            bot.reply_to(message, "Ошибка ответа от DeepSeek API.")
            
    except Exception as e:
        bot.reply_to(message, f"Ошибка кода: {e}")

if __name__ == "__main__":
    bot.infinity_polling()
