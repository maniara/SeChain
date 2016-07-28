
class ValueData:
    def __init__(self,send,recv,am,msg):
        self.dic = {"senderip" : send, "reveiverip" : recv, "amount" : am, "message" : msg}