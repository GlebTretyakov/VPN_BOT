from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

btnProfile = KeyboardButton('Профиль')
btnSub = KeyboardButton('Купить / продлить подписку')
btnList = KeyboardButton('Помощь')
#btnPromo = KeyboardButton('Пробная подписка')
btnPromo = KeyboardButton('Пробная подписка')
mainMenu = ReplyKeyboardMarkup(resize_keyboard = True)
mainMenu.add(btnProfile,  btnPromo, btnList, btnSub)


sub_inline_markup = InlineKeyboardMarkup(row_width=1)
btnSubMonth = InlineKeyboardButton(text="Месяц - 190 рублей", callback_data="submonth")
sub_inline_markup.insert(btnSubMonth)