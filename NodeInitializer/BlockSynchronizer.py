import json, sys, traceback
from socket import *
from SeChainController import Property
from CommunicationManager import Sender


#sending blocks in trust node is implemented in Receiver.py
def sync_blocks():
    import thread
    thread.start_new_thread(receive_block_for_sync, ("BlockSyncReceiver", 1))
    request_block_sync()


#check whether this node has last block
def request_block_sync():
    from NodeManager import NodeController
    from StorageManager import FileController
    import json

    trust_node_ip = Property.trust_node_ip
    json_node, new_json_nodes = NodeController.get_node()
    last_file = FileController.get_last_file()
    json_nodes = {
        'type': 'C',
        'last_file': last_file,
        'ip_address': json_node['ip_address']
    }
    new_json_node = json.dumps(json_nodes)
    Sender.send(trust_node_ip, new_json_node, Property.port)


def receive_block_for_sync(*args):
    from StorageManager import FileController


    #processing response
    addr = (Property.my_ip_address, Property.port)
    buf_size = 10000

    tcp_socket = socket(AF_INET, SOCK_STREAM)
    tcp_socket.bind(addr)
    tcp_socket.listen(5)

    while True:
        receive_socket, sender_ip = tcp_socket.accept()
        while True:
            data = receive_socket.recv(buf_size)
            sync_flag = False
            try:
                if data == "":
                    break

                data_entity = json.loads(data)
                print "Receiving " + data_entity['type']


                #if sync is finished
                if data_entity['type'] == 'Q':
                    print 'Block sync complete'
                    Property.block_sync = True
                    break

                # if sync is not finished, receive block
                elif data_entity['type'] == 'W':
                    FileController.write(FileController.block_storage_path + data_entity['file_name'], data_entity['message'])

            except:
                traceback.print_exc()
                break

        if Property.block_sync is True:
            receive_socket.close()
            tcp_socket.close()
            break