import json
from SmartContracts import ContractRunner
def verify(block_string):
    print '1'
    print '2'
    transactions = block_string['transactions']
    print '3'
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
        print 'transaction'
        print transaction
        transaction = json.loads(transaction)

        if transaction['type'] == 'ct':
            print 'befoe split ct'
            args = transaction['contract_datas']['args'].split()
            print 'befoe split rt'

            result = ContractRunner.makeContract(transaction['time_stamp'], transaction['contract_datas']['source'],
                                                 args)
            print 'befoe split rt'

            contract_states[result['contractAddr']] = result['state']
            print 'befoe split rt'


        if transaction['type'] == 'rt':
            print 'befoe split rt'
            args = transaction['contract_datas']['args'].split()
            print 'befoe split rt'

            result = ContractRunner.run(transaction['contract_datas']['contractAddr'],
                                        transaction['contract_datas']['function'], args)
            print 'befoe split rt'

            contract_states[transaction['contract_datas']['contractAddr']] = result['state']
            print 'befoe split rt'


    return contract_states