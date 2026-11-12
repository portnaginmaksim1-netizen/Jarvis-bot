
import logging
import sys
import os
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from openai import AsyncOpenAI

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Получаем ключи из безопасных переменных окружения Render
TOKEN = os.getenv("TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

if not TOKEN:
    print("Ошибка: Токен Telegram не задан в переменных окружения!")
    sys.exit(1)

# Инициализация бота и клиента DeepSeek
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

client = AsyncOpenAI(
    api_key=DEEPSEEK_API_KEY if DEEPSEEK_API_KEY else "stub",
    base_url="https://api.deepseek.com"
)

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Здорово, Максим! Джарвис на связи и готов к работе.")

@dp.message()
async def chat_with_deepseek(message: Message):
    if not DEEPSEEK_API_KEY:
        await message.answer("Брат, на Render еще не добавлен DEEPSEEK_API_KEY в настройках!")
        return
        
    try:
        response = await client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Ты — Джарвис, умный и верный помощник."},
                {"role": "user", "content": message.text}
            ],
            stream=False
        )
        answer = response.choices[0].message.content
        await message.answer(answer)
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
