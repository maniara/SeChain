import os

myNode = None #node entity
my_node_json = None   #node entity written in json
nodeList = None   #all peer(node) list of se-chain
trust_node_ip = "163.239.27.32"
my_ip_address = None
node_sync = False
alive_nodes = dict() # key value ['alive'] is currently connected nodes
check_flag = False
block_sync = False
port = 10654
ui_frame = None
node_started = False
NODE_IDX = 0

max_transaction = 0
CONTRACT_DEPLOY_PATH = os.path.dirname(os.path.dirname(__file__)) + '\_ContractStorage'+ '\\'
DB_PATH = os.path.dirname(os.path.dirname(__file__)) + '\StorageManager'+ '\\'


# type direction
# C: request last block
# Q: your last block is correct
# W: block for sync
# B: new block
# T: transaction
# RN : Request Node List
