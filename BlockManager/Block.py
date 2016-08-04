class Block(object):
    type = 'B'
    block_id = None
    time_stamp = None
    previous_hash = None
    transactions = []

    def __init__(self, previous_hash, transactions):
        self.previous_hash = previous_hash;
        self.time_stamp = time.strftime('%Y%m%d%H%M%S', time.localtime())
        self.block_id = "B"+time_stamp
        self.transactions = transactions
