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
    if FileController.get_number_of_transactions() >= 1:
        block = BlockGenerator.generate_block(trx_json)
        block_temp = json.dumps(block, indent=4, default=lambda o: o.__dict__, sort_keys=True)
        print "Sent block :" + block.block_id
        Sender.send_to_all_node(block_temp)

        FileController.remove_all_transactions()
        FileController.create_new_block(block.block_id, block_temp)

    else:
        Sender.send_to_all_node(trx_json)
        FileController.add_transaction(trx_json)