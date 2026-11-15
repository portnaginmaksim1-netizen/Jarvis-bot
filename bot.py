import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from openai import OpenAI

TOKEN = os.getenv("TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

bot = Bot(token=TOKEN)
dp = Dispatcher()

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
  await message.answer("Здорова! Джарвис на связи.")


@dp.message()
async def handle_message(message: types.Message):
  try:
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": "Ты — умный и верный ассистент Джарвис.",
            },
            {"role": "user", "content": message.text},
        ],
    )
    await message.answer(response.choices[0].message.content)
  except Exception as e:
    await message.answer(f"Ошибка: {e}")


async def main():
  await dp.start_polling(bot)


if __name__ == "__main__":
  asyncio.run(main())
