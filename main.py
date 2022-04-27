import os
import logging

from aiogram import Bot, Dispatcher, types, executor
from Search import find_with, find_without
from dotenv import load_dotenv
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import markups as mkp

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
bot = Bot(token=API_TOKEN)
logging.basicConfig(level=logging.INFO)

dp = Dispatcher(bot, storage=MemoryStorage())


class Form(StatesGroup):
    main_menu = State()
    chords = State()
    lyrics = State()


@dp.message_handler(commands=['start', 'help'], state='*')
async def start(message: types.Message):
    chat_id = message.from_user.id
    await Form.main_menu.set()
    await bot.send_message(
            chat_id=chat_id,
            text="Бот поможет Вам найти строчки песен с аккордами или без!",
            reply_markup=mkp.main_menu
        )


@dp.message_handler(content_types='text', state=Form.main_menu.state)
async def main_menu_state(message: types.Message):
    chat_id = message.from_user.id
    text = message.text
    if text == 'Слова с аккордами':
        await bot.send_message(
            chat_id=chat_id,
            text="Напишите название песни или строчки из нее.",
            reply_markup=mkp.back_menu,
        )
        await Form.chords.set()
    elif text == 'Без аккордов':
        await bot.send_message(
            chat_id=chat_id,
            text="Напишите название песни или строчки из нее.",
            reply_markup=mkp.back_menu
        )
        await Form.lyrics.set()
    else:
        await bot.send_message(
            chat_id=chat_id,
            text="Выберите, что хотите найти."
        )


@dp.message_handler(content_types='text', state=Form.chords.state)
async def send_chords(message: types.Message):
    chat_id = message.from_user.id
    text = message.text
    if text == 'Главное меню':
        await bot.send_message(
            chat_id=chat_id,
            text='Главное меню',
            reply_markup=mkp.main_menu
        )
        await Form.main_menu.set()
    else:
        try:
            await find_with(text)
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


@dp.message_handler(content_types='text', state=Form.lyrics.state)
async def send_lyrics(message: types.Message):
    chat_id = message.from_user.id
    text = message.text
    if text == 'Главное меню':
        await bot.send_message(
            chat_id=chat_id,
            text='Главное меню',
            reply_markup=mkp.main_menu
        )
        await Form.main_menu.set()
    else:
        try:
            await find_without(text)
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
