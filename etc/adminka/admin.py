import time
import telebot

# Мои библы
import config # Конфиг

# Библы из папок
from etc import functions
from classes import shelve
from etc.adminka import helper
from etc.adminka import ifsost
from classes.pay import bitcoin
from classes.database import DataBase
from etc.adminka.text import messages
from etc.adminka.text import keyboards




from config import bot # Импорт обекта бота

def adminka(message):
    chat_id = message.chat.id
    message_text = message.text
    sost = helper.get_admin_sost(chat_id) # Получение состояния


    if "/adm" == message_text or "Вернуться в начало" == message_text:
        mes = messages.start()
        key = keyboards.start_adm_keyboard()
        bot.send_message(chat_id, mes, reply_markup=key)

        helper.write_admin_sost(chat_id, 1)


    elif "Рассылка" == message_text:
        mes = messages.rasl_message()
        key = keyboards.back_keyboard()
        bot.send_message(chat_id, mes, reply_markup=key)

        helper.write_admin_sost(chat_id, 2)


    elif "Настройка киви" == message_text:
        mes = messages.qiwi_setting()
        key = keyboards.qiwi_setting_keyboard(functions.get_qiwies())
        bot.send_message(chat_id, mes, reply_markup=key)


    elif "Добавить киви" == message_text:
        mes = messages.add_qiwi_message()
        key = keyboards.back_keyboard()
        bot.send_message(chat_id, mes, reply_markup=key, parse_mode="HTML")

        helper.write_admin_sost(chat_id, 3)


    elif "Удалить киви" == message_text:
        mes = messages.del_qiwi_message()
        key = keyboards.all_qiwies_keyboard(functions.get_qiwi_data())
        bot.send_message(chat_id, mes, reply_markup=key)

        helper.write_admin_sost(chat_id, 4)

    elif "Удалить адреса" == message_text:
        mes = messages.delete_wallets()
        bot.send_message(chat_id, mes)

        DB = DataBase()
        DB.delete_addresses()
        DB.close()


    elif "Статистика" == message_text:
        DB = DataBase()
        stats = DB.stats()
        DB.close()

        users = stats["users"]
        active = stats["active_users"]

        btc_balance = functions.round(bitcoin.Btc().balance())
        qiwi_balance = functions.qiwi_balance()

        mes = messages.statistic_message(users, active, qiwi_balance, btc_balance)
        bot.send_message(chat_id, mes, parse_mode="HTML")






        







    elif sost > 1:
        ifsost.ifsost(message, sost)






    













        