import json
import ContractRunner

def process_contract(transactions):
    contract_states = {}
    for transaction in transactions:
        transaction = json.loads(transaction)
        #create contract in local
        if transaction['type'] == 'CT':
            #extract parameters
            args = transaction['contract_data']['args'].split()

            # (contract id, source_path, args)
            result = ContractRunner.makeContract(transaction['time_stamp'], transaction['contract_data']['source'],
                                                 args)
            # (contract id, source_path, args)
            # contract_states[result['contractAddr']] = result['state']

        #run contract
        if transaction['type'] == 'RT':
            args = transaction['contract_data']['args'].split()

            result = ContractRunner.run(transaction['contract_data']['contractAddr'],
                                        transaction['contract_data']['function'], args)

            contract_states[transaction['contract_data']['contractAddr']] = result['state']


    return contract_states