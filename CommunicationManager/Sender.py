from socket import *
from SeChainController import Property


def send(ip_address, message, port, *args):

    if ip_address != Property.my_ip_address:
        receiver_addr = (ip_address, port)
        tcp_socket = socket(AF_INET, SOCK_STREAM)

        try:
            tcp_socket.connect(receiver_addr)
            tcp_socket.send(message)
        except Exception as e:
            print "Connection Failed ", e

        tcp_socket.close()


'''
    closed
    param: message -> my ip address
    send my node information to node which is now running
'''


def send_to_all_node(message):

    address_list = Property.alive_nodes['alive']

    for addr in address_list:
        if addr != Property.my_ip_address:
            try:
                send(addr, message, Property.port, 1)
            except Exception as e:
                print e
        else:
            continue