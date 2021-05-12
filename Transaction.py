from typing import List
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
    
    def __str__(self) -> str:
        return "\n"+self.sender.id + "-$"+ str(self.amount) +"->"+ self.receiver.id

    def __repr__(self) -> str:
        return self.__str__()
