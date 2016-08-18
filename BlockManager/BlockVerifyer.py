import json
from SmartContracts import ContractRunner
def verify(block_string):
    block = json.loads(block_string)
    transactions = block['transactions']
    if transactions[-1] ==
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