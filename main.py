import os
import logging

from aiogram import Bot, Dispatcher, types, executor
from Search import find
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
bot = Bot(token=API_TOKEN)
logging.basicConfig(level=logging.INFO)

dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    chat_id = message.from_user.id
    await bot.send_message(
        chat_id=chat_id,
        text="Напишите название песни или строчки из нее.",
    )


@dp.message_handler(content_types='text')
async def send_chords(message: types.Message):
    chat_id = message.from_user.id
    message = message.text
    try:
        await find(message)
        f = open('file.txt')
        read = f.read()
        if len(read) > 4095:
            for x in range(0, len(read), 4095):
                await bot.send_message(
                    chat_id=chat_id,
                    text=read[x:x + 4095]
                )
        else:
            await bot.send_message(
                chat_id=chat_id,
                text=read
            )
        f.close()
        os.remove("file.txt")
    except Exception as e:
        await bot.send_message(
            chat_id=chat_id,
            text="По Вашему запросу ничего не найдено. Попробуйте добавить фамилию автора"
        )
        print(e)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
