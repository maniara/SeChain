from CommunicationManager import Sender
import Property

def send_transaction(receiver_ip, amount, message):
    trx_json = TransactionController.create_transaction(Property.myNode['public_key'],
                                                        Property.myNode['private_key'], 't',
                                                        receiver_ip, amount, message, '')

    #Check block generating condition
    if FileController.get_number_of_transactions() >= 0:
        block = BlockGenerator.generate_block(trx_json)
        block_temp = json.dumps(block, indent=4, default=lambda o: o.__dict__, sort_keys=True)
        Sender.send_to_all_node(block_temp)
    else:
        Sender.send_to_all_node(trx_json)