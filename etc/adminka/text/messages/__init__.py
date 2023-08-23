import datetime

# Мои библы
import config # Конфиг

# Библы из папок
from etc.adminka.text.messages import message_text as messages



def start():
	return messages.start


def rasl_message():
	return messages.rasl_message

def rasl_two_step_message(good, luse):
	mes = messages.rasl_two_step_message
	mes = mes.format(good, luse)

	return mes


def qiwi_setting():
	return messages.qiwi_setting


def add_qiwi_message():
	return messages.add_qiwi_message

def add_qiwi_not_valid_two_step_message(phone, token):
	mes = messages.add_qiwi_not_valid_two_step_message
	mes = mes.format(phone, token)

	return mes


def add_qiwi_two_step_message(added_wallets):
	mes = messages.add_qiwi_two_step_message
	mes = mes.format(added_wallets)

	return mes



def del_qiwi_message():
	return messages.del_qiwi_message

def del_qiwi_two_step_message():
	return messages.del_qiwi_two_step_message

def del_qiwi_not_data_two_step_message():
	return messages.del_qiwi_not_data_two_step_message




def delete_wallets():
	return messages.delete_wallets


def statistic_message(users, active_users, btc_balance, qiwi_balance):
	mes = messages.statistic_message
	mes = mes.format(users, active_users, btc_balance, qiwi_balance)

	return mes