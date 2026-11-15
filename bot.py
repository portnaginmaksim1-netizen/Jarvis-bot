import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from openai import OpenAI

TOKEN = os.getenv("TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

bot = Bot(token=TOKEN)
dp = Dispatcher()

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com",
)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
  await message.answer(
      "Здорова! Джарвис на связи и готов к работе. Чем могу помочь?"
  )


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
        stream=False,
    )
    answer = response.choices[0].message.content
    await message.answer(answer)
  except Exception as e:
    await message.answer(f"Произошла ошибка при обращении к нейросети: {e}")


async def main():
  logging.basicConfig(level=logging.INFO)
  await dp.start_polling(bot)


if __name__ == "__main__":
  asyncio.run(main())
