from MainController import NodeInformation

# Request and waiting IP information
def request_node_info(thread_name, request_ip):
    from socket import *
    from NodeManager import NodeController
    from StorageManager import FileController
    from DataInitializer import BlockSynchronizer
    import sys
    port = NodeInformation.port
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

# Waiting Request, response the node Information
def response_node_info(thread_name, request_ip):
    from socket import *
    from StorageManager import FileController
    from CommunicationManager import Sender

    port = NodeInformation.port
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
                    Sender.send(data, iter,NodeInformation.port)
                break
            except:
                print "EXCEPT"
                break

    tcp_socket.close()
    receive_socket.close()