from typing import List
from Account import Account
import string
import hashlib
from merklelib import MerkleTree


def getStateRoot(accounts: List[Account]) -> str:
    tree = MerkleTree(accounts)
    return tree.merkle_root
