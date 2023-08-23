import time
import sqlite3

# Мои библы
import config # Конфиг

# Библы из папок
from classes.pay import bitcoin



class DataBase:
    def __init__(self, path=config.PATH_2_BD):
        self.con = sqlite3.connect(path)
        self.cursor = self.con.cursor()

    def user_logger(self, chat_id, username):
        now_time  = round(time.time())

        if self.profile(chat_id)["status"] == "not_registered":
            self.__new_user(chat_id, username)

        else: # Если зареган
            sql = "UPDATE Users SET username = '{}', last_use = {} WHERE chat_id = {};"
            sql = sql.format(username, now_time, chat_id)
            self.cursor.execute(sql)

    def get_amount_str_in_table(self, table_name):
        self.cursor.execute("SELECT * FROM {}".format(table_name))
        amount = len(self.cursor.fetchall())
        return amount


    def __new_user(self, chat_id, username, referer=None):
        time_now = round(time.time()) # Текущее время
        users = self.get_amount_str_in_table("Users") + 1 # Кол-во юзеров

        sql = "INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        values = (users, chat_id, username, 0, 0, time_now, time_now, referer)

        self.cursor.execute(sql, values)



    def last_btc_wallet(self, chat_id):
        sql = "SELECT id, address FROM Byu_btc WHERE chat_id = {} ORDER BY \
                                                                id DESC;"
        sql = sql.format(chat_id)
        self.cursor.execute(sql)
        address = self.cursor.fetchone()
        if address != None:
            id, address = address
        return address

    def last_qiwi_wallet(self, chat_id):
        sql = "SELECT id, qiwi_number FROM Sell_btc WHERE chat_id = {} ORDER BY \
                                                                id DESC;"
        sql = sql.format(chat_id)
        self.cursor.execute(sql)
        qiwi_num = self.cursor.fetchone()
        if qiwi_num != None:
            id, qiwi_num = qiwi_num
        return qiwi_num


    def profile(self, chat_id, search_by="chat_id"):
        resp = {}
        if search_by == "username": chat_id = "'{}'".format(chat_id)

        sql = "SELECT * FROM Users WHERE {} = {};".format(search_by, chat_id)
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        
        if result == None:
            resp["status"] = "not_registered"


        else: # Если пользователь зареган
            resp["status"] = "registered"

            id, chat_id, username, balance, referal_income, \
            registration_date, last_use, referer = result

            last_btc_wallet = self.last_btc_wallet(chat_id)
            last_qiwi_wallet = self.last_qiwi_wallet(chat_id)
            amount_exchanges = self.amount_user_exchanges(chat_id)


            resp["profile"] = {
                            "id": id,
                            "chat_id": chat_id,
                            "username": username,
                            "balance": balance,

                            "registration_date": registration_date,
                            "last_use": last_use,
                            "referer": referer,

                            "exchanges": { 
                                        "amount": amount_exchanges,
                                        "sum": self.sum_user_exchanges(chat_id)
                                        },

                            "last_wallet": {
                                            "btc": last_btc_wallet,
                                            "qiwi": last_qiwi_wallet
                            },
                            "ref":  {
                                    "amount": self.amount_referals(chat_id),
                                    "income": referal_income
                                    }
                            }   

      
        return resp


    def all_users(self):
        users = []

        sql = "SELECT id, chat_id FROM Users"
        self.cursor.execute(sql)
        for id, chat_id in self.cursor.fetchall():
            users.append(chat_id)

        return users


    def close(self):
        self.con.commit()
        self.con.close()


        