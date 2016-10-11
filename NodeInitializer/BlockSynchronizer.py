from SeChainController import NodeInformation
from CommunicationManager import Sender

#check whether this node has last block
def request_block_sync():
    from NodeManager import NodeController
    from StorageManager import FileController
    import json
    import socket

    trust_node_ip = NodeInformation.trust_node_ip
    json_node, new_json_nodes = NodeController.get_node()
    last_file = FileController.get_last_file()
    json_nodes = {
        'type': 'C',
        'last_file' : last_file,
        'ip_address': json_node['ip_address']
    }
    new_json_node = json.dumps(json_nodes)
    Sender.send(trust_node_ip, new_json_node, NodeInformation.port)

def sync_blocks():
    import thread
    thread.start_new_thread(receive_block_for_sync, ("BlockSyncReceiver", 1))
    request_block_sync()

def receive_block_for_sync(*args):
    from CommunicationManager import Sender
    import json, sys
    from socket import *
    from StorageManager import FileController

    #processing response
    addr = (NodeInformation.my_ip_address, NodeInformation.port)
    buf_size = 10000

    tcp_socket = socket(AF_INET, SOCK_STREAM)
    tcp_socket.bind(addr)
    tcp_socket.listen(5)
    print "Block Receiver is started"

    while True:
        receive_socket, sender_ip = tcp_socket.accept()
        while True:
            data = receive_socket.recv(buf_size)
            if not data == "":
                print "Receiving "+data
            sync_flag = False
            try:
                data_entity = json.loads(data)

                #if sync is finished
                if data_entity['type'] == 'Q':
                    print 'Block Sync Complete'
                    NodeInformation.block_sync = True
                    break

                # if sync is not finished, receive block
                elif data_entity['type'] == 'W':
                    try:
                        FileController.write(FileController.block_storage_path + data_entity['file_name'], data_entity['message'])
                    except:
                        print "write error"
                        break
            except:
                break

        if(NodeInformation.block_sync == True) :
            receive_socket.close()
            tcp_socket.close()
            break