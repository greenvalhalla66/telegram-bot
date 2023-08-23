import telebot
import time

# Мои библы
import config  # Конфиг

# Библы из папок
from classes.pay import qiwi
import classes.shelve as shelve  # Работа с временным хранилищем
from classes.pay import bitcoin
import etc.messages as messages
from classes.database import DataBase


#-------------------------------Работа с shelve--------------------------------
def user_balance(chat_id):  # Получение баланса юзера
    """
    Получение баланса юзера.
    Поиск по chat_id
    Parameters
    ----------
    chat_id : int
        Telegram chat_id нужного юзера.

    Returns
    -------
    str
        Баланс юзера в боте,
        валюта btc.
    """
    BD = DataBase()  # Подключение к бд
    balance = BD.profile(chat_id)["profile"]["balance"]  # Получение баланса
    BD.close()  # Закрытие бд
    balance = float(balance)  # Привод баланса к читаему виду
    return balance  # возрат


def update_sost(chat_id, sost):  # Изменение состояния юзера
    """
    Изменение состояния юзера.
    Parameters
    ----------
    chat_id : int
        Telegram chat_id нужного юзера.
    sost : int
        Новое состояние юзера.
    """
    SH = shelve.Temp(chat_id)  # Подключение к shelve
    SH.write_sost(sost)  # Запись в shelve
    SH.close()  # Закрытие shelve


def user_sost(chat_id):  # Получение состояния юзера
    """
    Получение состояния юзера.
    Поиск по chat_id.
    Parameters
    ----------
    chat_id : int
        Telegram chat_id нужного юзера.

    Returns
    -------
    int
        Состояние юзера.
    """
    SH = shelve.Temp(chat_id)  # Подключение к shelve
    sost = SH.get_sost()  # Получение состояния
    SH.close()  # Закрытие shelve
    return sost  # Возрат состояния


def write_address(chat_id, address):  # Запись адреса для перевода
    """
    Запись адреса для перевода.
    Parameters
    ----------
    chat_id : int
        Telegram chat_id нужного юзера.
    address : str
        Адрес, который нужно сохранить.
    Returns
    -------
    str
        Баланс юзера в боте,
        валюта btc
    """
    SH = shelve.Temp(chat_id)  # Подключение к shelve
    SH.write_btc_address(address)  # Запись адреса в shelve
    SH.close()  # Закрытие shelve


def get_btc_address(chat_id):
    SH = shelve.Temp(chat_id)  # Подключение к shelve
    address = SH.get_btc_address()
    SH.close()
    return address


#----------------------------Математические операции---------------------------
def commission_on_removal(sum, commission):  # Высчитывание комисси
    """
    Комиссия(в btc) на вывод указанной суммы.
    Parameters
    ----------
    sum : sum
        Сумма, на которую комисиию нужно расчитать.
    commission : int
        Комиссия на вывод. 
        Которая прописывается в конфиге.
    Returns
    -------
    str
        Сумма комиссии в btc.
    """
    # commission = sum * (commission/100)  # Расчитывание комиссии
    commission = config.REMOVAL
    return commission  # Возрат


def max_removal(balance, commission):  # Макс сумма для вывода(учитывая комму)
    """
    Максимальная сумма для вывода юзера
    с его балансом.
    Parameters
    ----------
    balance : float
        Баланс юзера.
        Переводавать в формате float.
    commission : int
        Комиссия на вывод.
        Которая прописывается в конфиге.
    Returns
    -------
    str
        Максимальная сумма, которую можно вывести.
    """
    commission = commission_on_removal(
        float(balance), commission)  # Комисиия в btc
    commission = float(commission)  # Приведение комисии к числу
    max_removal = float(balance) - commission  # Сумма которую можно вывести
    max_removal = round(max_removal)  # Округление суммы
    return max_removal  # Возрат  # Возрат


def min_balance(min_removal, commission):  # Мин баланс вывода(учитывая комму)
    """
    Получение минимального баланса, 
    чтоб можно было вывести деньги.
    Parameters
    ----------
    min_removal : float
        Минимальная сумма для вывода.
        Не учитывая комиссию.
    commission : int
        Комиссия на вывод. 
        Которая прописывается в конфиге.
    Returns
    -------
    str
        Максимальная сумма, которую можно вывести.
    """
    commission = commission_on_removal(min_removal, commission)  # Кома в btc

    """Мин сумма для вывода, учитывая комиссию"""
    min_balance = min_removal + float(commission)
    min_balance = float(min_balance)
    min_balance = round(min_balance)  # Округление и приведение к чит. виду
    return min_balance  # Возрат


def will_on_balance(balance, sum_removal, commission):  # Будет на балике
    """
    Высчитывание, 
    сколько после вывода/перевода
    останется на балансе.
    Parameters
    ----------
    balance : float
        Баланс юзера.
    sum_removal : float
        Сумма, Которую юзер будет выводить/переводить    
    commission : int
        Комиссия на вывод. В %.
        Которая прописывается в конфиге.
    Returns
    -------
    str
        Сумма, Которая останется на балансе
    """
    commission = commission_on_removal(sum_removal, commission)  # Комиссия
    commission = float(commission)  # Приведение комисии к числу
    will_balance = float(balance) - sum_removal - \
        commission  # Сколько будет баланс
    will_balance = round(will_balance)  # Округление и приведение к чит. виду
    return will_balance


def round(digit):  # Округление числа и приведение к читаемому виду
    """
    Округление и приведение числа к читаемому виду.
    Parameters
    ----------
    digit : any
        Число.

    Returns
    -------
    str
        Округлённое и приведённое к читаемому виду число.
    """
    temp = {}  # Создание временного словаля
    code = "a = round({}, 8)".format(digit)  # Написание кода для исполнения
    digit = exec(code, temp)  # Исполненик кода в другом пространстве
    digit = temp["a"]  # Получение округлённого чила
    digit = "{:.8f}".format(digit)  # Приведение к строке
    return digit  # Возрат числа


#------------------------------Расчёты для обмена------------------------------
def sum_with_comission(sum, commission, operation):  # нужно получить и отправить
    global it_rub
    btc_price = bitcoin.Btc().price_with_comission(commission)
    if 1 < sum:
        it_rub = sum
        it_btc = sum / btc_price

    elif 1 > sum:
        it_btc = sum
        it_rub = sum * btc_price

    it_rub = round(it_rub)
    it_btc = round(it_btc)
    it_btc = float(it_btc)
    it_rub = float(it_rub)

    resp = {}
    if operation == "byu":
        resp["need_me"] = it_rub
        resp["need_send"] = it_btc

    elif operation == "sell":
        resp["need_me"] = it_btc
        resp["need_send"] = it_rub

    return resp


#---------------------------------Другие функции-------------------------------
def qrcode_url(word, version=5):  # Генерация ссылки на qrcode
    url = "http://qrcoder.ru/code/?{}&{}&0".format(word, version)
    return url


def close_key(text):  # Получение кнопки с надписью, для удаления сообщения
    key = telebot.types.InlineKeyboardMarkup()
    b1 = telebot.types.InlineKeyboardButton(text, callback_data="Закрыть")
    key.add(b1)
    return key


def btc_to_user(sender_id, payee_id, sum):  # Отправка btc по chat_id
    """
    Отправка btc по chat_id другому юзеру бота.
    Parameters
    ----------
    sender_id : int
        Telegram chat_id отправителя.
    payee_id : int
        Telegram chat_id получателя денег.
    sum : float
        Сумма перевода в btc.
    """
    comm1 = "transfer {}".format(payee_id)  # Генерация комментария отправителя
    comm2 = "get_transfer"  # Комментарий для получателя

    BD = DataBase()
    BD.money_operation(sender_id, float(sum), "removal", comm1)  # Отправитель
    BD.money_operation(payee_id, float(sum), "refill", comm2)  # Получатель
    BD.close()


def isdigit(digit):  # Проверка, является ли строка числом
    try:
        float(digit)
        return True
    except:
        return False


def create_link(code):
    username = config.bot.get_me().username
    url = "https://t.me/{}?start={}".format(username, code)
    return url


def balance_for_exchange():  # Сколько балика можно использовать для обмена
    # BD = DataBase()
    # balance = float(bitcoin.Btc().balance()) - \
    #     (BD.users_balance() - (1 * config.REMOVAL))
    # BD.close()
    # return balance
    return config.max_in_btc


def check_address(address):
    try:
        bitcoin.Btc().address_balance(address)
        resp = True
    except:
        resp = False
        if len(address) == 34 or len(address) == 42:
            resp = True

    return resp


def num_validator(number):
    if number[0] == "+":
        number = number[1:]
    if number[0] == "8":
        number = "7{}".format(number[1:])

    number = int(number)
    return number


def get_qiwies():
    DB = DataBase()
    qiwies = DB.get_qiwies()
    DB.close()

    return qiwies


def get_qiwi_data():
    data = []

    for qiwi in get_qiwies():
        line = "{}:{}".format(qiwi["phone"], qiwi["token"])

        data.append(line)

    return data


def qiwi_balance():
    balance = 0

    for qiwi in get_qiwies():
        balance += qiwi["balance"]

    return balance


def update_qiwi(what, phone, new_balance):
    DB = DataBase()
    DB.update_qiwi(what, phone, new_balance)
    DB.close()


def send_qiwies_money(recipient, sum):
    alredy_send = 0

    for qiwi_data in get_qiwies():
        phone, token = qiwi_data["phone"], qiwi_data["token"]

        wallet = qiwi.QApi(num=phone, token=token)

        temp = {}  # Создание временного словаля
        # Написание кода для исполнения
        code = "a = round({})".format(wallet.balance() * 0.98)
        digit = exec(code, temp)  # Исполненик кода в другом пространстве
        now_balance = int(temp["a"])  # Получение округлённого чила

        now_need_send = sum - alredy_send
        will_balance = now_balance - now_need_send

        if now_need_send > now_balance:
            wallet.send(recipient, now_balance)

            update_qiwi("balance", phone, 0)

            alredy_send += now_balance

        else:
            wallet.send(recipient, now_need_send)

            update_qiwi("balance", phone, will_balance)

            break

        if sum <= alredy_send:
            break
