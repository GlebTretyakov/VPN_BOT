import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
import markups as nav
from db import Database
from wg_get_profile import Wg_Profile

import time
import datetime

TOKEN = ""
YOOTOKEN = ""


now_time = int(time.time())

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

db = Database('database.db')


def days_to_seconds(days):
    return days * 24 * 60 * 60

#Получение времени подписки
def time_sub_day(get_time):
    time_now = int(time.time())
    middle_time = int(get_time) - time_now
    if middle_time <= 0:
        return False
    else:
        dt = str(datetime.timedelta(seconds=middle_time))
        dt = dt.replace("days", "дней")
        dt = dt.replace("day", "день")
        return dt



@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if (not db.user_exists(message.from_user.id)):
        db.add_user(message.from_user.id)
        await bot.send_message(message.from_user.id, "Укажите ваш ник")
    else:
        await bot.send_message(message.from_user.id, "Вы уже зарегистрированы!", reply_markup=nav.mainMenu)


@dp.message_handler()
async def bot_message(message: types.Message):
    if message.chat.type == 'private':
        if message.text == 'Профиль':
            user_nickname = "Ваш ник: " + db.get_nickname(message.from_user.id)
            user_sub = time_sub_day(db.get_time_sub(message.from_user.id))
            end_sub = str(user_sub)
            end_sub = end_sub[:-10]
            if user_sub == False:
                end_sub = "У вас нет подписки"
            end_sub = "\nПодписка истекает через: " + end_sub
            await bot.send_message(message.from_user.id,  user_nickname + "\nВаш ID: " + str(message.from_user.id) + end_sub )
            if db.get_wg_profile_status(message.from_user.id) > 0:
                user_id_str = str(message.from_user.id)
                await bot.send_message(message.from_user.id, "Ваш профиль VPN")
                await bot.send_document(message.from_user.id, open(user_id_str + ".conf", 'rb'))
            else:
                await bot.send_message(message.from_user.id, "Чтобы выпустить профиль VPN, получите подписку")

        if message.text == 'Помощь':
            await bot.send_message(message.from_user.id, 'Инструкция по установке - https://telegra.ph/Instrukciya-kak-polzovatsya-VPN-12-16-2')
            await bot.send_message(message.from_user.id, "Перед тем как написать в тех-поддержку, внимательно прочитайте инструкцию! \nТех-поддержка: @connect_vpn_support")


        elif message.text == 'Купить / продлить подписку':
            await bot.send_message(message.from_user.id, "Подписка VPN на 1 месяц", reply_markup=nav.sub_inline_markup)

        if message.text == 'Продлить подписку':
            if db.get_sub_status(message.from_user.id):
                plus_time = db.get_time_sub(message.from_user.id) + days_to_seconds(30)
                db.set_time_sub(message.from_user.id, plus_time)
                await bot.send_message(message.from_user.id, "Подписка продлена на 30 дней")
            else:
                await bot.send_message(message.from_user.id, "Купите подписку!")

        if message.text == "Пробная подписка":
            if db.get_promo_sub(message.from_user.id) == 0:
                if db.get_wg_profile_status(message.from_user.id) == 0:
                    Wg_Profile.get_profile(message.from_user.id, TOKEN)
                    await bot.send_message(message.from_user.id, "Ожидайте выдачу профиля...")
                    plus_time = days_to_seconds(7) + int(time.time())
                    db.set_time_sub(message.from_user.id, plus_time)
                    db.set_promo_sub(message.from_user.id, 1)
                    user_id_str = str(message.from_user.id)
                    await bot.send_document(message.from_user.id, open(user_id_str + ".conf", 'rb'))
                    db.set_wg_profile_status(message.from_user.id, 1)
                    await bot.send_message(message.from_user.id, "Поздравляем! Вы получили пробную подписку на 7 дней.")
                    await bot.send_message(message.from_user.id, 'Инструкция по установке - https://telegra.ph/Instrukciya-kak-polzovatsya-VPN-12-16-2')
            else:
                await bot.send_message(message.from_user.id,
                                       "Вы уже активировали пробную подписку или у вас была куплена подписка!")

        else:
            if db.get_signup(message.from_user.id) == "setnickname":
                if (len(message.text) > 15):
                    await bot.send_message(message.from_user.id, "Никнейм не должен превышать 15 символов")
                elif '@' in message.text or '/' in message.text:
                    await bot.send_message(message.from_user.id, "Вы ввели запрещеный символ")
                else:
                    db.set_nickname(message.from_user.id, message.text)
                    db.set_signup(message.from_user.id, "done")
                    await bot.send_message(message.from_user.id, "Регистрация прошла успешно!",
                                           reply_markup=nav.mainMenu)




@dp.callback_query_handler(text="submonth")
async def submonth(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_invoice(chat_id=call.from_user.id, title="Оформление подписки", description="Подписка на VPN 1 месяц", payload="month_sub", provider_token=YOOTOKEN, currency="RUB", start_parameter="VPN", prices=[{"label": "Руб", "amount": 19000}])

@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message):
    if message.successful_payment.invoice_payload == "month_sub":
        await bot.send_message('938346742', "Купили подписочку )))")
        if db.get_sub_status(message.from_user.id) == True:
            plus_time = db.get_time_sub(message.from_user.id) + days_to_seconds(30)
            db.set_time_sub(message.from_user.id, plus_time)
            await bot.send_message(message.from_user.id, "Вам продлена подписка на месяц!")
            db.set_promo_sub(message.from_user.id, 1)
            db.set_wg_profile_status(message.from_user.id, 1)
        if db.get_wg_profile_status(message.from_user.id) == 0:
            Wg_Profile.get_profile(message.from_user.id, TOKEN)
            time_sub = int(time.time()) + days_to_seconds(30)
            db.set_time_sub(message.from_user.id, time_sub)
            await bot.send_message(message.from_user.id, "Вам выдана подписка на месяц!")
            await bot.send_message(message.from_user.id, 'Инструкция по установке - https://telegra.ph/Instrukciya-kak-polzovatsya-VPN-12-16-2')
            await bot.send_message(message.from_user.id, "Ожидайте выдачу профиля...")
            user_id_str = str(message.from_user.id)
            await bot.send_document(message.from_user.id, open(user_id_str + ".conf", 'rb'))
            db.set_promo_sub(message.from_user.id, 1)
            db.set_wg_profile_status(message.from_user.id, 1)
        if db.get_wg_profile_status(message.from_user.id) == 1:
            if db.get_sub_status(message.from_user.id) != True:
                time_sub = int(time.time()) + days_to_seconds(30)
                db.set_time_sub(message.from_user.id, time_sub)
                await bot.send_message(message.from_user.id, "Вам выдана подписка на месяц!")
                await bot.send_message(message.from_user.id, 'Инструкция по установке - https://telegra.ph/Instrukciya-kak-polzovatsya-VPN-12-16-2')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)


