def send(ip_address, message):
    from socket import *
    port = 2001
    buf_size = 4000
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
        send(addr, message)


# Database Syncronization
def send_sync(ip_address, message):
    from socket import *

    port = 50007
    receiver_addr = (ip_address, port)
    tcp_socket =socket(AF_INET, SOCK_STREAM)
    connected = tcp_socket.connect(receiver_addr)

    if connected is False :
        print "Connection failed to "+ip_address

    else :
        if tcp_socket.send(message) is False:
            print "Send fail to "+ip_address

    tcp_socket.close()
