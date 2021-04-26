from Block import Block
from typing import List
from Account import Account
from Transaction import Transaction
import random
import numpy as np


def simulateRollup(porters: List[Account], rollups: List[Account], numTx: int, probSenderPorter=.5, probRecieverPorter=.5, seed=123456):
    random.seed(seed)
    # generate transactions
    blocks: List[Block] = []
    block = Block(porters)
    for i in range(numTx):
        # sample sender from porters or rollups depending on weighted coin toss
        sender = random.choice(
            porters) if random.random() < probSenderPorter else random.choice(rollups)
        # sample reciever from porters or rollups depending on weighted coin toss
        reciever = random.choice(
            porters) if random.random() < probRecieverPorter else random.choice(rollups)
        # sender gifts random amount of their money away
        amount = int(random.random() * sender.value)
        tx = Transaction(sender, reciever, amount)
        # if they are both porters
        # TODO only for last porter-to-porter do we need to recompute
        if sender.isPorter and reciever.isPorter:
            block.setPorterStateRoot(porters)
        else:
            if(block.getCapacity() == 0):
                blocks.append(block)
                block = Block(porters)
            block.addTransaction(tx)
    blocks.append(block)
    print(str(len(blocks)) + " blocks required for " +
          str(numTx) + " transaction(s)")
    # tps = numTx/(len(blocks)*15)
    # print(str(np.round(tps, 2)) + " transactions per second")


if __name__ == "__main__":
    # initalize constats for simulation
    NUM_PORTER_ACCOUNTS = 10
    NUM_ROLLUP_ACCOUNTS = 10
    # init account arrays
    porterAccounts: List[Account] = []
    rollupAcounts: List[Account] = []
    # generate zk-porter accounts
    for i in range(NUM_PORTER_ACCOUNTS):
        porterAccounts.append(Account("porter" + str(i), isPorter=True))
    # generate zk-rollup accounts
    for i in range(NUM_ROLLUP_ACCOUNTS):
        rollupAcounts.append(Account("rollup" + str(i), isPorter=False))
    # simulate just roll up for 50 txs
    simulateRollup(porterAccounts, rollupAcounts, 5000, 0, 0)
    simulateRollup(porterAccounts, rollupAcounts, 5000, .2, .2)
    simulateRollup(porterAccounts, rollupAcounts, 5000, .5, .5)
    simulateRollup(porterAccounts, rollupAcounts, 5000, .7, .7)
    simulateRollup(porterAccounts, rollupAcounts, 5000, .9, .9)
    simulateRollup(porterAccounts, rollupAcounts, 5000, .95, .95)
    simulateRollup(porterAccounts, rollupAcounts, 5000, .99, .99)
    simulateRollup(porterAccounts, rollupAcounts, 5000, 1, 1)
