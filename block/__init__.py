import datetime

import db

peer_number = 0
block_sync = True  # Need to Set FALSE after Test

from sqlalchemy import Column, String, Integer, DateTime
from block import peer_number


class Block(db.Base):
    __tablename__ = 'blocks'

    _id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String)
    prev_block_id = Column(String)
    prev_block_hash = Column(String)
    tx_list = Column(String)
    merkle_root = Column(String)
    time_stamp = Column(DateTime)
    block_id = Column(String)
    block_hash = Column(String)
    nonce = Column(String)
    block_info = Column(String)
    block_miner = Column(Integer)

    def __init__(self, prev_block_id, prev_block_hash, tx_list, merkle_root, nonce, block_info):
        self.type = 'B'
        self.prev_block_id = prev_block_id
        self.prev_block_hash = prev_block_hash
        self.tx_list = tx_list
        self.merkle_root = merkle_root
        self.time_stamp = datetime.datetime.now()
        self.block_id = self.type + self.time_stamp.strftime('%Y%m%d%H%M%S')
        self.block_hash = ''
        self.nonce = nonce
        self.block_info = block_info
        self.block_miner = 1


class GenesisBlock(object):
    def __init__(self):
        self.type = 'B'
        self.prev_block_id = 'B000000000000'
        self.prev_block_hash = 'block_hash'
        self.tx_list = 'sechain'
        self.timp_stamp = '0000-00-00-00-00-00'
        self.block_id = 'B000000000000'
        self.merkle_root = 'sogangfinotek2017'
        self.block_hash = 'sechainfinochain2017'
        self.nonce = 2010101010


def create_block(block):
    db.insert(block)


def get_my_block():
    return 0


def count():
    db.count(Block)


def get_all_block():
    return db.get_all(Block)


def get_last_block():
    return get_all_block()[-1]


if __name__ == '__main__':
    import json

    t = GenesisBlock()
    temp = json.dumps(t, indent=4, default=lambda o: o.__dict__, sort_keys=True)
    temps = json.loads(temp)
    print(type(temps['nonce']))
