from CryptoController import dataEncode
from CryptoController import dataDecode
import json
import Transaction

def print_all_transaction():
    transaction_list = read_all_transactions()
    for tr in transaction_list:
        load_list = json.loads(tr)
        data = dataDecode(load_list['value'], load_list['publickey'])
        value = json.loads(data)
        print "TimeStamp : " + load_list['timestamp'] + " SenderPubKey : " + load_list['publickey']
        print "SenderIP : " + value['senderip'] + " ReceiveIP : " + value['reveiverip'] + " Amount : " + value['amount'] + " Msg : " + value['msg']


def create_transaction(public_key, target_ip, amount, msg):
    t = Transaction.Transaction(public_key, target_ip, amount, msg)
    t.dic['value'] = dataEncode(t.dic['value'], public_key)
    data = json.dumps(t.dic)
    return data
