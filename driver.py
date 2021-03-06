from Block import Block
from typing import List
from Account import Account
from Transaction import Transaction
import random
import numpy as np
import matplotlib.pyplot as plt
import sys


def simulateRollup(numPorters: int, numRollups: int, numTx: int, seed=123456):
    # init account arrays
    porterAccounts: List[Account] = []
    rollupAccounts: List[Account] = []
    all_accounts: List[Account] = []
    # generate zk-porter accounts
    for i in range(numPorters):
        porter = Account("porter" + str(i), isPorter=True)
        porterAccounts.append(porter)
        all_accounts.append(porter)
    # generate zk-rollup accounts
    for i in range(numRollups):
        rollup = Account("rollup" + str(i), isPorter=False)
        rollupAccounts.append(rollup)
        all_accounts.append(rollup)

    random.seed(seed)
    # generate transactions
    blocks: List[Block] = []
    block = Block(porterAccounts, rollupAccounts)
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
        # randomly sample from all accounts to create transactions
        sender = random.choice(all_accounts)
        while True:
            receiver = random.choice(all_accounts)
            if sender != receiver:
                break

        # sender gifts random amount of their money away
        amount = int(random.random() * sender.value)
        tx = Transaction(sender, receiver, amount)

        # if they are both porters
        if sender.isPorter and receiver.isPorter:
            num_porter_txs = num_porter_txs + 1
        else:
            if block.getCapacity() == 0:
                block.setPorterStateRoot(porterAccounts)
                block.setRollupStateRoot(rollupAccounts)
                blocks.append(block)
                print(block)
                block = Block(porterAccounts, rollupAccounts)
            block.addTransaction(tx)
    block.setPorterStateRoot(porterAccounts)
    block.setRollupStateRoot(rollupAccounts)
    blocks.append(block)


    # print the block after we append it?
    # print(block)

    # Output data
    porter_percentage = (numPorters / (numRollups + numPorters)) * 100
    # print(str(len(blocks)))
    print(str(len(blocks)) + " blocks required for "
          + str(numTx) + " transaction(s) when " + str(porter_percentage) + "% of accounts are zkPorters.")

    # Known variables for real-world transfers
    # blocks_per_sec = float(1/13)
    # gas_limit_per_block = float(12500000)
    # trans_per_gas_unit = float(1/1184)
    amortized_blocks_per_sec = float(9.52)

    # get average number of transfers per block
    num_transfers = 0
    for b in range(len(blocks)):
        for transfer in blocks[b].transactions:
            num_transfers = num_transfers + 1
    avg_num_transfers_per_block = num_transfers / len(blocks)
    avg_num_porter_txs = num_porter_txs / len(blocks)

    tps = (avg_num_transfers_per_block + avg_num_porter_txs) * amortized_blocks_per_sec
    # print(str(np.round(tps, 2)))
    print(str(np.round(tps, 2)) + " transactions per second when " + str(porter_percentage)
          + "% of accounts are zkPorters.")

    return [len(blocks), np.round(tps, 2), porter_percentage]


if __name__ == "__main__":
    
    # user inputs
    args = sys.argv[1:]
    if len(args) == 0:
        TOT_NUM_ACCOUNTS = 10000
        NUM_TXS = 5000
    elif len(args) == 1:
        TOT_NUM_ACCOUNTS = int(args[0])
        NUM_TXS = 5000
    else:
        TOT_NUM_ACCOUNTS = int(args[0])
        NUM_TXS = int(args[1])

    # initialize the network proportions of each account type
    NUM_PORTERS = [int(TOT_NUM_ACCOUNTS * 0), int(TOT_NUM_ACCOUNTS * .10), int(TOT_NUM_ACCOUNTS * .20),
                   int(TOT_NUM_ACCOUNTS * .3000), int(TOT_NUM_ACCOUNTS * .40), int(TOT_NUM_ACCOUNTS * .50),
                   int(TOT_NUM_ACCOUNTS * .60), int(TOT_NUM_ACCOUNTS * .70), int(TOT_NUM_ACCOUNTS * .80),
                   int(TOT_NUM_ACCOUNTS * .90), int(TOT_NUM_ACCOUNTS * .95), int(TOT_NUM_ACCOUNTS * .98),
                   int(TOT_NUM_ACCOUNTS * .999)]
    NUM_ROLLUPS = [int(TOT_NUM_ACCOUNTS), int(TOT_NUM_ACCOUNTS * .90), int(TOT_NUM_ACCOUNTS * .80),
                   int(TOT_NUM_ACCOUNTS * .70), int(TOT_NUM_ACCOUNTS * .60), int(TOT_NUM_ACCOUNTS * .50),
                   int(TOT_NUM_ACCOUNTS * .40), int(TOT_NUM_ACCOUNTS * .30), int(TOT_NUM_ACCOUNTS * .20),
                   int(TOT_NUM_ACCOUNTS * .10), int(TOT_NUM_ACCOUNTS * .05), int(TOT_NUM_ACCOUNTS * .02),
                   int(TOT_NUM_ACCOUNTS * .001)]

    # simulate just roll up scenarios
    sim_data = []
    for i in range(len(NUM_ROLLUPS)):
        sim_data.append(simulateRollup(NUM_PORTERS[i], NUM_ROLLUPS[i], NUM_TXS))

    # display data from simulations
    acct_percentages = []
    num_blocks_needed = []
    txs_per_second = []
    for d in range(len(sim_data)):
        num_blocks_needed.append(sim_data[d][0])
        txs_per_second.append(sim_data[d][1] / 1000)
        acct_percentages.append(sim_data[d][2])


    # first plot
    plt.plot(acct_percentages, num_blocks_needed)
    plt.title('Number of Blocks Needed vs. % Network ZK-Porter Accounts')
    plt.xlabel('% of Network ZK-Porter Accounts')
    plt.ylabel('Number of Blocks needed to post' + str(NUM_TXS) + ' transactions')
    plt.grid()
    plt.show()

    # second plot
    plt.plot(acct_percentages, txs_per_second)
    plt.title('Transactions per Second vs. % Network ZK-Porter Accounts')
    plt.xlabel('% of Network ZK-Porter Accounts')
    plt.ylabel('Transactions per second (thousands)')
    plt.grid()
    plt.show()
