import pickle
import hashlib
import importlib
import os
from SeChainController import Property

CONTRACT_ADDR = Property.CONTRACT_DEPLOY_PATH
SOURCE_ADDR = "SmartContractManager.Sources."

#LIMITATION
#No source code deploy implementation
#Need to exist sources all node
def makeContract(time_stamp,sourceName,args):
    contract  = getattr(importlib.import_module(SOURCE_ADDR+sourceName),'Contract')(*args)
    contractAddr = time_stamp
    fContract = open(CONTRACT_ADDR +"C"+contractAddr,'wb')
    print contractAddr
    #serialize and write
    pickle.dump(contract,fContract)
    fContract.close()
    fContract = open(CONTRACT_ADDR +"C"+contractAddr,'rb')
    state = fContract.read()
    fContract.close()
    print 'Contract (' + contractAddr ,+ ') deployied'
    return {'contractAddr' :  contractAddr ,'state' : state}

def run(contractAddr,functionName,args):

    #load states & run
    contractAddress = CONTRACT_ADDR+contractAddr
    fContract = open(contractAddress,'r')
    contract = pickle.load(fContract)
    print 'Contract loaded'
    method = getattr(contract, functionName)
    #run method
    result = method(*args)
    fContract.close()

    #save state
    fContract = open(contractAddress,'w')
    pickle.dump(contract,fContract)
    fContract.close()
    fContract = open(contractAddress,'r')
    state = fContract.read()
    fContract.close()
    print {'result' : result,'state' : state}
    return {'result' : result,'state' : state}

#makeContract('aaaaa','aaa',(1,2))
#print(run('aaaaa','add','20'))
