def check_status():
    return False


def generate_block(last_transaction):
    from BlockManager import Block
    from StorageManager import FileController
    from SmartContracts import ContractRunner
    import hashlib
    import json

    transactions = FileController.get_transaction_list()
    transactions.append(last_transaction + "\n")

    contract_states = {}

    for transaction in transactions :
        transaction = json.loads(transaction)

        if transaction['type'] == 'ct':
            args = transaction['contract_datas']['args'].spilt()
            result = ContractRunner.makeContract(transaction['time_stamp'],transaction['contract_datas']['source'],args)
            contract_states[result['contractAddr']] = result['state']

        if transaction['type'] == 'rt':
            args = transaction['contract_datas']['args'].spilt()
            result = ContractRunner.run(transaction['contract_datas']['contractAddr'],transaction['contract_datas']['fucntion'],args)
            contract_states[transaction['contract_datas']['contractAddr']] = result['state']

    # last block -> hash
    last_block_id, last_block = FileController.get_last_block()
    last_block_hash = hashlib.sha256(last_block).hexdigest()
    block = Block.Block(last_block_id, last_block_hash, transactions,contract_states)

    return block
