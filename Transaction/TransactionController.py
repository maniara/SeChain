from Controller import MainController
from CryptoController import dataEncode
from CryptoController import dataDecode
import json
import Transaction

#LIst Transaction
@staticmethod
def print_all_transaction():
    listtran = read_all_transactions()
    for list in listtran:
        load_list = json.loads(list)    #Transaction.dic
        data = dataDecode(load_list['value'], load_list['publickey'])
        value = json.loads(data)
        print "TimeStamp : " + load_list['timestamp'] + " SenderPubKey : " + load_list['publickey']
        print "SenderIP : " + value['senderip'] + " ReceiveIP : " + value['reveiverip'] + " Amount : " + value['amount'] + " Msg : " + value['msg']

#return Transaction(json)
#recv = recv.publickey
@staticmethod
def create_transaction(mynode,recv,amount,msg):
    t = Transaction(mynode.publickey,recv,amount,msg)
    t.dic['value'] = dataEncode(t.dic['value'], mynode.privatekey)
    data = json.dumps(t.dic)
    return data