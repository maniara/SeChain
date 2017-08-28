import codecs
import datetime
import json

from dateutil import parser
from sqlalchemy import Column, String, Integer, DateTime

import db
import key
import transaction
from p2p import Sender


class Transaction(db.Base):
    __tablename__ = 'transactions'

    _id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String)
    time_stamp = Column(DateTime)
    tx_id = Column(String)
    pub_key = Column(String)
    recv_addr = Column(String)
    message = Column(String)  # document hash
    signature = Column(String)

    def __init__(self):
        self.type = 'T'
        self.time_stamp = datetime.datetime.now()
        self.tx_id = self.type + self.time_stamp.strftime('%Y%m%d%H%M%S')
        self.pub_key = ''
        self.recv_addr = ''
        self.message = ''  # document hash
        self.signature = ''

    def from_json(self, dictionary):
        """Constructor"""
        for key in dictionary:
            setattr(self, key, dictionary[key])

        self.time_stamp = parser.parse(self.time_stamp)
        return self

    def to_json(self):
        return json.dumps({
            'type': self.type,
            'time_stamp': self.time_stamp.strftime('%Y%m%d%H%M%S'),
            'tx_id': self.tx_id,
            'pub_key': self.pub_key,
            'recv_addr': self.recv_addr,
            'message': self.message,
            'signature': self.signature
        })


def add_transaction(tx):
    db.insert(tx)


def get_transactions():
    return db.get_all(Transaction)


def count():
    return db.count(Transaction)


def remove_all():
    db.remove_all(Transaction)


def create_tx(pub_key, pri_key, recv_addr, msg):
    tx = Transaction()
    tx.recv_addr = recv_addr
    tx.message = msg

    pub_key_b = key.key_to_string(pub_key)
    tx.pub_key = codecs.encode(pub_key_b, 'hex_codec').decode('utf-8')

    msg = tx.time_stamp.strftime('%Y%m%d%H%M%S') + msg

    sig = key.get_signature(msg, pri_key)
    tx.signature = codecs.encode(sig, 'hex_codec').decode('utf-8')

    return tx


def send_tx(tx):
    Sender.send(tx.recv_addr, tx.to_json(), 3000)
    transaction.add_transaction(tx)
