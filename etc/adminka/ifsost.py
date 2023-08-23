import time
import telebot

import config


from etc import functions
from classes import shelve
from classes.pay import qiwi
from etc.adminka import helper
from classes.database import DataBase
from etc.adminka.text import messages
from etc.adminka.text import keyboards


from config import bot

def ifsost(message, sost):
    chat_id = message.chat.id
    message_text = message.text


    # Ждём сообщение для рассылки
    if sost == 2:
        DB = DataBase()
        users = DB.all_users()
        DB.close()

        good = 0
        luse = 0


        for user_chat_id in users:
            try:
                bot.send_message(user_chat_id, message_text, parse_mode="HTML")

                good += 1
            except:
                luse += 1


            if good + luse % 25 == 0:
                time.sleep(10)

        mes = messages.rasl_two_step_message(good, luse)
        key = keyboards.start_adm_keyboard()
        bot.send_message(chat_id, mes, reply_markup=key)

        helper.write_admin_sost(chat_id, 1)


    # Ждём киви кошельки
    elif 3 == sost:
        added_qiwies = 0

        for data in message_text.split("\n"):
            phone, token = data.split(":")

            if phone.isdigit():
                phone = int(phone)

                wallet = qiwi.QApi(num=phone, token=token)


                if False == wallet.check_valid_account(config.test_send_phone, 1):
                    mes = messages.add_qiwi_not_valid_two_step_message(phone, token)
                    bot.send_message(chat_id, mes, parse_mode="HTML")
                else:
                    balance = wallet.balance()

                    DB = DataBase()
                    DB.add_qiwi(phone, token, balance)
                    DB.close()

                    added_qiwies += 1


            else:
                mes = messages.add_qiwi_not_valid_two_step_message(phone, token)
                bot.send_message(chat_id, mes, parse_mode="HTML")


        mes = messages.add_qiwi_two_step_message(added_qiwies)
        key = keyboards.qiwi_setting_keyboard(functions.get_qiwies())
        bot.send_message(chat_id, mes, reply_markup=key)

        helper.write_admin_sost(chat_id, 1)


    # Ждём киви кошелёк для удаления
    elif 4 == sost:
        if message_text in functions.get_qiwi_data():
            phone = message_text.split(":")[0]

            DB = DataBase()
            DB.del_qiwi(phone)
            DB.close()

            mes = messages.del_qiwi_two_step_message()
            key = keyboards.qiwi_setting_keyboard(functions.get_qiwies())

            helper.write_admin_sost(chat_id, 1)

        else:
            mes = messages.del_qiwi_not_data_two_step_message()
            key = None


        bot.send_message(chat_id, mes, reply_markup=key)













        














































        


























