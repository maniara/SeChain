def check_status():
    return False


def generate_block(last_transaction):
    from BlockManager import Block
    from StorageManager import FileController
    import hashlib

    transactions = FileController.get_transaction_list()
    transactions.append(last_transaction + "\n")

    # last block -> hash
    last_block_id, last_block = FileController.get_last_block()
    last_block_hash = hashlib.sha256(last_block).hexdigest()
    block = Block.Block(last_block_id, last_block_hash, transactions)

    return block

