from aiogram.types.reply_keyboard import KeyboardButton, ReplyKeyboardMarkup


def generatemainmenubutton():

    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(
        KeyboardButton(text='⛅️ Ob-havo'),
        KeyboardButton(text='💰 Valyuta ayirboshlash'),
        KeyboardButton(text='🖼️ Rasmlar')
    )

    return markup




def genratebackbutton():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(
        KeyboardButton(text='⬅️ Orqaga')
    )
    return markup