from Controller import MainController
import CryptoController
import Transaction

#LIst Transaction
@staticmethod
def print_all_transaction():
    listtran = read_all_transactions()
    for list in listtran:
        load_list = json.loads(list)
        data = dataDecode(load_list.value, load_list.publickey)
        value = json.load(data)
        print "TimeStamp : " + load_list['timestamp'] + " SenderPubKey : " + load_list['publickey']
        print "SenderIP : " + value['senderip'] + " ReceiveIP : " + value['reveiverip'] + " Amount : " + value['amount'] + " Msg : " + value['msg']

#return Transaction(json)
#recv = recv.publickey
@staticmethod
def create_transaction(mynode,recv,amount,msg):
    t = Transaction(mynode.publickey,recv,amount,msg)
    t.value = dataEncode(msg, mynode.privatekey)
    return json.dumps(t)