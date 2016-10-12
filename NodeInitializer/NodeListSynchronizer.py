from SeChainController import NodeInformation
from NodeManager import NodeController
from CommunicationManager import Sender
from StorageManager import FileController
import json, sys
from socket import *


#sending node list in trust node is implemented in Receiver.py
def download_node_list(my_node):
    import thread

    thread.start_new_thread(receive_node_list, ("Node List Receiver", 1))
    request_node_list()

def request_node_list():
    trust_node_ip = NodeInformation.trust_node_ip
    json_node, new_json_nodes = NodeController.get_node()
    json_nodes = {
        'type': 'RN',
        'ip_address': json_node['ip_address']
    }

    new_json_node = json.dumps(json_nodes)
    Sender.send(trust_node_ip, new_json_node, NodeInformation.port)


def receive_node_list(*args):
    addr = (NodeInformation.my_ip_address, NodeInformation.port)
    buf_size = 10000

    tcp_socket = socket(AF_INET, SOCK_STREAM)
    tcp_socket.bind(addr)
    tcp_socket.listen(5)
    print "Node List Receiver is started(" + str(NodeInformation.my_ip_address) + ":" + str(NodeInformation.port)+")"

    while True:
        receive_socket, sender_ip = tcp_socket.accept()

        # data : request sync node  ip address
        while True:
            data = receive_socket.recv(buf_size)
            if not data == "":
                print "Receiving "+data
            try:
                data_entity = json.load(data)
                if data_entity['type'] == 'QN':
                    print 'Node list sync complete'
                    NodeInformation.node_sync = True
                    break

                elif data_entity['type'] == 'N':
                    NodeController.add_new_node(data_entity)
            except :
                print sys.exc_info()
                break

        if(NodeInformation.node_sync == True) :
            tcp_socket.close()
            receive_socket.close()
            break