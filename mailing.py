from aiogram import Dispatcher, Bot
from aiogram.utils import executor
import time
from db import Database

TOKEN = ""
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
db = Database('database.db')


# получим объект файла
file1 = open("user_id.txt", "r")

# считываем все строки
lines = file1.readlines()




def send():
    for line in lines:
        try:
            print(line)
            async def send_message():
                await bot.send_message(db.get_telegram_id(line), "Оформляем подписочку на наш прекрасный VPN! \nДля обновления бота нажмите на эту команду /start ")
            executor.start(dp, send_message())
            time.sleep(0.3)
        except:
            pass




# закрываем файл
file1.close


send()
