import datetime

import paramiko
import schedule
from aiogram import Bot, Dispatcher
from aiogram.utils import executor
import time
from db import Database

TOKEN = ""
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
db = Database('database.db')


def time_sub_day(get_time):
    time_now = int(time.time())
    middle_time = int(get_time) - time_now
    if middle_time <= 0:
        return False
    else:
        dt = str(datetime.timedelta(seconds=middle_time))
        dt = dt.replace("days", "дня")
        dt = dt.replace("day", "день")
        return dt


max_id = db.get_last_id()



def alert_send():
    for i in range(1, max_id + 1):
        try:
            user_sub = time_sub_day(db.get_time_sub(db.get_telegram_id(i)))
            user_sub = str(user_sub)[:2]
            str_user_sub = time_sub_day(db.get_time_sub(db.get_telegram_id(i)))
            str_user_sub = str(str_user_sub)[:-10]
            if int(user_sub) <= 4:
                async def send_message():
                    await bot.send_message(db.get_telegram_id(i), "Подписка на VPN истекает через: " + str_user_sub)
                    await bot.send_message(db.get_telegram_id(i), "Продлите подписку на VPN!")

                executor.start(dp, send_message())
                print(user_sub)
        except:
            pass

def main():
    schedule.every().day.at('12:37').do(alert_send)
    schedule.every().day.at('19:49').do(alert_send)
    while True:
        schedule.run_pending()



if __name__ == '__main__':
    main()