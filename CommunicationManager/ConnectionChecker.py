import socket
from MainController import NodeInformation

# data sync thread port = 50007
# If node is on-line , return True
# If node is off-line, return False
def connection_check(ip_address):
    PORT = NodeInformation.port
    sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sck.connect((ip_address, PORT))
        sck.settimeout(1.0)
        # sck.shutdown(3)
        sck.close()
        return True
    except socket.error as e:
        print e
        return False
