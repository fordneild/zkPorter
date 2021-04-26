from typing import List
from Transaction import Transaction
from Account import Account
from MerkelTree import getPorterStateRoot


class Block:
    # 100 is the real value
    MAX_NUM_TRANSACTION = 10

    def __init__(self, porters: List[Account]):
        self.transactions = []
        self.porterStateRoot = self.setPorterStateRoot(porters)

    def addTransaction(self, transaction: Transaction):
        if(len(self.transactions) > self.MAX_NUM_TRANSACTION):
            raise ValueError("Too many transactions for this block")
        else:
            self.transactions.append(transaction)

    def getCapacity(self):
        return self.MAX_NUM_TRANSACTION - len(self.transactions)

    def setPorterStateRoot(self, porters: List[Account]):
        self.porterStateRoot = getPorterStateRoot(porters)
