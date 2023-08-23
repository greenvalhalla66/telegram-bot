import time
import random
import sqlite3



class DataBase:
    def new_voucher(self, creator_chat_id, sum):
        vouchers = self.get_amount_str_in_table("Vouchers")
        now_time = round(time.time())
        value = None
        code = self.gen_code()

        sql = "INSERT INTO Vouchers VALUES (?, ?, ?, ? ,?, ?, ?, ?)"
        values = (vouchers+1, code, "not_activated",  creator_chat_id, 
                                                sum, now_time, value, value)

        self.cursor.execute(sql, values)

        # Создание фин.операции 
        type = "removal"
        comm = "create_voucher {}".format(vouchers+1)

        self.money_operation(creator_chat_id, sum, type, comm)

        return code


    def gen_code(self):
        sumn = list("1234567890ablmnopqrstuvyxwzA3BCDEFGHIGKLMNOPQRSTUVYXW64Z") 
        random.shuffle(sumn)
        code = ''.join([random.choice(sumn) for x in range(25)])
        return code 


    def activate_voucher(self, voucher_code, chat_id):
        now_time = round(time.time())

        # Получение данных о ваучере
        voucher = self.get_voucher(voucher_code)["voucher"]
        id = voucher["id"]
        creator_chat_id, sum = voucher["creator_chat_id"], voucher["sum"]

        # Внесение изменений в таблицу с ваучерами
        sql = "UPDATE Vouchers SET status = 'activated', date_use = {}, \
                                        user_chat_id = {} WHERE code = '{}';"
        sql = sql.format(now_time, chat_id, voucher_code)
        self.cursor.execute(sql)


        # Создание фин.операции у юзера
        type = "refill"
        comm = "activate_voucher {}".format(id)

        self.money_operation(chat_id, sum, type, comm)

        return creator_chat_id, sum


    def get_voucher(self, code):
        resp = {}

        sql = "SELECT * FROM Vouchers WHERE code = '{}';".format(code)
        self.cursor.execute(sql)
        result = self.cursor.fetchone()

        if result == None:
            resp["exist"] = False
            resp["status"] = "not_activated"

        else:
            resp["exist"] = True
            resp["status"] = "activated"

            id, code, status, creator_chat_id, sum, create_date, \
            date_use, user_chat_id = result

            if status == "not_activated":
                resp["status"] = "not_activated"


            resp["voucher"] = {
                                "id": id,
                                "creator_chat_id": creator_chat_id,
                                "sum": sum,
                                "create_date": create_date,
                                "date_use": date_use,
                                "user_chat_id": user_chat_id
                               }


        return resp


    def user_notactivated_vouchers(self, chat_id):
        resp = {
                "amount": 0,
                "vouchers": {}
                }
        amount = 0

        sql = "SELECT id, code, sum FROM Vouchers WHERE creator_chat_id = {} \
        AND status = 'not_activated';".format(chat_id)

        self.cursor.execute(sql)

        for id, code, sum in self.cursor.fetchall():
            resp["vouchers"][amount] = {
                                            "id": id,
                                            "code": code,
                                            "sum": sum
                                         }
            amount += 1

        resp["amount"] = amount
        return resp



