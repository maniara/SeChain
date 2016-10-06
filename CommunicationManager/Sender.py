def send(ip_address, message, port):
    from socket import *
    print "Sending "+ message + " to "+ip_address
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
        try:
            send(addr, message, 2001)
        except:
            continue

#check whether this node has last block
def block_sync():
    from NodeManager import NodeController
    from StorageManager import FileController
    import NodeInformation
    import json
    import socket
    ip_address = socket.gethostbyname(socket.gethostname())
    trust_node_ip = NodeInformation.trust_node_ip
    json_node, new_json_nodes = NodeController.get_node(ip_address)
    last_file = FileController.get_last_file()
    json_nodes = {
        'type': 'C',
        'last_file' : last_file,
        'ip_address': json_node['ip_address']
    }
    new_json_node = json.dumps(json_nodes)
    send(trust_node_ip, new_json_node, 10654)
