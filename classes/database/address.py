import time
import sqlite3

# Библы из папок
from classes.pay import bitcoin



class DataBase:
    def generate_btc_address(self, chat_id):
        addresses = self.get_amount_str_in_table("Addresses")
        time_now = round(time.time()) # Текущее время
        a = bitcoin.Btc().create_address()
        address = a["address"]
        address_id = a["address_id"]

        sql = "INSERT INTO Addresses VALUES (?, ?, ?, ?, ?, ?)"
        values = (addresses+1, chat_id, 0, address, address_id, time_now)
        self.cursor.execute(sql, values)

        return address

    def get_btc_address(self, chat_id):
        sql = "SELECT id, address FROM Addresses WHERE chat_id = {}"
        sql = sql.format(chat_id)
        self.cursor.execute(sql)
        result = self.cursor.fetchone()

        # Если для юзера ещё адресов не генерировалось
        if result == None:
            address = self.generate_btc_address(chat_id)
        # Если генерировались
        else:
            id, address = result

        return address

    def get_address_info(self, address):
        sql = "SELECT id, chat_id, date FROM Addresses WHERE address = '{}';"
        sql = sql.format(address)
        self.cursor.execute(sql)
        result = self.cursor.fetchone()

        if result == None:
            resp = None

        else: # Если адрес есть в бд

            id, chat_id, date = result

            resp = {
                    "id": id,
                    "chat_id": chat_id,
                    "date": date
                    }
      
        return resp


    def delete_addresses(self):
        sql = "DELETE FROM Addresses"
        self.cursor.execute(sql)



