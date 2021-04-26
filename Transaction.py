from Account import Account


class Transaction:

    def __init__(self, sender: Account, receiver: Account, amount: int):
        self.sender = sender
        self.receiver = receiver
        self.validateAmount(amount)
        self.amount = amount

    def validateAmount(self, amount: int):
        if amount > self.sender.value:
            raise ValueError("This is an invalid transaction")
        else:
            self.sender.value -= amount
            self.receiver.value += amount

    # def print():
    #     print()
