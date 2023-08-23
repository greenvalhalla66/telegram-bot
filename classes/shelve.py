import shelve

# Мои библы
import config # Конфиг


class Temp:
	def __init__(self, chat_id, path=config.PATH_2_SH):
		self.chat_id = chat_id
		self.bd = shelve.open(path)


	def write_btc_address(self, address):
		key = "a_{}".format(self.chat_id)
		self.bd[key] = address

	def get_btc_address(self):
		key = "a_{}".format(self.chat_id)
		return self.bd[key]


	def write_sum_in_btc(self, sum):
		key = "sb_{}".format(self.chat_id)
		self.bd[key] = sum

	def get_sum_in_btc(self):
		key = "sb_{}".format(self.chat_id)
		return self.bd[key]


	def write_sost(self, sost):
		key = "s_{}".format(self.chat_id)
		self.bd[key] = sost

	def get_sost(self):
		key = "s_{}".format(self.chat_id)
		return self.bd[key]


	def need_send(self, sum):
		key = "nd_{}".format(self.chat_id)
		self.bd[key] = sum

	def need_me(self, sum):
		key = "nm_{}".format(self.chat_id)
		self.bd[key] = sum

	def get_need_send(self):
		key = "nd_{}".format(self.chat_id)
		return self.bd[key]

	def get_need_me(self):
		key = "nm_{}".format(self.chat_id)
		return self.bd[key]


	def write_comment(self, comment):
		key = "c_{}".format(self.chat_id)
		self.bd[key] = comment

	def get_comment(self):
		key = "c_{}".format(self.chat_id)
		return self.bd[key]


	def write_qiwi_data(self, qiwi_data):
		key = "w_q_d{}".format(self.chat_id)
		self.bd[key] = qiwi_data

	def qiwi_data(self):
		key = "w_q_d{}".format(self.chat_id)
		return self.bd[key]






	def write_admin_sost(self, sost):
		key = "a_s_{}".format(self.chat_id)
		self.bd[key] = sost

	def get_admin_sost(self):
		key = "a_s_{}".format(self.chat_id)
		return self.bd[key]


	def close(self):
		self.bd.close()