import telebot

# Мои библы
import config # Конфиг

import classes.shelve as shelve # Работа с временным хранилищем




def admin_notifications(message):
    mes = message
    key = telebot.types.InlineKeyboardMarkup() 
    b1 = telebot.types.InlineKeyboardButton("Закрыть", callback_data="Закрыть")
    key.add(b1)

    for admin_id in config.ADMINS_ID:
        id = admin_id
        config.bot.send_message(id, mes, reply_markup=key, parse_mode="HTML")



def write_admin_sost(chat_id, sost):
	Temp = shelve.Temp(chat_id)
	Temp.write_admin_sost(sost)
	Temp.close()


def get_admin_sost(chat_id):
	Temp = shelve.Temp(chat_id)
	sost = Temp.get_admin_sost()
	Temp.close()

	return sost