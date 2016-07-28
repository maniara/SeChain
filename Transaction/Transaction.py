
class Transaction:
    def __init__(self,send,recv,amount,msg):
        from ValueData import ValueData
        import json
        import time
        import socket
        ip_address = socket.gethostbyname(socket.gethostname())
        data = ValueData(ip_address, recv, amount, msg)
        dumpdata = json.dumps(data.dic)
        self.dic  = {"timestamp" : time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime()), "senderpublickey" : send,  "value" :  dumpdata}
        # a = T.dic['value'].dic['senderip']