from typing import List
from Account import Account
import string
import hashlib
from merklelib import MerkleTree


def getPorterStateRoot(porters: List[Account]) -> str:
    tree = MerkleTree(porters)
    return tree.merkle_root
