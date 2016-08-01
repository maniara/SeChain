from CryptoController import dataEncode
from CryptoController import dataDecode
import json
import Transaction


def print_all_transaction():
    from StorageManager import FileController
    transaction_list = FileController.get_transaction_list()

    for tr in transaction_list:
        transaction_entity = json.loads(tr)
        transaction_entity['message'] = transaction_entity['message'].decode('string_escape')
        data = dataDecode(transaction_entity['message'], transaction_entity['sender_public_key'])
        value = json.loads(data)
        print "TimeStamp : ", transaction_entity['time_stamp'], "SenderIP : ",  value['sender_ip'], " ReceiverIP : ", value['receiver_ip'], " Amount : ", value['amount'], " Msg : ", value['message']


def create_transaction(public_key, private_key, target_ip, amount, msg):
    t = Transaction.Transaction(public_key, target_ip, amount, msg)
    encoded_message = dataEncode(t.message, private_key)
    t.message = encoded_message.encode('string_escape')
    data = json.dumps(t, default=lambda o: o.__dict__)
    return data
