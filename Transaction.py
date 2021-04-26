from Account import Account


class Transaction:

    def __init__(self, sender: Account, reciever: Account, amount: int):
        self.sender = sender
        self.reciever = reciever
        self.validateAmount(amount)
        self.amount = amount

    def validateAmount(self, amount: int):
        if(amount > self.sender.value):
            raise ValueError("This is an invalid transaction")
        else:
            self.sender.value -= amount
            self.reciever.value += amount

    # def print():
    #     print()
