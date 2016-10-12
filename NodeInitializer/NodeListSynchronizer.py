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
    print "Node List Receiver is started"

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