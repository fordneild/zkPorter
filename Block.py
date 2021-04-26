from typing import List
from Transaction import Transaction
from Account import Account
from MerkelTree import getPorterStateRoot


class Block:
    # 315 is the real value for number of zkSync transfers capable of being fit into one block
    MAX_NUM_TRANSACTION = 315

    def __init__(self, porters: List[Account]):
        self.porterStateRoot = getPorterStateRoot(porters)
        self.transactions = []

    def addTransaction(self, transaction: Transaction):
        if len(self.transactions) > self.MAX_NUM_TRANSACTION:
            raise ValueError("Too many transactions for this block")
        else:
            self.transactions.append(transaction)

    def getCapacity(self):
        return self.MAX_NUM_TRANSACTION - len(self.transactions)

    def setPorterStateRoot(self, porters: List[Account]):
        self.porterStateRoot = getPorterStateRoot(porters)
