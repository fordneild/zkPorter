from typing import List
from Transaction import Transaction
from Account import Account
from MerkelTree import getStateRoot


class Block:
    # 315 is the real value for number of zkSync transfers capable of being fit into one block
    MAX_NUM_TRANSACTION = 315

    def __init__(self, porters: List[Account], rollups: List[Account]):
        self.porterStateRoot = getStateRoot(porters)
        self.newRollupStateRoot = getStateRoot(rollups)
        self.prevRollupStateRoot = (self.newRollupStateRoot + '.')[:-1]
        self.transactions: List[Transaction] = []

    def addTransaction(self, transaction: Transaction):
        if len(self.transactions) > self.MAX_NUM_TRANSACTION:
            raise ValueError("Too many transactions for this block")
        else:
            self.transactions.append(transaction)

    def getCapacity(self):
        return self.MAX_NUM_TRANSACTION - len(self.transactions)

    def setPorterStateRoot(self, porters: List[Account]):
        self.porterStateRoot = getStateRoot(porters)

    def setRollupStateRoot(self, rollups: List[Account]):
        self.prevRollupStateRoot = (self.newRollupStateRoot + '.')[:-1]
        self.newRollupStateRoot = getStateRoot(rollups)
    
    def __str__(self) -> str:
        return "Block------------------------\n"+'porterStateRoot: ' + str(self.porterStateRoot) +\
               '\nprevRollupStateRoot: ' + str(self.prevRollupStateRoot) + \
               '\nnewRollupStateRoot: ' + str(self.newRollupStateRoot) + '\ntransactions:' + str(self.transactions) + \
               "\n-----------------------------"
    
    def __repr__(self) -> str:
        return self.__str__()
