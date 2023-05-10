from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
from aiogram.types import Message

load_dotenv()
import os

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class Weather(StatesGroup):
    city = State()


class ConvertValut(StatesGroup):
    fromvalut = State()
    amount = State()
    tovalut = State()


from getpctutefunction import getpicture
from keboards import generatemainmenubutton, genratebackbutton
from getweatherinfofunction import getweatherinfo
from getconvertvalutfunction import getconvertvalut

bot = Bot(os.getenv('telegramtoken'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands='start')
async def start(message: Message):
    await message.answer('Xush kelibsiz', reply_markup=generatemainmenubutton())


@dp.message_handler(text='⛅️ Ob-havo')
async def sendresponse(message: Message):
    await message.answer('Shahar kiriting: ', reply_markup=genratebackbutton())
    await Weather.city.set()


@dp.message_handler(state=Weather.city)
async def sendweatherinfo(message: Message, state: FSMContext):
    city = message.text
    if city == '⬅️ Orqaga' or city == '/start':
        await state.finish()
        await message.answer('Kategoriyani tanlang: ', reply_markup=generatemainmenubutton())
    else:
        text = getweatherinfo(city)
        if len(text) == 2:
            info, image = text
            await message.answer_photo(photo=image, caption=info)
        else:
            await message.answer(text)


@dp.message_handler(text='🖼️ Rasmlar')
# @dp.message_handler(lambda message: 'Rasmlar' in message.text)
async def randompicture(message: Message):
    link = getpicture()
    # await message.answer(link)
    await message.answer_photo(photo=link)


@dp.message_handler(text='💰 Valyuta ayirboshlash')
async def convertvalut(message: Message):

    # data = getsymols()
    text = ''
    # print(data)
    # for key, val in data['symbols'].items():
    #     text += f'{key} - {val} \n'
    #
    #
    # await message.answer(f'{text}\nQaysi valyutadan: ', reply_markup=genratebackbutton())

    await message.answer('Qaysi valyutadan: ', reply_markup=genratebackbutton())
    await ConvertValut.fromvalut.set()


@dp.message_handler(state=ConvertValut.fromvalut)
async def getfromvalut(message: Message, state: FSMContext):



    await message.answer('Summani kiriting')
    if message.text == '⬅️ Orqaga' or message.text == '/start':
        await message.answer('Bosh menu', reply_markup=generatemainmenubutton())
        await state.finish()
    else:
        await state.update_data({'fromvalut': message.text})
        await ConvertValut.amount.set()


@dp.message_handler(state=ConvertValut.amount)
async def getamunt(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data({'amount': message.text})
        await message.answer('Qaysi valyutaga: ')
        await ConvertValut.tovalut.set()
    elif message.text == '⬅️ Orqaga' or message.text == '/start':
        await message.answer('Bosh menu', reply_markup=generatemainmenubutton())
        await state.finish()
    else:
        await ConvertValut.amount.set()


@dp.message_handler(state=ConvertValut.tovalut)
async def gettovalut(message: Message, state: FSMContext):
    if message.text == '⬅️ Orqaga' or message.text == '/start':
        await message.answer('Bosh menu', reply_markup=generatemainmenubutton())
        await state.finish()
    else:

        await state.update_data({'tovalut': message.text})

        data = await state.get_data()

        fromvalut = data['fromvalut']
        amount = data['amount']
        tovalut = data['tovalut']

        convert, statuscode = getconvertvalut(fromvalut, tovalut, amount)


        if statuscode == 200:
            timestamp = convert['info']['timestamp']
            rate = convert['info']['rate']
            date = convert['date']
            result = convert['result']
            text = f'So\'ralgan vaqt: {timestamp}\n' \
                   f'1 {fromvalut}: {rate} {tovalut}\n' \
                   f'Sana: {date}\n' \
                   f'Qayerdan: {fromvalut}\n' \
                   f'Qayerga: {tovalut}\n' \
                   f'Natija: {amount} {fromvalut} = {result} {tovalut}'
            await message.answer(text, reply_markup=generatemainmenubutton())
            await state.finish()
        else:
            await message.answer('Xatolik')
            await state.finish()

executor.start_polling(dp, skip_updates=True)
