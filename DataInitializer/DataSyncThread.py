# Request and waiting IP information
def request_node_info(thread_name, request_ip):
    from socket import *
    from NodeManager import NodeController
    from StorageManager import FileController
    import sys
    port = 50007
    addr = (request_ip, port)
    buf_size = 4000

    tcp_socket = socket(AF_INET, SOCK_STREAM)
    tcp_socket.bind(addr)
    tcp_socket.listen(5)

    print "Sync Thread starting...(REQUEST)"
    while True:
        receive_socket, sender_ip = tcp_socket.accept()

        # data : request sync node  ip address
        while True:
            data = receive_socket.recv(buf_size)
            sync_flag = False
            try:
                node_list = FileController.get_ip_list()

                for outer_list in node_list:
                    outer_list = str(outer_list)
                    if outer_list in data:
                        sync_flag = True

                if sync_flag is False:
                    NodeController.add_new_node(data.replace("\n", ""))

                break
            except :
                print sys.exc_info()
                break

    tcp_socket.close()
    receive_socket.close()

    # block sync
    from NodeManager import NodeController

    ip_address = socket.gethostbyname(socket.gethostname())

    my_node,my_json_node = NodeController.get_node(ip_address)
    json_node = {
        'type': 'R',
        'is_disabled': False,
        'public_key': my_node['public_key'],
        'private_key': my_node['private_key'],
        'ip_address': my_node['ip_address']
    }
    # for nodes in node_list:
    #    from CommunicationManager import Sender
    #    import json
    #    data = json.dumps(json_node)
    #    Sender.send(nodes, data)

    from CommunicationManager import Sender
    import json
    data = json.dumps(json_node)
    Sender.send('163.239.27.32', data)

# Waiting Request, response the node Information
def response_node_info(thread_name, request_ip):
    from socket import *
    from StorageManager import FileController
    from CommunicationManager import Sender

    port = 50007
    addr = (request_ip, port)
    buf_size = 4000

    tcp_socket = socket(AF_INET, SOCK_STREAM)
    tcp_socket.bind(addr)
    tcp_socket.listen(5)

    print "Sync Thread starting...(RESPONSE)"

    while True:
        receive_socket, sender_ip = tcp_socket.accept()

        # data : request sync node  ip address
        while True:
            data = receive_socket.recv(buf_size)
            try:
                node_list = FileController.get_node_list()
                for iter in node_list:
                    Sender.send_sync(data, iter)
                break
            except:
                print "EXCEPT"
                break

    tcp_socket.close()
    receive_socket.close()