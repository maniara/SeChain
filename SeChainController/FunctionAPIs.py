from CommunicationManager import Sender
from TransactionManager import TransactionController
from StorageManager import FileController
from BlockManager import BlockGenerator
from SmartContractManager import ContractManager
import Property
import json

def send_transaction(receiver_ip, amount, message):
    trx_json = TransactionController.create_transaction(Property.myNode['public_key'],
                                                        Property.myNode['private_key'], 't',
                                                        receiver_ip, amount, message, '')

    #Check block generating condition
    if FileController.get_number_of_transactions() >= Property.max_transaction:
        block = BlockGenerator.generate_block(trx_json)
        block_temp = json.dumps(block, indent=4, default=lambda o: o.__dict__, sort_keys=True)
        print "Sending block (" + block.block_id+") to others"
        Sender.send_to_all_node(block_temp)

        FileController.remove_all_transactions()
        FileController.create_new_block(block.block_id, block_temp)

    else:
        print "Sending transaction to others"
        Sender.send_to_all_node(trx_json)
        FileController.add_transaction(trx_json)

def deply_contract(public_key, private_key, type,target_ip, amount, msg,contract_source):
    trx_json = TransactionController.create_transaction(public_key,
                                                        private_key, type,
                                                        target_ip, amount, msg, contract_source)

    if FileController.get_number_of_transactions() >= Property.max_transaction:
        block = BlockGenerator.generate_block(trx_json)
        block_temp = json.dumps(block, indent=4, default=lambda o: o.__dict__, sort_keys=True)
        print "Sending block (" + block.block_id + ") to others"
        Sender.send_to_all_node(block_temp)
    else:
        print "Sending transaction to others"
        Sender.send_to_all_node(trx_json)
        FileController.add_transaction(trx_json)

def run_contract(public_key, private_key, type,target_ip, amount, msg,contract_data):
    trx_json = TransactionController.create_transaction(public_key,
                                                        private_key, type,
                                                        target_ip, amount, msg, contract_data)
    if FileController.get_number_of_transactions() >= Property.max_transaction:
        block = BlockGenerator.generate_block(trx_json)
        block_temp = json.dumps(block, indent=4, default=lambda o: o.__dict__, sort_keys=True)
        Sender.send_to_all_node(block_temp)
    else:
        Sender.send_to_all_node(trx_json)