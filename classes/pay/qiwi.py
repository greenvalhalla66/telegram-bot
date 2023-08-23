import config

# Мои библы
import myqiwi # Самопис модуль киви



class QApi:
    def __init__(self, num, token):
        self.num = num
        self.qiwi = myqiwi.Wallet(token, number=num)

    def balance(self):
        balance = self.qiwi.balance()
        balance = round(balance * 0.98)
        return balance

    def gen_comment(self):
        return self.qiwi.gen_comment()

    def pay_form(self, sum, comment):
        link = self.qiwi.generate_pay_form(self.num, sum=sum, comment=comment)
        return link

    def search_payment(self, need_sum, need_comment):
        payments = self.qiwi.history(rows=30, currency=643, operation="IN")
        resp = {"status": False}

        for i in payments:
            comment = payments[i]["comment"]
            sum = payments[i]["sum"]["amount"]

            if comment == need_comment and sum == round(need_sum):
                payment = payments[i]
                resp = {
                        "status": True,
                        "payment": payment
                        }
                break

        return resp

    def send(self, number, sum, warnings=True):
        response = self.qiwi.send(number, sum, warnings=warnings)

        return response


    def check_valid_account(self, recipient, sum=1):
        try:
            try_send = self.send(recipient, sum, warnings=False)

            if "code" in try_send and "QWPRC-1021" == try_send["code"]:
                response = False

            else:
                response = True

        except:
            response = False




        return response



        

