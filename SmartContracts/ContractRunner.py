import pickle
import hashlib
import importlib
import sources.Example
CONTRACT_ADDR = "./contracts/"
SOURCE_ADDR = "sources."

def makeContract(time_stamp,sourceName,args):

    contract  = getattr(importlib.import_module(SOURCE_ADDR+sourceName),'Contract')(args)
    contractAddr = hashlib.sha256(time_stamp).hexdigest()
    fContract = open(CONTRACT_ADDR +contractAddr,'wb')
    pickle.dump(contract,fContract)
    fContract.close()
    fContract = open(CONTRACT_ADDR +contractAddr,'rb')
    state = fContract.read()
    fContract.close()

    return {'contractAddr' :  contractAddr ,'state' : state}

def run(contractAddr,functionName,args):

    #load states & run
    contractAddress = CONTRACT_ADDR+contractAddr
    fContract = open(contractAddress,'rb')
    contract = pickle.load(fContract)
    method = getattr(contract,functionName)
    result = method(args)
    fContract.close()

    #save state
    fContract = open(contractAddress,'wb')
    pickle.dump(contract,fContract)
    fContract.close()
    fContract = open(contractAddress,'rb')
    state = fContract.read()
    fContract.close()

    return {'result' : result,'state' : state}
