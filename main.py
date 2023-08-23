import threading

import telebot

# Мои библы
import bot as b0t
import classes.shelve as shelve  # Работа с временным хранилищем
import config  # Конфиг
import etc.functions as functions  # Дополнительные функции
import etc.messages as messages  # Сообщения
import script
from classes.database import DataBase
from classes.pay import bitcoin, qiwi
# Библы из папок
from etc.adminka import admin
from etc.adminka import helper

bot = config.bot


@bot.message_handler(commands=["restart"])
def restart(message):
    if message.chat.id in config.ADMINS_ID:
        if len(message.text) > 8:  # Если сообщение больше 8 символов, знач там код
            exec(message.text[9:])  # Он исполняется

        else:
            raise ValueError("Specifically caused the error to restart")


@bot.message_handler(commands=["adm"])
def adminka(message):
    if message.chat.id in config.ADMINS_ID:
        admin.adminka(message)


# @bot.message_handler(commands=["sos"])
# def sos(message):
# bot.send_message(message.chat.id, '')


@bot.message_handler(commands=["start"])
def start_message(message):
    key = telebot.types.ReplyKeyboardMarkup(True, False)
    # key.row("♻️ Обмен", "🔐 Личный кабинет")
    # key.row("ℹ️ О сервисе")
    key.row("✅ Соглашение принимаю!")
    mes = messages.soglas()

    bot.send_message(message.chat.id, mes, reply_markup=key,
                     disable_web_page_preview=True, parse_mode="HTML")
    functions.update_sost(message.chat.id, 0)

    # Если длинна сообщения больше обычного
    if len(message.text) > 6 and message.text[7:9] == "v_":
        voucher = message.text[9:]

        BD = DataBase()
        resp = BD.get_voucher(voucher)
        if resp["exist"] == False or resp["status"] == "activated":
            mes = messages.incorrect_voucher()
            bot.send_message(message.chat.id, mes)

        elif resp["exist"] == True and resp["status"] == "not_activated":
            resp = BD.activate_voucher(voucher, message.chat.id)
            creator_chat_id, sum = resp
            sum = functions.round(sum)

            """Отправка уведомы создателю ваучера"""
            mes = messages.your_voucher_acvtivate(sum)
            bot.send_message(creator_chat_id, mes, parse_mode="HTML")

            """Активировавшему"""
            mes = messages.when_btc_came(sum)
            bot.send_message(message.chat.id, mes, parse_mode="HTML")

        BD.close()

    functions.update_sost(message.chat.id, 0)  # Апдейт состояния юзера
    helper.write_admin_sost(message.chat.id, 0)


@bot.message_handler(content_types=["text"])
def handle_message(message):
    chat_id = message.chat.id

    try:
        # Получение состояния  юзера
        sost = functions.user_sost(message.chat.id)
    except:
        sost = 0
        functions.update_sost(message.chat.id, sost)  # Апдейт состояния юзера
        bot.send_message(message.chat.id, messages.start(), parse_mode="HTML")

    if message.text == "✅ Соглашение принимаю!":
        key = telebot.types.ReplyKeyboardMarkup(True, False)
        key.row("♻️ Обмен", "🔐 Личный кабинет")
        key.row("ℹ️ О сервисе")
        # key.row("✅ Соглашение принимаю!")
        mes = messages.start()

        bot.send_message(message.chat.id, mes, reply_markup=key,
                         disable_web_page_preview=True, parse_mode="HTML")
        functions.update_sost(message.chat.id, 0)

    if message.text == "🔐 Личный кабинет":
        # Получение данных о профиле
        BD = DataBase()
        profile = BD.profile(message.chat.id)["profile"]
        BD.close()
        reg_date = profile["registration_date"]
        # referals = profile["ref"]["amount"]
        # referal_income = profile["ref"]["income"]
        balance = profile["balance"]
        in_rub = bitcoin.Btc().convert("btc", balance)
        # ----------------------------------------------------------------------

        mes = messages.wallet(message.chat.id, reg_date, balance, in_rub)

        key = telebot.types.InlineKeyboardMarkup()
        b1 = telebot.types.InlineKeyboardButton(text="📥 Внести",
                                                callback_data="Внести")
        b2 = telebot.types.InlineKeyboardButton(text="📤 Вывести",
                                                callback_data="Вывести")
        b3 = telebot.types.InlineKeyboardButton(text="💸 Перевести",
                                                callback_data="Перевести")
        b4 = telebot.types.InlineKeyboardButton(text="🎟 Ваучеры",
                                                callback_data="Ваучеры")
        b5 = telebot.types.InlineKeyboardButton(text="🤝 Реф. программа",
                                                callback_data="Рефералка")
        key.add(b1, b2)
        key.add(b3, b4)
        key.add(b5)
        chat_id = message.chat.id
        bot.send_message(chat_id, mes, reply_markup=key, parse_mode="HTML")
        functions.update_sost(message.chat.id, 0)  #

    # elif message.text == "👤 Профиль":
    # BD = DataBase()
    # profile = BD.profile(message.chat.id)["profile"]
    # BD.close()
    # reg_date = profile["registration_date"]
    # referals = profile["ref"]["amount"]
    # referal_income = profile["ref"]["income"]

    # mes = messages.profile(message.chat.id, reg_date, referals, referal_income)
    # key = telebot.types.InlineKeyboardMarkup()
    # b1 = telebot.types.InlineKeyboardButton(text="🤝 Реф. программа",
    # callback_data="Рефералка")
    # key.add(b1)

    # chat_id = message.chat.id
    # bot.send_message(chat_id, mes, reply_markup=key, parse_mode="HTML")
    # functions.update_sost(message.chat.id, 0) #

    elif message.text == "ℹ️ О сервисе":
        key = telebot.types.InlineKeyboardMarkup()
        b1 = telebot.types.InlineKeyboardButton("👤 Польз. соглашение",
                                                url=config.RULES)
        b2 = telebot.types.InlineKeyboardButton("⁉️ FAQ",
                                                url=config.FAQ)
        b3 = telebot.types.InlineKeyboardButton("🆘 Поддержка",
                                                url=config.SUPPORT)
        # b4 = telebot.types.InlineKeyboardButton("Новостной канал",
        # commands="start")
        # b5 = telebot.types.InlineKeyboardButton("Закрыть",
        # callback_data="Закрыть")
        key.add(b1)
        key.add(b2, b3)
        # key.add(b5)
        mes = messages.rules()
        chat_id = message.chat.id
        bot.send_message(chat_id, mes, reply_markup=key, parse_mode="HTML")
        functions.update_sost(message.chat.id, 0)  #

    elif message.text == "♻️ Обмен":
        BD = DataBase()
        profile = BD.profile(message.chat.id)["profile"]
        BD.close()
        exchanges = profile["exchanges"]["amount"]
        sum_exchange = profile["exchanges"]["sum"]
        key = telebot.types.InlineKeyboardMarkup()
        b1 = telebot.types.InlineKeyboardButton(text="📈 Купить ฿TC",
                                                callback_data="Купить BTC")
        b2 = telebot.types.InlineKeyboardButton(text="📉 Продать ฿TC",
                                                callback_data="Продать BTC")
        mes = messages.info(exchanges, sum_exchange)
        key.add(b1, b2)
        # key.add(b2)
        bot.send_message(message.chat.id, mes,
                         reply_markup=key, parse_mode="HTML")
        functions.update_sost(message.chat.id, 0)  #

    elif sost > 0:
        b0t.ifsost(message, sost)

    elif chat_id in config.ADMINS_ID and helper.get_admin_sost(chat_id) > 0:
        admin.adminka(message)


@bot.callback_query_handler(func=lambda c: True)
def inline(callback):
    if callback.data == "Внести":
        bot.answer_callback_query(callback.id, text="")
        # Получения адреса для пользователя
        BD = DataBase()
        address = BD.get_btc_address(callback.message.chat.id)
        a_mes = "<code>{}</code>".format(address)
        BD.close()
        # ----------------------------------------------------------------------

        mes = messages.when_btc_refill()  # Получения сообщения
        chat_id = callback.message.chat.id
        bot.send_message(chat_id, mes, parse_mode="HTML")

        """Отправка адреса"""
        key = telebot.types.InlineKeyboardMarkup()
        b1 = telebot.types.InlineKeyboardButton(text="Получить QR код",
                                                callback_data="Получить QR код")
        key.add(b1)
        bot.send_message(chat_id, a_mes, reply_markup=key, parse_mode="HTML")
        # ----------------------------------------------------------------------

        functions.write_address(chat_id, address)

        # ----------------------------------------------------------------------

    elif callback.data == "Вывести":
        # bot.answer_callback_query(callback.id, text="")
        balance = float(functions.user_balance(callback.message.chat.id))

        """Нужный минимальный баланс вместе с комиссией"""
        min_balance = functions.min_balance(config.ON_REMOVAL, config.REMOVAL)
        min_balance = float(min_balance)

        if balance >= min_balance:
            bot.answer_callback_query(callback.id, text="")
            key = telebot.types.InlineKeyboardMarkup()
            b1 = telebot.types.InlineKeyboardButton(text="⬅️ Назад",
                                                    callback_data="Кошелек")
            key.add(b1)
            mes = messages.removal_address()
            chat_id = callback.message.chat.id
            bot.edit_message_text(mes, chat_id=chat_id, reply_markup=key,
                                  message_id=callback.message.message_id,
                                  parse_mode="HTML")

            functions.update_sost(callback.message.chat.id, 1)

        else:
            # key = telebot.types.InlineKeyboardMarkup()
            text = messages.min_removal()
            bot.answer_callback_query(callback.id, show_alert=True, text=text)
            # callback_data="Закрыть")

        # key.add(b1)
        # chat_id = callback.message.chat.id
        # bot.send_message(chat_id, mes, reply_markup=key, parse_mode="HTML")

        # ----------------------------------------------------------------------

    elif callback.data == "Подтверждаю вывод":
        BD = DataBase()
        BD.close()

        # balance = profile["balance"]
        # in_rub = bitcoin.Btc().convert("btc", balance)
        # exchanges = profile["exchanges"]["amount"]
        # reg_date = str(datetime.datetime.fromtimestamp(reg_date))[:10].split("-")
        # reg_date = "{}-{}-{}".format(reg_date[2], reg_date[1], reg_date[0])
        # exchange_sum = profile["exchanges"]["sum"]
        SH = shelve.Temp(callback.message.chat.id)
        if SH.get_sost() == 3:
            # bot.answer_callback_query(callback.id, text="")
            chat_id = callback.message.chat.id
            key = telebot.types.InlineKeyboardMarkup()
            b1 = telebot.types.InlineKeyboardButton(text="🆗",
                                                    callback_data="Кошелек")
            key.add(b1)
            bot.edit_message_text("✅ Средства успешно отправлены", chat_id=chat_id,
                                  message_id=callback.message.message_id, reply_markup=key,
                                  parse_mode="HTML")

            address = SH.get_btc_address()
            sum = SH.get_sum_in_btc()
            commission = functions.commission_on_removal(sum, config.REMOVAL)

            text = "✅ Средства успешно отправлены"
            bot.answer_callback_query(callback.id, show_alert=True, text=text)

            BD = DataBase()
            type = "removal"
            BD.money_operation(chat_id, float(sum), type, type)
            BD.money_operation(chat_id, float(commission), type, "commission")
            BD.close()

            bitcoin.Btc().send(address, sum)  # Перевод денег

            SH.write_sost(0)

        SH.close()

    elif callback.data == "Перевести":
        # bot.answer_callback_query(callback.id, text="")
        # print("П")
        chat_id = callback.message.chat.id  # chat_id, сокращение
        balance = float(functions.user_balance(chat_id))  # Баланс юзера
        if balance > 0:
            bot.answer_callback_query(callback.id, text="")
            mes = messages.when_money_transfer()  # Получение сообщения
            key = telebot.types.InlineKeyboardMarkup()
            b1 = telebot.types.InlineKeyboardButton(text="⬅️ Назад",
                                                    callback_data="Кошелек")
            key.add(b1)
            bot.edit_message_text(mes, chat_id=callback.message.chat.id,
                                  message_id=callback.message.message_id, reply_markup=key,
                                  parse_mode="HTML")
            functions.update_sost(chat_id, 4)  # Обновление состояния
            print(functions.user_sost(chat_id))

        else:
            bot.answer_callback_query(
                callback.id, show_alert=True, text="🚫 Пополните баланс для совершения операции!")
            # key = functions.close_key("Закрыть")

        # bot.send_message(chat_id, mes, reply_markup=key, parse_mode="HTML")

    elif callback.data == "Подтверждаю перевод":
        SH = shelve.Temp(callback.message.chat.id)
        if SH.get_sost() == 6:
            chat_id = callback.message.chat.id
            key = telebot.types.InlineKeyboardMarkup()
            b1 = telebot.types.InlineKeyboardButton(text="🆗",
                                                    callback_data="Кошелек")
            key.add(b1)
            bot.edit_message_text("✅ Средства успешно переведены пользователю", chat_id=chat_id,
                                  message_id=callback.message.message_id, reply_markup=key,
                                  parse_mode="HTML")

            address = SH.get_btc_address()
            sum = SH.get_sum_in_btc()

            text = "✔️ Средства успешно переведены"
            bot.answer_callback_query(callback.id, show_alert=True, text=text)

            functions.btc_to_user(chat_id, address, float(sum))  # Сенд мани

            mes = messages.when_btc_came(sum)
            bot.send_message(address, mes, parse_mode="HTML")

            SH.write_sost(0)

        SH.close()

    elif callback.data == "Ваучеры":
        bot.answer_callback_query(callback.id, text="")
        chat_id = callback.message.chat.id
        BD = DataBase()
        amount_vouchers = BD.user_notactivated_vouchers(chat_id)["amount"]
        BD.close()

        key = telebot.types.InlineKeyboardMarkup()
        b1 = telebot.types.InlineKeyboardButton("🆕 Создать",
                                                callback_data="Создать")
        b2 = telebot.types.InlineKeyboardButton("✳️ Активировать",
                                                callback_data="Активировать")
        key.add(b1, b2)
        if amount_vouchers > 0:
            text = "🎁 Активные ({})".format(amount_vouchers)
            b3 = telebot.types.InlineKeyboardButton(text,
                                                    callback_data="Активные")
            key.add(b3)

        mes = messages.voucher()
        b4 = telebot.types.InlineKeyboardButton("⬅️ Назад",
                                                callback_data="Кошелек")
        key.add(b4)
        bot.edit_message_text(mes, chat_id=callback.message.chat.id, reply_markup=key,
                              message_id=callback.message.message_id,
                              parse_mode="HTML")
        functions.update_sost(chat_id, 0)

    elif callback.data == "Создать":
        # bot.answer_callback_query(callback.id, text="")
        chat_id = callback.message.chat.id
        # balance = functions.user_balance(callback.message.chat.id)
        balance = float(functions.user_balance(chat_id))
        if balance > 0:
            bot.answer_callback_query(callback.id, text="")
            mes = messages.create_voucher(balance)
            key = telebot.types.InlineKeyboardMarkup()
            b1 = telebot.types.InlineKeyboardButton("⬅️ Назад",
                                                    callback_data="Ваучеры")
            key.add(b1)
            chat_id = callback.message.chat.id
            bot.edit_message_text(mes, chat_id=callback.message.chat.id,
                                  message_id=callback.message.message_id, reply_markup=key,
                                  parse_mode="HTML")
            functions.update_sost(chat_id, 7)  # Обновление состояния
        else:
            bot.answer_callback_query(
                callback.id, show_alert=True, text="🚫 Пополните баланс для совершения операции!")

    elif callback.data == "Активировать":
        bot.answer_callback_query(callback.id, text="")
        mes = "🎟 <i>Активация ваучера</i>\n➖➖➖➖➖➖➖➖➖➖\n🔢 Введите код полученного ваучера"
        key = telebot.types.InlineKeyboardMarkup()
        b1 = telebot.types.InlineKeyboardButton("⬅️ Назад",
                                                callback_data="Ваучеры")
        key.add(b1)
        bot.edit_message_text(mes, chat_id=callback.message.chat.id,
                              message_id=callback.message.message_id, reply_markup=key,
                              parse_mode="HTML")
        functions.update_sost(callback.message.chat.id, 8)  # Апдейт состояния

    elif callback.data == "Активные":
        bot.answer_callback_query(callback.id, text="")
        chat_id = callback.message.chat.id
        BD = DataBase()
        vouchers = BD.user_notactivated_vouchers(chat_id)
        BD.close()
        bot.send_message(chat_id, "Ваши активные ваучеры:")
        if vouchers["amount"] > 0:
            vouchers_info = vouchers["vouchers"]
            for i in vouchers_info:
                code = vouchers_info[i]["code"]
                sum = vouchers_info[i]["sum"]
                link = functions.create_link("v_{}".format(code))
                mes = messages.my_vouchers(sum, code, link)
                bot.send_message(
                    chat_id, mes, disable_web_page_preview=True, parse_mode="HTML")

    elif callback.data == "Купить BTC":
        bot.answer_callback_query(callback.id, text="")
        btc_balance = functions.balance_for_exchange()

        chat_id = callback.message.chat.id
        mes = messages.one_step_byu_btc(btc_balance)
        key = functions.close_key("⬅️ Назад")
        bot.edit_message_text(mes, chat_id=callback.message.chat.id,
                              message_id=callback.message.message_id, reply_markup=key,
                              parse_mode="HTML")
        functions.update_sost(chat_id, 9)  # Обновление состояния

    elif callback.data == "Продолжить":
        bot.answer_callback_query(callback.id, text="")
        chat_id = callback.message.chat.id
        qiwi_data = functions.get_qiwies()[0]
        BD = DataBase()
        address = BD.get_btc_address(callback.message.chat.id)
        BD.close()
        SH = shelve.Temp(chat_id)

        # address = message_text
        need_me = SH.get_need_me()
        need_send = SH.get_need_send()

        phone, token = qiwi_data["phone"], qiwi_data["token"]

        wallet = qiwi.QApi(num=phone, token=token)

        comment = wallet.gen_comment()
        pay_form = wallet.pay_form(need_me, comment)

        SH.write_qiwi_data("{}:{}".format(phone, token))
        SH.write_btc_address(address)
        SH.write_sost(11)
        SH.write_comment(comment)
        SH.close()

        key = telebot.types.InlineKeyboardMarkup()
        b1 = telebot.types.InlineKeyboardButton("✔ Я оплатил",
                                                callback_data="Проверить оплату")
        b2 = telebot.types.InlineKeyboardButton("❌ Отмена",
                                                callback_data="Закрыть")
        b3 = telebot.types.InlineKeyboardButton("🌐 К оплате ➪",
                                                url=pay_form)
        key.add(b1, b3)
        key.add(b2)

        mes = messages.four_step_byu_btc(need_me, phone, comment, need_send)

        # else:
        # key = functions.close_key("❌ Отмена")
        # mes = messages.if_nevalid_address()

        bot.edit_message_text(mes, chat_id=callback.message.chat.id, reply_markup=key,
                              message_id=callback.message.message_id,
                              parse_mode="HTML", disable_web_page_preview=True)
        functions.update_sost(chat_id, 11)  # Апдейт состояния юзера

    elif callback.data == "Проверить оплату":
        chat_id = callback.message.chat.id
        if functions.user_sost(chat_id) == 11:
            SH = shelve.Temp(chat_id)
            qiwi_data = SH.qiwi_data()
            comment = SH.get_comment()
            need_send = SH.get_need_send()
            need_me = SH.get_need_me()
            address = SH.get_btc_address()
            SH.close()

            phone, token = qiwi_data.split(":")

            wallet = qiwi.QApi(num=phone, token=token)
            payment = wallet.search_payment(need_me, comment)["status"]

            if payment == True:
                bot.delete_message(chat_id, callback.message.message_id)
                # start_message(callback.message)
                bot.answer_callback_query(callback.id, text="")
                mes = messages.when_user_pay(need_send)
                key = functions.close_key("🆗")
                bot.send_message(
                    chat_id, mes, reply_markup=key, parse_mode="HTML")

                bitcoin.Btc().send(address, need_send)
                DB = DataBase()
                DB.new_btc_byu(chat_id, address, need_send, need_me)
                DB.update_qiwi("balance", phone, wallet.balance() + need_me)
                DB.close()
                functions.update_sost(chat_id, 0)  # Апдейт состояния юзера

            elif payment == False:
                text = "❌ Платеж не найден! Проверьте корректность указанных реквизитов."
                bot.answer_callback_query(callback.id, show_alert=True,
                                          text=text)

    elif callback.data == "Продать BTC":
        bot.answer_callback_query(callback.id, text="")
        qiwi_balance = functions.qiwi_balance()

        chat_id = callback.message.chat.id
        mes = messages.one_step_sell_btc(qiwi_balance)
        key = functions.close_key("⬅️ Назад")
        bot.edit_message_text(mes, chat_id=callback.message.chat.id,
                              message_id=callback.message.message_id, reply_markup=key,
                              parse_mode="HTML")
        functions.update_sost(chat_id, 12)  # Обновление состояния

    elif callback.data == "Продолжить1":
        chat_id = callback.message.chat.id
        # BD = DataBase()
        # last_qiwi = BD.profile(chat_id)["profile"]["last_wallet"]["qiwi"]
        # BD.close()
        key = telebot.types.InlineKeyboardMarkup()
        # if last_qiwi != None:
        # key.row(str(last_qiwi))
        mes = messages.three_step_sell_btc()
        b2 = telebot.types.InlineKeyboardButton(text="❌ Отмена",
                                                callback_data="Закрыть")
        key.add(b2)
        bot.edit_message_text(mes, chat_id=callback.message.chat.id,
                              message_id=callback.message.message_id, reply_markup=key,
                              parse_mode="HTML")
        functions.update_sost(chat_id, 13)  # Апдейт состояния юзера

    elif callback.data == "Оплатить с баланса бота":
        chat_id = callback.message.chat.id
        if functions.user_sost(chat_id) == 14:
            SH = shelve.Temp(chat_id)
            need_send = SH.get_need_send()
            need_me = SH.get_need_me()
            qiwi_num = SH.get_btc_address()
            SH.close()

            balance = float(functions.user_balance(chat_id))

            if balance >= need_me:
                bot.delete_message(chat_id, callback.message.message_id)
                # start_message(callback.message)
                bot.answer_callback_query(callback.id, text="")
                mes = messages.five_step_sell_btc(need_send, qiwi_num)
                key = functions.close_key("🆗")
                bot.send_message(
                    chat_id, mes, reply_markup=key, parse_mode="HTML")

                functions.send_qiwies_money(qiwi_num, need_send)

                BD = DataBase()
                BD.new_btc_sell(chat_id, qiwi_num, need_me, need_send)
                BD.money_operation(chat_id, need_me, "removal", "removal")
                BD.close()
                # functions.send_qiwies_money(qiwi_num, need_send)
                functions.update_sost(chat_id, 0)  # Апдейт состояния юзера

            else:
                text = "❌ На вашем балансе недостаточно средств!"
                bot.answer_callback_query(callback.id, show_alert=True,
                                          text=text)

    elif callback.data == "Закрыть":
        bot.answer_callback_query(callback.id, text="")
        BD = DataBase()
        profile = BD.profile(callback.message.chat.id)["profile"]
        BD.close()
        exchanges = profile["exchanges"]["amount"]
        sum_exchange = profile["exchanges"]["sum"]
        chat_id = callback.message.chat.id
        key = telebot.types.InlineKeyboardMarkup()
        b1 = telebot.types.InlineKeyboardButton(text="📈 Купить ฿TC",
                                                callback_data="Купить BTC")
        b2 = telebot.types.InlineKeyboardButton(text="📉 Продать ฿TC",
                                                callback_data="Продать BTC")
        mes = messages.info(exchanges, sum_exchange)
        key.add(b1, b2)
        # key.add(b2)
        bot.edit_message_text(mes, chat_id=callback.message.chat.id,
                              message_id=callback.message.message_id, reply_markup=key,
                              parse_mode="HTML")

        functions.update_sost(chat_id, 0)  # Обновление состояния

    elif callback.data == "Отмена":
        bot.answer_callback_query(callback.id, text="")
        chat_id = callback.message.chat.id
        bot.delete_message(chat_id, callback.message.message_id)
        functions.update_sost(chat_id, 0)

    elif callback.data == "Получить QR код":
        bot.answer_callback_query(callback.id, text="")
        text = callback.message.text
        qrcode = functions.qrcode_url(text)
        bot.send_photo(callback.message.chat.id, qrcode)
        bot.edit_message_text(text, chat_id=callback.message.chat.id,
                              message_id=callback.message.message_id,
                              parse_mode="HTML")

    elif callback.data == "Рефералка":
        bot.answer_callback_query(callback.id, text="")
        BD = DataBase()
        profile = BD.profile(callback.message.chat.id)["profile"]
        BD.close()
        referals = profile["ref"]["amount"]
        referal_income = profile["ref"]["income"]

        chat_id = callback.message.chat.id
        link = functions.create_link("r_{}".format(chat_id))
        mes = messages.ref_message(link, referals, referal_income)
        key = telebot.types.InlineKeyboardMarkup()
        b1 = telebot.types.InlineKeyboardButton(text="⬅️ Назад",
                                                callback_data="Кошелек")
        key.add(b1)
        bot.edit_message_text(mes, chat_id=callback.message.chat.id, reply_markup=key,
                              message_id=callback.message.message_id, disable_web_page_preview=True,
                              parse_mode="HTML")

    elif callback.data == "Кошелек":
        bot.answer_callback_query(callback.id, text="")
        # Получение данных о профиле
        BD = DataBase()
        profile = BD.profile(callback.message.chat.id)["profile"]
        BD.close()
        reg_date = profile["registration_date"]
        # referals = profile["ref"]["amount"]
        # referal_income = profile["ref"]["income"]
        balance = profile["balance"]
        in_rub = bitcoin.Btc().convert("btc", balance)

        # ----------------------------------------------------------------------

        mes = messages.wallet(callback.message.chat.id,
                              reg_date, balance, in_rub)
        # referals, referal_income)

        key = telebot.types.InlineKeyboardMarkup()
        b1 = telebot.types.InlineKeyboardButton(text="📥 Внести",
                                                callback_data="Внести")
        b2 = telebot.types.InlineKeyboardButton(text="📤 Вывести",
                                                callback_data="Вывести")
        b3 = telebot.types.InlineKeyboardButton(text="💸 Перевести",
                                                callback_data="Перевести")
        b4 = telebot.types.InlineKeyboardButton(text="🎟 Ваучеры",
                                                callback_data="Ваучеры")
        b5 = telebot.types.InlineKeyboardButton(text="🤝 Реф. программа",
                                                callback_data="Рефералка")
        key.add(b1, b2)
        key.add(b3, b4)
        key.add(b5)
        chat_id = callback.message.chat.id
        functions.update_sost(callback.message.chat.id, 0)  #
        bot.edit_message_text(mes, chat_id=callback.message.chat.id, reply_markup=key,
                              message_id=callback.message.message_id,
                              parse_mode="HTML")
        functions.update_sost(chat_id, 0)

    elif callback.data == "Профиль":
        bot.answer_callback_query(callback.id, text="")
        BD = DataBase()
        profile = BD.profile(callback.message.chat.id)["profile"]
        BD.close()
        reg_date = profile["registration_date"]
        referals = profile["ref"]["amount"]
        referal_income = profile["ref"]["income"]

        mes = messages.profile(callback.message.chat.id,
                               reg_date, referals, referal_income)
        key = telebot.types.InlineKeyboardMarkup()
        b1 = telebot.types.InlineKeyboardButton(text="🤝 Реф. программа",
                                                callback_data="Рефералка")
        key.add(b1)

        chat_id = callback.message.chat.id
        bot.edit_message_text(mes, chat_id=callback.message.chat.id, reply_markup=key,
                              message_id=callback.message.message_id,
                              parse_mode="HTML")

        functions.update_sost(chat_id, 0)


def handle_updates(updates):
    for message in updates:
        BD = DataBase()
        BD.user_logger(message.chat.id, message.chat.username)

        chat_id = message.chat.id
        time_stamp = message.date
        username = message.chat.username
        text = message.text

        try:
            if "start" in text:
                """Если реферальная ссылка"""
                if len(text) > 6 and text[7:9] == "r_":
                    referer_id = int(text[9:])
                    BD.new_referal(chat_id, referer_id)

                elif len(text) > 6 and text[7:9] == "v_":
                    voucher = message.text[9:]
                    resp = BD.get_voucher(voucher)
                    if resp["exist"] == True:
                        referer_id = resp["voucher"]["creator_chat_id"]
                        BD.new_referal(chat_id, referer_id)
        except:
            pass

        BD.close()

        s = "-------------------------------------------\n"
        line = "{} | {} | {} | {}".format(chat_id, username, text, time_stamp)

        with open(config.PATH_2_LOG, "a", encoding="utf-8") as f:
            f.write("{}\n".format(line))
            f.write(s)

    thread = threading.Thread(target=script.main)
    thread.start()

    script.check_qiwies()


bot.set_update_listener(handle_updates)
bot.polling(none_stop=True)
