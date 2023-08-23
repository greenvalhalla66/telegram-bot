import time
import random
import sqlite3

class DataBase:
	def users_balance(self):
		balances = 0
		sql = "SELECT id, balance FROM Users WHERE balance > 0;"
		self.cursor.execute(sql)
		for id, balance in self.cursor.fetchall():
			balances += balance
		return balances


	def get_qiwies(self):
		qiwies = []

		sql = "SELECT * FROM Qiwies"
		self.cursor.execute(sql)
		for phone, token, balance, time_stamp in self.cursor.fetchall():
			qiwi = {
				"phone": int(phone),
				"token": token,
				"balance": round(balance * 0.98),
				"time_stamp": time_stamp

			}
			qiwies.append(qiwi)

		random.shuffle(qiwies)

		return qiwies


	def add_qiwi(self, phone, token, balance):
		for qiwi in self.get_qiwies():
			if qiwi["phone"] == phone:
				return 


		sql = "INSERT INTO Qiwies VALUES (?, ?, ?, ?)"
		values = (phone, token, balance, round(time.time()))
		self.cursor.execute(sql, values)

			
		
	def del_qiwi(self, phone):
		sql = "DELETE FROM Qiwies WHERE phone = '{}'".format(phone)
		self.cursor.execute(sql)


	
	def update_qiwi(self, what, phone, new_balance):
		sql = "UPDATE Qiwies SET {} = {} WHERE phone = '{}'"
		sql = sql.format(what, new_balance, phone)

		self.cursor.execute(sql)



	def stats(self):
		sql = "SELECT * FROM Users"
		self.cursor.execute(sql)
		users = len(self.cursor.fetchall())


		day = round(time.time()) - 86400
		sql = "SELECT * FROM Users WHERE last_use > {}".format(day)
		self.cursor.execute(sql)
		active_users = len(self.cursor.fetchall())


		response = {
			"users": users,
			"active_users": active_users
		}

		return response



