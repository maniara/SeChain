import json
from SmartContracts import ContractRunner
from StorageManager import FileController
def verify(block_string):
    transactions = block_string['transactions']
    a_id =  json.loads(FileController.get_my_block())['block_id']
    b_id = block_string['block_id']
    if a_id != b_id :
        contract_states = transaction_verify(transactions)
    #TODO varifty
    '''for k,v in contract_states :
        if block['contract_states'][k] != v:
            return False
    '''
    return True

def transaction_verify(transactions):
    contract_states = {}

    for transaction in transactions:
        transaction = json.loads(transaction)

        if transaction['type'] == 'ct':
            args = transaction['contract_datas']['args'].split()

            result = ContractRunner.makeContract(transaction['time_stamp'], transaction['contract_datas']['source'],
                                                 args)

            contract_states[result['contractAddr']] = result['state']


        if transaction['type'] == 'rt':
            args = transaction['contract_datas']['args'].split()

            result = ContractRunner.run(transaction['contract_datas']['contractAddr'],
                                        transaction['contract_datas']['function'], args)

            contract_states[transaction['contract_datas']['contractAddr']] = result['state']


    return contract_states