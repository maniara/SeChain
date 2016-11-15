from SeChainController import Property
class Transaction(object):
    def __init__(self, send, receiver, amount, msg, tx_type, contract_data):
        from ValueData import ValueData
        import json
        import time
        import socket
        self.type = tx_type
        self.time_stamp = time.strftime('%Y%m%d%H%M%S', time.localtime())
        self.ip_address = Property.my_ip_address # should not send ip address
        self.sender_public_key = send
        self.data = ValueData(self.ip_address, receiver, amount, msg)
        self.message = json.dumps(self.data, default=lambda o: o.__dict__)
        self.contract_data = contract_data
