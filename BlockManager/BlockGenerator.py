def check_status():
    return False

def generate_block(last_transaction):
    from BlockManager import Block
    from StorageManager import FileController
    from SmartContracts import ContractRunner
    from BlockVerifyer import  transaction_verify
    import hashlib
    import json

    transactions = FileController.get_transaction_list()
    transactions.append(last_transaction + "\n")

    contract_states =  transaction_verify(transactions)

    # last block -> hash
    last_block_id, last_block = FileController.get_last_block()
    last_block_hash = hashlib.sha256(last_block).hexdigest()
    block = Block.Block(last_block_id, last_block_hash, transactions,contract_states)
    block_temp = json.dumps(block, indent=4, default=lambda o: o.__dict__, sort_keys=True)
    FileController.save_my_block(block_temp)
    return block
