import time
import sqlite3

# Мои библы
import config # Конфиг

# Библы из папок
import etc.messages as messages # Сообщения
import etc.adminka.helper as helper



class DataBase:
    def money_operation(self, chat_id, sum, type, comm):
        """
        type Тип операции. Может быть 
                    refill - пополнение(к юзеру придёт)
                    removal - снятие(т.е у юзера вычтеться)

        comm Описание операции. Может быть
                    revearal_income(Доход с рефералки)
                    activate_voucher(Активация ваучера) + id ваучера
                    create_voucher(Оплата ваучера) + id ваучера
                    refill(Пополнение счёта) 
                    removal(Вывод денег с счёта)
                    transfer(Перевод денег юзеру по chat_id) + chat_id получателя
                    get_transfer(Получение перевода)
                    commission(Комиссия)
        """
        # Уведомление админов
        notification = messages.admin_notific_about_money(chat_id, comm, sum)
        helper.admin_notifications(notification)
        #----------------------------------------------------------------------

        amount_operation = self.get_amount_str_in_table("Money_operation")
        sum = round(sum, 8)
        
        # Добавление фин операции в таблицу
        sql = "INSERT INTO Money_operation VALUES(?, ?, ?, ?, ?)"
        values = (amount_operation+1, sum, chat_id, type, comm)
        self.cursor.execute(sql, values)

        # Вычет или пополнение денег в таблице Users
        balance = self.profile(chat_id)["profile"]["balance"]

        if type == "refill": new_balance = balance + sum
        elif type == "removal": new_balance = balance - sum
        new_balance = "{:.10f}".format(new_balance).rstrip("0")

        sql = "UPDATE Users SET balance = {} WHERE chat_id = {};"
        sql = sql.format(new_balance, chat_id)
        self.cursor.execute(sql)


    def referal_income(self, chat_id, sum):
        profile  = self.profile(chat_id)["profile"]
        referer = profile["referer"]

        if referer != None:
            sum = sum * (config.REFERAL_INCOME / 100)

            referal_income = self.profile(referer)["profile"]["ref"]["income"] + sum
    
            sql = "UPDATE Users SET referal_income = {} WHERE chat_id = {};"
            sql = sql.format(referal_income, referer)
            self.cursor.execute(sql)

            self.money_operation(referer, sum, "refill", "referal_income")







