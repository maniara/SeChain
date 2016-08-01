
class Transaction(object):
    def __init__(self, send, receiver, amount, msg):
        from ValueData import ValueData
        import json
        import time
        import socket
        self.type = 'T'
        self.time_stamp = time.strftime('%Y%m%d%H%M%S', time.localtime())
        self.sender_public_key = send
        ip_address = socket.gethostbyname(socket.gethostname())
        data = ValueData(ip_address, receiver, amount, msg)
        self.message = json.dumps(data, default=lambda o: o.__dict__)
