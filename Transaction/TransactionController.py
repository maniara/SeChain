#-*- coding: utf-8 -*-
from CryptoController import dataEncode
from CryptoController import dataDecode
from Node import JsonEncoder
import json
import Transaction


def print_all_transaction():
    from DataStorage import FileController
    transaction_list = FileController.get_transaction_list()
    for tr in transaction_list:
        load_list = json.loads(tr)
        data = dataDecode(load_list['value'], load_list['senderpublickey'])
        value = json.loads(data)
        print "TimeStamp : " + load_list['timestamp'] + " SenderPubKey : " + load_list['senderpublickey']
        print "SenderIP : " + value['senderip'] + " ReceiveIP : " + value['reveiverip'] + " Amount : " + value['amount'] + " Msg : " + value['msg']


def create_transaction(public_key, private_key, target_ip, amount, msg):
    t = Transaction.Transaction(public_key, target_ip, amount, msg)
    t.dic['value'] = dataEncode(t.dic['value'], private_key)
    t.dic['value'] = unicode(t.dic['value'], errors = 'ignore')
    data = json.dumps(t.dic)
    return data
