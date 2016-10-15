from SeChainController import Property
from socket import *
from SeChainController import Property

def send(ip_address, message, port):

    if(ip_address != Property.my_ip_address):
        #print "Sending "+ message + " to "+ip_address+":"+str(port)
        buf_size = 10000
        receiver_addr = (ip_address, port)
        tcp_socket =socket(AF_INET, SOCK_STREAM)
        connected = tcp_socket.connect(receiver_addr)
        if connected is False :
            print "Connection failed to "+ip_address

        else :
            if tcp_socket.send(message) is False:
                print "Send fail to "+ip_address

        tcp_socket.close()


def send_to_all_node(message):
    from StorageManager import FileController

    address_list = FileController.get_ip_list()

    for addr in address_list:
        if addr != Property.my_ip_address:
            try:
                send(addr, message, Property.port)
            except:
                continue
