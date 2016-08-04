def check_status():
    return False


def generate_block(last_transaction):
    from CommunicationManager import Sender
    from BlockManager import Block
    from StorageManager import FileController

    transactions = [] '''get all temporary transactions'''
    transactions.append(last_transaction)
    '''add last_transaction into transaction's array'''
    '''instance Block instance'''
    last_block_id, last_block = FileController.get_last_block()
    block = Block(last_block_id, '''hashcode of last_block''', transactions)
    return block

