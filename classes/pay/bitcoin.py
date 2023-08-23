import config
import requests
from coinbase.wallet.client import Client

# Библы из папок
import etc.functions as functions  # Дополнительные функции
from classes.database import DataBase


class Btc:
    def __init__(self, api_key=config.API_KEY, private_key=config.PRIVATE_KEY):
        self.client = Client(api_key, private_key)
        self.account_id = self.client.get_primary_account()["id"]

    def create_address(self):
        resp = self.client.create_address(self.account_id)
        resp = {
            "address": resp["address"],
            "address_id": resp["id"]
        }
        return resp

    def convert(self, currency, sum, btc_price=None):
        if btc_price == None:
            btc_price = self.price()
        if currency == "rub":
            sum = round(sum / btc_price, 8)

        elif currency == "btc":
            sum = round(btc_price * sum)

        elif currency == "sts":
            ln = 8 - len(str(sum))  # Сколько нулей нужно ещё до 8
            sum = "0.{}{}".format("0" * ln, sum)  # И создаётся сумма с нулями
            sum = float(sum)

        return sum

    def price(self):
        price = self.client.get_buy_price(currency_pair="BTC-RUB")
        price = int(price["amount"][0:7])
        return price

    def address_balance(self, address):
        url = "https://blockchain.info/q/addressbalance/{}".format(address)
        r = requests.get(url)
        sum = int(r.text)
        return sum

    def send(self, address, sum):
        sum = functions.round(sum)

        DB = DataBase()
        a_info = DB.get_address_info(address)
        if a_info != None:  # Если такой адрес есть в бд
            chat_id = a_info["chat_id"]
            DB.money_operation(chat_id, float(sum), "refill", "refill")

        else:
            acc_id = self.account_id
            self.client.send_money(
                acc_id, to=address, amount=sum, currency="BTC")
        DB.close()

    def balance(self):
        balance = self.client.get_primary_account()["balance"]["amount"]
        # print(balance)
        balance = float(balance)
        return balance

    def price_with_comission(self, comission, btc_price=None):
        if btc_price == None:
            btc_price = self.price()
        comission = 1 + comission / 100  # Типо 1.10
        btc_price = btc_price * comission
        btc_price = round(btc_price)

        return btc_price
