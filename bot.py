# bot.py
import os
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from app.schemas import run_conversation, user_contexts

TOKEN = os.environ['TELEGRAM_API_KEY']
# Initialize bot and dispatcher
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
last_assistant_responses = {}

@dp.message(Command("start"))
async def cmd_start(message: Message):
    user_contexts[message.from_user.id] = []
    await message.answer(
        "Привет!  Я ваш ассистент в поиске квартир в аренду и автомобилей")


@dp.message(Command("contact_to_owner"))
async def send_welcome(message: Message):
    user_id = '1420580290'
    assistant_response = last_assistant_responses.get(message.from_user.id, "No previous assistant response available.")
    await bot.send_message(user_id, text=f"Добрый день ваши машину хотят купить + {assistant_response}")



@dp.message()
async def process_message(message: Message):
    user_id = message.from_user.id
    question = message.text
    response = run_conversation(user_id, question)
    if response:
        assistant_content = str(response.choices[0].message.content)
        last_assistant_responses[user_id] = assistant_content
        await message.answer(assistant_content)
    else:
        await message.answer("Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте снова позже.")
