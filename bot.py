import telebot
import requests

TOKEN = "ТВОЙ_ТОКЕН_БОТА"
bot = telebot.TeleBot(TOKEN)@bot.message_handler(func=lambda message: True)
def handle_message(message):
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
        
        # Проверяем, есть ли поле choices в ответе
        if "choices" in res_json:
            bot_reply = res_json['choices'][0]['message']['content']
            bot.reply_to(message, bot_reply)
        else:
            # Если DeepSeek вернул ошибку, покажем её текст целиком
            bot.reply_to(message, f"Ответ от DeepSeek без choices: {res_json}")
            
    except Exception as e:
        bot.reply_to(message, f"Ошибка код: {e}")
