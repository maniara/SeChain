import json

class ValueData:
    def __init__(self,send,recv,am,msg):
        self.senderip=send
        self.reveiverip=recv
        self.amount=am
        self.message=msg

    def get_valuedata(self):
        data = json.dumps(self)
        return data