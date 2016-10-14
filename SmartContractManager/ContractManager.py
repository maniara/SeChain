def process_contract(block_string):
    transactions = block_string['transactions']

    contract_states = {}
    for transaction in transactions:
        transaction = json.loads(transaction)
        #create contract in local
        if transaction['type'] == 'ct':
            #extract parameters
            args = transaction['contract_datas']['args'].split()

            # (contract id, source_path, args)
            result = ContractRunner.makeContract(transaction['time_stamp'], transaction['contract_datas']['source'],
                                                 args)
            # (contract id, source_path, args)
            contract_states[result['contractAddr']] = result['state']

        #run contract
        if transaction['type'] == 'rt':
            args = transaction['contract_datas']['args'].split()

            result = ContractRunner.run(transaction['contract_datas']['contractAddr'],
                                        transaction['contract_datas']['function'], args)

            contract_states[transaction['contract_datas']['contractAddr']] = result['state']


    return contract_states