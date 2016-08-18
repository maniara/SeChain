import pickle
import hashlib
import importlib
import os
CONTRACT_ADDR = os.path.dirname(os.path.dirname(__file__)) + '\contracts'+ '\\'
SOURCE_ADDR = "sources."

def makeContract(time_stamp,sourceName,args):
    contract  = getattr(importlib.import_module(SOURCE_ADDR+sourceName),'Contract')(*args)
    contractAddr = time_stamp
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
    fContract = open(contractAddress,'r')
    contract = pickle.load(fContract)
    print 'pickle load'
    method = getattr(contract,functionName)
    result = method(*args)
    fContract.close()

    #save state
    fContract = open(contractAddress,'w')
    pickle.dump(contract,fContract)
    fContract.close()
    fContract = open(contractAddress,'r')
    state = fContract.read()
    fContract.close()

    return {'result' : result,'state' : state}

#makeContract('aaaaa','aaa',(1,2))
#print(run('aaaaa','add','20'))
