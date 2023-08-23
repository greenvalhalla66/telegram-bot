from classes.database.info import DataBase as info
from classes.database.user import DataBase as user
from classes.database.money import DataBase as money
from classes.database.referal import DataBase as referal 
from classes.database.voucher import DataBase as voucher 
from classes.database.address import DataBase as address 
from classes.database.exchange import DataBase as exchange




class DataBase(user, money, referal, voucher, address, info, exchange):
	pass


