import os
import sys
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from openai import AsyncOpenAI

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

if not TOKEN:
    sys.exit(1)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
client = AsyncOpenAI(api_key=DEEPSEEK_API_KEY or "stub", base_url="https://api.deepseek.com")

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Здорово, Максим! Джарвис на связи.")

@dp.message()
async def chat(message: Message):
    try:
        response = await client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": message.text}],
            stream=False
        )
        await message.answer(response.choices[0].message.content)
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
