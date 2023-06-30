from aiogram import types, executor, Dispatcher, Bot
from aiogram.types import CallbackQuery, \
    ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
import requests
import json

city = ''
bot = Bot('YOUR_TOKEN_HERE')
dp = Dispatcher(bot)
API = '937c436168e04ddb0b394d51605288dd'
@dp.message_handler(commands=['start'])
async def hi(message: types.Message):
    global city
    cities = types.InlineKeyboardMarkup(row_width=2)
    cities.add(InlineKeyboardButton('London', callback_data='London'),
               InlineKeyboardButton('Bishkek', callback_data='Bishkek'),
               InlineKeyboardButton('Moscow', callback_data='Moscow'))
    # await call.message.answer('првет я погоду говорю', reply_markup=cities)    await message.reply('првет я погоду говорю', reply_markup=cities)


@dp.message_handler(content_types=['text'])
async def get_weather(message: types.Message, call_city=None):
    global city
    city = message.text.strip().lower() if not call_city else call_city.lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    data = json.loads(res.text)
    temp = data['main']['temp']
    await message.reply(f'щас погода {temp}')


@dp.callback_query_handler(lambda call: True)
async def callback_worker(call: CallbackQuery):
    call_city = None
    if call.data == 'London':
        call_city = 'London'
    if call.data == 'Bishkek':
        call_city = 'Bishkek'
    if call.data == "Moscow":
        call_city = 'Moscow'
    await get_weather(call.message, call_city)
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)