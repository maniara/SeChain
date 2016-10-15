myNode = None #node entity
my_node_json = None   #node entity written in json
nodeList = None   #all peer(node) list of se-chain
trust_node_ip = "163.239.27.32"
my_ip_address = None
node_sync = False
block_sync = False
port = 10654
ui_frame = None
node_started = False
max_transaction = 0

# type direction
# C: request last block
# Q: your last block is correct
# W: block for sync
# B: new block
# T: transaction
# RN : Request Node List
