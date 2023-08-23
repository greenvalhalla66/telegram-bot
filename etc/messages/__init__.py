import datetime

# Мои библы
import config  # Конфиг

# Библы из папок
import etc.functions as functions
from classes.pay import bitcoin
import etc.messages.message_text as messages


def soglas():
    return messages.soglas.format(config.RULES)


def start():
    return messages.start.format(config.bot_name, config.FAQ)


def rules():
    return messages.rules


def incorrect_voucher():
    return messages.incorrect_voucher_code


def your_voucher_acvtivate(sum):
    return messages.your_voucher_acvtivate.format(sum)


def profile(chat_id, reg_date, referals, referal_income):
    reg_date = str(datetime.datetime.fromtimestamp(reg_date))[:10].split("-")
    reg_date = "{}-{}-{}".format(reg_date[2], reg_date[1], reg_date[0])
    referal_income = functions.round(referal_income)

    mes = messages.profile.format(chat_id, reg_date, referals, referal_income)
    return mes


def wallet(chat_id, reg_date, balance, in_rub):
    reg_date = str(datetime.datetime.fromtimestamp(reg_date))[:10].split("-")
    reg_date = "{}-{}-{}".format(reg_date[2], reg_date[1], reg_date[0])
    # referal_income = functions.round(referal_income)
    balance = float(balance)
    balance = functions.round(balance)
    #sum_exchange = functions.round(sum_exchange)
    mes = messages.wallet
    mes = mes.format(chat_id, reg_date, balance, in_rub)
    return mes


def info(exchanges, sum_exchange):
    #comissions = config.commission_on_sell
    sum_exchange = functions.round(sum_exchange)
    #btc = bitcoin.Btc()
    #btc_price = btc.price()
    #btc_prices = bitcoin.Btc().price_with_comission(comissions, btc_price=btc_price)
    #comissionb = config.commission_on_byu
    #btc_pricesb = bitcoin.Btc().price_with_comission(comissionb, btc_price=btc_price)
    return messages.info.format(exchanges, sum_exchange)


def when_btc_refill():
    return messages.when_btc_refill.format(config.need_confirmations)


def when_btc_came(sum):
    sum = functions.round(sum)
    return messages.when_btc_came.format(sum)


def min_removal():
    min_removal = config.ON_REMOVAL  # Мин сумма вывода
    commission = config.REMOVAL  # Комиссия на вывод
    #min_balance = functions.min_balance(min_removal, commission)
    min_balance = min_removal + commission
    min_balance = round(min_balance, 8)
    return messages.min_removal.format(min_balance, min_removal, commission)


def sum_removal(balance):
    commission = config.REMOVAL  # Комиссия на вывод
    min_removal = config.ON_REMOVAL  # Сумма мин вывода

    max_removal = functions.max_removal(balance, commission)

    mes = messages.sum_removal
    return mes.format(balance, commission, min_removal, max_removal)


def removal(address, sum_removal, balance):
    commission = config.REMOVAL

    balance = round(balance, 8)
    sum_removal = round(sum_removal, 8)
    will_balance = balance - (sum_removal + commission)
    #will_balance = functions.will_on_balance(balance, sum_removal, commission)
    will_balance = round(will_balance, 8)
    #commission = functions.commission_on_removal(sum_removal, commission)
    commission = round(commission, 4)
    mes = messages.removal

    return mes.format(address, sum_removal, commission, will_balance)


def admin_notific_about_money(chat_id, oparation_name, sum):
    sum = functions.round(sum)

    mes = messages.admin_notific_about_money
    mes = mes.format(chat_id, oparation_name, sum)
    return mes


def when_money_transfer():
    return messages.when_money_transfer


def removal_address():
    return messages.removal_address


def when_sum_transfer(balance):
    balance = round(balance, 8)
    return messages.when_sum_transfer.format(balance)


def transfer(payee_id, sum_removal, balance):
    balance = float(balance)
    balance = round(balance, 8)
    sum_removal = float(sum_removal)
    sum_removal = round(sum_removal, 8)
    will_balance = balance - sum_removal

    #will_balance = functions.round(will_balance)
    mes = messages.transfer.format(payee_id, sum_removal, will_balance)
    return mes


def when_not_username():
    return messages.when_not_username


def voucher():
    return messages.voucher


def create_voucher(balance):
    balance = functions.round(balance)
    return messages.create_voucher.format(balance)


def when_create_voucher(code, sum, link):
    sum = functions.round(sum)
    mes = messages.when_create_voucher.format(code, sum, link)
    return mes


def my_vouchers(sum, code, link):
    sum = functions.round(sum)
    mes = messages.my_vouchers.format(sum, code, link)
    return mes


def one_step_byu_btc(balance_in_btc):
    #commission = config.commission_on_byu
    btc = bitcoin.Btc()
    btc_price = btc.price()
    max_in_rub = btc.convert("btc", balance_in_btc, btc_price=btc_price)
    min_in_btc = btc.convert("rub", config.min_byu_btc, btc_price=btc_price)

    # max_in_btc = round(balance_in_btc, 8)
    # max_in_b#tc = float(balance_in_btc)
    #min_in_btc = float(min_in_btc)
    #min_in_btc = float(min_in_btc)
    min_in_btc = functions.round(min_in_btc)
    #min_in_btc = functions.round(min_in_btc)

    mes = messages.one_step_byu_btc
    return mes.format(config.min_byu_btc, max_in_rub, min_in_btc, config.max_in_btc)


def re_step_byu_btc(balance_in_btc):
    btc = bitcoin.Btc()
    btc_price = btc.price()
    max_in_rub = btc.convert("btc", balance_in_btc, btc_price=btc_price)
    min_in_btc = btc.convert("rub", config.min_byu_btc, btc_price=btc_price)

    # max_in_btc = round(balance_in_btc, 8)

    min_in_btc = round(min_in_btc, 8)

    mes = messages.re_step_byu_btc
    return mes.format(min_in_btc, config.max_in_btc, config.min_byu_btc, max_in_rub)


def two_step_byu_btc(btc_price, sum_in_rub, sum_in_btc):
    commission = config.commission_on_byu
    btc = bitcoin.Btc()
    btc_price = btc.price_with_comission(commission, btc_price=btc_price)

    sum_in_rub = float(sum_in_rub)
    sum_in_rub = round(sum_in_rub)
    sum_in_btc = functions.round(sum_in_btc)
    #need_me = float(need_me)
    #need_send = functions.round(need_send)
    #need_me = round(need_me)

    mes = messages.two_step_byu_btc
    mes = mes.format(btc_price, sum_in_rub, sum_in_btc)
    return mes


def three_step_byu_btc():
    return messages.three_step_byu_btc


def four_step_byu_btc(need_me, qiwi_phone, comment, need_send):
    need_me = float(need_me)
    need_me = round(need_me)
    need_send = functions.round(need_send)
    mes = messages.four_step_byu_btc
    mes = mes.format(need_me, qiwi_phone, comment, need_send)
    return mes


def when_user_pay(sum):
    sum = functions.round(sum)
    return messages.when_user_pay.format(sum)


def one_step_sell_btc(qiwi_balance):
    #commission = config.commission_on_sell
    btc = bitcoin.Btc()
    btc_price = btc.price()

    min_in_btc = btc.convert("rub", config.min_sell_btc, btc_price=btc_price)
    # max_in_btc = btc.convert("rub", qiwi_balance, btc_price=btc_price)

    min_in_btc = round(min_in_btc, 8)
    # max_in_btc = round(config.max_in_btc, 8)

    mes = messages.one_step_sell_btc
    return mes.format(min_in_btc, config.max_in_btc, config.min_sell_btc, qiwi_balance)


def re_step_sell_btc(qiwi_balance):
    btc = bitcoin.Btc()
    btc_price = btc.price()

    min_in_btc = btc.convert("rub", config.min_sell_btc, btc_price=btc_price)
    # config.max_in_btc = btc.convert("rub", qiwi_balance, btc_price=btc_price)

    min_in_btc = round(min_in_btc, 8)
    # config.max_in_btc = round(config.max_in_btc, 8)

    mes = messages.re_step_sell_btc
    return mes.format(min_in_btc, config.max_in_btc, config.min_sell_btc, qiwi_balance)


def two_step_sell_btc(btc_price, sum_in_btc, sum_in_rub):
    comission = config.commission_on_sell

    btc_price = bitcoin.Btc().price_with_comission(comission, btc_price=btc_price)

    sum_in_btc = round(sum_in_btc, 8)
    sum_in_rub = round(sum_in_rub)
    mes = messages.two_step_sell_btc
    mes = mes.format(btc_price, sum_in_btc, sum_in_rub)
    return mes


def three_step_sell_btc():
    return messages.three_step_sell_btc


def four_step_sell_btc(qiwi_num, need_me, need_send):
    need_me = round(need_me, 8)
    need_send = round(float(need_send))
    mes = messages.four_step_sell_btc
    mes = mes.format(need_me, need_send, qiwi_num)
    return mes


def five_step_sell_btc(sum, qiwi_num):
    sum = round(float(sum))
    return messages.five_step_sell_btc.format(sum, qiwi_num)


def ref_message(link, referals, referal_income):
    referal_income = functions.round(referal_income)
    return messages.ref_message.format(config.REFERAL_INCOME, link, referals, referal_income)


def if_nevalid_address():
    return messages.if_nevalid_address
