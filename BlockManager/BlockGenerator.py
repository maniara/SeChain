def check_status():
    return False


def generate_block(last_transaction):
    from CommunicationManager import Sender
    from BlockManager import Block
    '''get all temporary transactions'''
    '''add last_transaction into transaction's array'''
    '''instance Block instance'''

    block = Block("hash", all_temporary_transaction_array)
    return block

