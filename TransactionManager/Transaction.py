from SeChainController import Property


class Transaction(object):
    '''
        sender_pubkey: sender's public key for signature and encryption
        value data - receiver :receiver's address
                   - amount : coin
    '''
    def __init__(self, sender_pubkey, receiver, amount, msg, tx_type, contract_data):
        from ValueData import ValueData
        from SeChainController import Property
        import json
        import time


        # from param
        self.type = tx_type
        self.sender_address = Property.myNode['address'] # receiver address
        self.data = ValueData(receiver, amount) # ValueData(recv addr, coin)
        self.value_data = json.dumps(self.data, default=lambda o: o.__dict__)
        self.contract_data = contract_data
        self.message = msg
        self.pubkey = sender_pubkey

        # self
        self.ip_address = Property.my_ip_address # should not send ip address
        self.time_stamp = time.strftime('%Y%m%d%H%M%S', time.localtime())
