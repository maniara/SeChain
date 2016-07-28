from ValueData import ValueData
import time

#json
class Transaction:
    def __init__(self,send,recv,amount,msg):
        self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime())
        self.senderpublickey = send
        ip_address = socket.gethostbyname(socket.gethostname())
        data = ValueData(ip_address,recv,amount,msg)
        self.value = data.get_valuedata()