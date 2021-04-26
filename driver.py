from Block import Block
from typing import List
from Account import Account
from Transaction import Transaction
import random
import numpy as np


def simulateRollup(numPorters: int, numRollups: int, numTx: int, seed=123456):

    # init account arrays
    porterAccounts: List[Account] = []
    rollupAccounts: List[Account] = []
    # generate zk-porter accounts
    for i in range(numPorters):
        porterAccounts.append(Account("porter" + str(i), isPorter=True))
    # generate zk-rollup accounts
    for i in range(numRollups):
        rollupAccounts.append(Account("rollup" + str(i), isPorter=False))

    random.seed(seed)
    # generate transactions
    blocks: List[Block] = []
    block = Block(porterAccounts)
    all_accounts = []
    num_porter_txs = 0
    for t in range(numTx):
        """
        # sample sender from porters or rollups depending on weighted coin toss
        sender = random.choice(
            porters) if random.random() < probSenderPorter else random.choice(rollups)
        # sample receiver from porters or rollups depending on weighted coin toss
        receiver = random.choice(
            porters) if random.random() < probReceiverPorter else random.choice(rollups)
        """
        # combine all accounts to randomly sample from
        all_accounts = rollupAccounts.copy()
        for acct in porterAccounts:
            all_accounts.append(acct)
        sender = random.choice(all_accounts)
        while True:
            receiver = random.choice(all_accounts)
            if sender != receiver:
                break

        # sender gifts random amount of their money away
        amount = int(random.random() * sender.value)
        tx = Transaction(sender, receiver, amount)
        # if they are both porters
        # TODO only for last porter-to-porter do we need to recompute
        if sender.isPorter and receiver.isPorter:
            num_porter_txs = num_porter_txs + 1
            block.setPorterStateRoot(porterAccounts)
        else:
            if block.getCapacity() == 0:
                blocks.append(block)
                block = Block(porterAccounts)
            block.addTransaction(tx)
    blocks.append(block)

    # Output data
    porter_percentage = (numPorters / (numRollups + numPorters)) * 100
    #print(str(len(blocks)))
    print(str(len(blocks)) + " blocks required for " +
          str(numTx) + " transaction(s) when " + str(porter_percentage) + "% of accounts are zkPorters.")

    # Known variables for real-world transfers
    blocks_per_sec = float(1/13)
    gaslimit_per_block = float(12500000)
    trans_per_gasunit = float(1/1184)
    amortized_blocks_per_sec = float(2.54)

    # get average number of transfers per block
    num_transfers = 0
    for b in range(len(blocks)):
        for transfer in blocks[b].transactions:
            num_transfers = num_transfers + 1
    avg_num_transfers_per_block = num_transfers / len(blocks)
    avg_num_porter_txs = num_porter_txs / len(blocks)

    tps = (avg_num_transfers_per_block + avg_num_porter_txs) * amortized_blocks_per_sec
    #print(str(np.round(tps, 2)))
    print(str(np.round(tps, 2)) + " transactions per second when " + str(porter_percentage) +
          "% of accounts are zkPorters.")


if __name__ == "__main__":

    # initialize the network proportions of each account type
    NUM_PORTERS = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 9500, 9800, 9990]
    NUM_ROLLUPS = [10000, 9000, 8000, 7000, 6000, 5000, 4000, 3000, 2000, 1000, 500, 200, 10]
    NUM_TXS = 5000

    # simulate just roll up scenarios
    for i in range(len(NUM_ROLLUPS)):
        simulateRollup(NUM_PORTERS[i], NUM_ROLLUPS[i], NUM_TXS)

    # P(A porter is involved) = P(porter is sender) + P(porter is receiver) - P(porter is both)
    # P(Porter is both)  = P(porter is sender) * P(porter is receiver)
