# Code by 0xy // TTd // 10.01.22
import os, re, configparser, requests
import urllib
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import urllib.request
from tiktok_downloader import snaptik
from config import *
from keyboard import menu

bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())

def download_video(video_url, name):
    r = requests.get(video_url, allow_redirects=True)
    content_type = r.headers.get('content-type')
    if content_type == 'video/mp4':
        open(f'./videos/video{name}.mp4', 'wb').write(r.content)
    else:
        pass

if not os.path.exists('videos'):
    os.makedirs('videos')
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text='Приветствую тебя в боте!\nТут ты можешь скачать видео из TikTok, без водяного знака!\nПросто пришли мне ссылку на видео!')

@dp.message_handler(text="Скачать")
async def help_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text='Отправьте ссылку на видео TikTok.')

@dp.message_handler(content_types=['text'])
async def text(message: types.Message):
    if message.text.startswith('https://www.tiktok.com'):
        await bot.send_message(chat_id=message.chat.id, text='Ссылка принята!\nОжидайте скачаного видео!')
        print('Принят запрос от: ', message.from_user.id)
        video_url = message.text
        try:
            snaptik(video_url).get_media()[0].download(f"./videos/result_{message.from_user.id}.mp4")
            path = f'./videos/result_{message.from_user.id}.mp4'
            with open(f'./videos/result_{message.from_user.id}.mp4', 'rb') as file:
                await bot.send_video(
                    chat_id=message.chat.id,
                    video=file,
                    caption='Ваше видео скаченно!'
                    )
            os.remove(path)
            print('Скаченное видео отправлено: ', message.from_user.id)
        except:
            await bot.send_message(chat_id=message.chat.id, text='Ошибка при скачивании, видео не найдено или удалено.',  reply_markup = menu())
    elif message.text.startswith('https://vm.tiktok.com') or message.text.startswith('http://vm.tiktok.com'):
        await bot.send_message(chat_id=message.chat.id, text='Ссылка принята!\nОжидайте скаченного видео!')
        video_url = message.text
        print('Принят запрос от: ', message.from_user.id)
        try:
            snaptik(video_url).get_media()[0].download(f"./videos/result_{message.from_user.id}.mp4")
            path = f'./videos/result_{message.from_user.id}.mp4'
            with open(f'./videos/result_{message.from_user.id}.mp4', 'rb') as file:
                await bot.send_video(
                    chat_id=message.chat.id,
                    video=file,
                    caption='Ваше видео скаченно!'
                    )
            os.remove(path)
            print('Скаченное видео отправлено: ', message.from_user.id)
        except:
            await bot.send_message(chat_id=message.chat.id, text='Ошибка при скачивании, видео не найдено или удалено.',  reply_markup = menu())
    else:
        await bot.send_message(chat_id=message.chat.id, text='Ссылка не распознана, отправьте корректную ссылку.',  reply_markup = menu())
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)