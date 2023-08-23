import config

# Библы из папок
import etc.messages as messages # Сообщения
from classes.pay import bitcoin
import etc.adminka.helper as helper


class DataBase:
    def new_btc_byu(self, chat_id, address, sum_in_btc, sum_in_rub):
        self.referal_income(chat_id, sum_in_btc * (config.commission_on_byu / 100))

        notification = messages.admin_notific_about_money(chat_id, "btc_byu", sum_in_btc)
        helper.admin_notifications(notification)

        btc_price = bitcoin.Btc().price()
        exchanges = self.get_amount_str_in_table("Byu_btc")
        sql = "INSERT INTO Byu_btc VALUES (?, ?, ?, ?, ?, ?)"
        values = (exchanges+1, chat_id, address, btc_price, sum_in_btc, 
                                                                    sum_in_rub)
        self.cursor.execute(sql, values)

    def new_btc_sell(self, chat_id, qiwi_num, sum_in_btc, sum_in_rub):
        self.referal_income(chat_id, sum_in_btc * (config.commission_on_sell*-1 / 100))

        notification = messages.admin_notific_about_money(chat_id, "btc_sell", sum_in_btc)
        helper.admin_notifications(notification)

        btc_price = bitcoin.Btc().price()
        exchanges = self.get_amount_str_in_table("Sell_btc")
        sql = "INSERT INTO Sell_btc VALUES (?, ?, ?, ?, ?, ?)"
        values = (exchanges+1, chat_id, qiwi_num, btc_price, sum_in_btc, 
                                                                    sum_in_rub)
        self.cursor.execute(sql, values)

    def amount_user_exchanges(self, chat_id):
        amount = 0
        sql = "SELECT id FROM Byu_btc WHERE chat_id = {};".format(chat_id)
        self.cursor.execute(sql)
        amount += len(self.cursor.fetchall())

        sql = "SELECT id FROM Sell_btc WHERE chat_id = {};".format(chat_id)
        self.cursor.execute(sql)
        amount += len(self.cursor.fetchall())
        return amount

    def sum_user_exchanges(self, chat_id):
        sum = 0
        sql = "SELECT id, sum_in_btc FROM Byu_btc WHERE chat_id = {};"
        sql = sql.format(chat_id)
        self.cursor.execute(sql)
        for id, sum_in_btc in self.cursor.fetchall():
            sum += sum_in_btc

        sql = "SELECT id, sum_in_btc FROM Sell_btc WHERE chat_id = {};"
        sql = sql.format(chat_id)
        self.cursor.execute(sql)
        for id, sum_in_btc in self.cursor.fetchall():
            sum += sum_in_btc

        return sum

