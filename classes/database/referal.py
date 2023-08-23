import time
import sqlite3





class DataBase:
    def new_referal(self, chat_id, referer):
        # Проверка refeра
        if self.profile(referer)["status"]  == "registered":
            # Узнаётся дата реги
            info = self.profile(chat_id)
            user_reg_time = info["profile"]["registration_date"] 

            # Если юзер зарегался меньше 20 сек назад
            if (round(time.time()) - user_reg_time) < 20:
                sql = "UPDATE Users SET referer = {} WHERE chat_id = {};"
                sql = sql.format(referer, chat_id)
                self.cursor.execute(sql)


    def all_referals(self, chat_id):
        referals = []
        sql = "SELECT id, chat_id FROM Users WHERE referer = {};"
        sql = sql.format(chat_id)
        self.cursor.execute(sql)

        for id, chat_id in self.cursor.fetchall():
            referals.append(chat_id)

        return referals


    def amount_referals(self, chat_id):
        sql = "SELECT id, chat_id FROM Users WHERE referer = {};"
        sql = sql.format(chat_id)
        self.cursor.execute(sql)

        return len(self.cursor.fetchall())




