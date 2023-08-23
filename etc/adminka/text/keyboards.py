import telebot

# import config


# from etc import functions

def start_adm_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
    keyboard.row("Рассылка")
    keyboard.add("Настройка киви")
    keyboard.row("Удалить адреса")
    keyboard.row("Статистика")
    keyboard.row("/start")

    return keyboard



def qiwi_setting_keyboard(qiwies):
	keyboard = telebot.types.ReplyKeyboardMarkup(True, False)

	if 0 < len(qiwies):
		keyboard.row("Добавить киви", "Удалить киви")
	else:
		keyboard.row("Добавить киви")

	keyboard.row("Вернуться в начало")

	return keyboard


def all_qiwies_keyboard(qiwies):
	keyboard = telebot.types.ReplyKeyboardMarkup(True, False)

	for qiwi in qiwies:
		keyboard.row(qiwi)

	keyboard.row("Вернуться в начало")

	return keyboard




def back_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
    keyboard.row("Вернуться в начало")

    return keyboard





