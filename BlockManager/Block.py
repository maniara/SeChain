
class Block(object):
    type = 'B'
    block_id = None
    time_stamp = None
    previous_block_id = None
    previous_block_hash = None
    transactions = []

    def __init__(self, previous_block_id, previous_block_hash, transactions, contract_states):
        import time
        self.type = 'B'
        self.previous_block_id = previous_block_id
        self.previous_block_hash = previous_block_hash
        self.transactions = transactions
        self.time_stamp = time.strftime('%Y%m%d%H%M%S', time.localtime())
        self.block_id = "B" + self.time_stamp
        self.contract_states = contract_states


