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

def block_sync():
    from NodeManager import NodeController
    from MainController import MainController
    from NodeManager import JsonEncoder
    from StorageManager import FileController
    import json

    fetch_node_ip = '163.239.27.32'
    json_node, new_json_nodes = NodeController.get_node(MainController.get_ip_address())
    node = json.loads(json_node)
    last_file = FileController.get_last_file()
    json_nodes = {
        'type': 'C',
        'last_file' : last_file,
        'ip_address': node['ip_address']
    }
    new_json_node = json.dumps(json_nodes, cls=JsonEncoder.json_encoder)
    send(fetch_node_ip,new_json_node)