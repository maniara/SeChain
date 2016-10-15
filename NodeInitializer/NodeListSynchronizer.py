from SeChainController import Property
from NodeManager import NodeController
from CommunicationManager import Sender
from StorageManager import FileController
import json, sys, traceback
from socket import *


#sending node list in trust node is implemented in Receiver.py
def download_node_list(my_node):
    import thread

    thread.start_new_thread(receive_node_list, ("Node List Receiver", 1))
    request_node_list()

def request_node_list():
    trust_node_ip = Property.trust_node_ip
    json_node, new_json_nodes = NodeController.get_node()
    json_nodes = {
        'type': 'RN',
        'ip_address': json_node['ip_address']
    }
    new_json_node = json.dumps(json_nodes)
    Sender.send(trust_node_ip, new_json_node, Property.port)


def receive_node_list(*args):
    addr = (Property.my_ip_address, Property.port)
    buf_size = 10000

    tcp_socket = socket(AF_INET, SOCK_STREAM)
    tcp_socket.bind(addr)
    tcp_socket.listen(5)
    print "Node List Receiver is started(" + str(Property.my_ip_address) + ":" + str(Property.port) + ")"

    while True:
        receive_socket, sender_ip = tcp_socket.accept()

        # data : request sync node  ip address
        while True:
            data = receive_socket.recv(buf_size)
            try:
                if data == "":
                    break
                data_entity = json.loads(data)
                print "Receiving " + data_entity['type']

                if data_entity['type'] == 'QN':
                    print 'Node list sync complete'
                    Property.node_sync = True
                    break

                elif data_entity['type'] == 'N':
                    NodeController.add_new_node(json.loads(data_entity['message']))
            except :
                traceback.print_exc()
                break

        if(Property.node_sync == True) :
            tcp_socket.close()
            receive_socket.close()
            break