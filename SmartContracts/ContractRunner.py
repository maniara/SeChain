import pickle
import hashlib
import importlib
import sources.Example
CONTRACT_ADDR = "./contracts/"
SOURCE_ADDR = "sources."

def route(transaction):

    if not isinstance(transaction, dict)
        return {'err' : 'transaction is wrong , transaction must dict'}

    if 'source' in transaction:
        try:
            return makeContract(transaction)
        except Exception as e:
            return {'err ' : 'make contract err '+ e}

    elif 'contract' in transaction:
        try:
            return run(transaction)
        except Exception as e:
            return {'err ' : 'run contract err '+ e}

    else :
        return {'err' : 'transaction is wrong, transction have not attribute for contract '}

def makeContract(transaction):
    contract  = getattr(importlib.import_module(SOURCE_ADDR+transaction['source']),'Contract')()
    contractAddr = hashlib.sha256(str(transaction) +'contract').hexdigest()
    print(contractAddr)
    fContract = open(CONTRACT_ADDR +contractAddr,'wb')
    pickle.dump(contract,fContract)
    fContract.close()
    fContract = open(CONTRACT_ADDR +contractAddr,'rb')
    state = fContract.read()
    fContract.close()

    return {'contractAddr' :  contractAddr ,'state' : state}

def run(transaction):
    contractAddress = CONTRACT_ADDR+transaction['contract']
    fContract = open(contractAddress,'rb')
    contract = pickle.load(fContract)
    method = getattr(contract,transaction['function'])
    result = method(transaction['args'])
    fContract.close()
    fContract = open(contractAddress,'wb')

    pickle.dump(contract,fContract)
    fContract.close()
    fContract = open(contractAddress,'rb')
    state = fContract.read()
    fContract.close()
    return {'result' : result,'state' : state}


#examples
#print(route({'source' : 'aaa','args' : ''}))
#print(route({'contract' : '677df83e6f1040bd6e85b29593aeb3795d33d31e6eddc09dd8bb14183e7fd190','function' : 'add','args' : 'aaa'}))
#print(route({}))
#print(route('aaa'))
