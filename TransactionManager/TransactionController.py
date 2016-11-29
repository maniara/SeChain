from CryptoController import data_encode
from CryptoController import data_decode
import json
import Transaction


def print_all_transaction():
    from StorageManager import FileController
    transaction_list = FileController.get_transaction_list()

    for tr in transaction_list:
        transaction_entity = json.loads(tr)
        transaction_entity['message'] = transaction_entity['message'].decode('string_escape')
        data = data_decode(transaction_entity['message'], transaction_entity['sender_public_key'])
        value = json.loads(data)
        print "TimeStamp : ", transaction_entity['time_stamp'], "SenderIP : ",  value['sender_ip'], " ReceiverIP : ", value['receiver_ip'], " Amount : ", value['amount'], " Msg : ", value['message']


def create_transaction(public_key, private_key, tx_type, target_ip, amount, msg, contract_source):
    t = Transaction.Transaction(public_key, target_ip, amount, msg, tx_type, contract_source)
    encoded_message = data_encode(t.message, private_key)
    t.message = encoded_message.encode('string_escape')
    data = json.dumps(t, default=lambda o: o.__dict__)
    return data

'''
    New
'''
def create_tx(public_key, receiver_address, coin, msg, contract_source):
    tx = Transaction.Transaction(public_key, receiver_address, coin, msg, 't', contract_source)
    '''
        need to add encryption with public key (ecdsa)
        and signature
    '''
    tx_json = json.dumps(tx, default=lambda o: o.__dict__)
    return tx_json


if __name__ == '__main__':
    tx = create_tx('pbk', 'recvaddr', 10, 'test', '')
    print tx