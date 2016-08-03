# Request and waiting IP information
def request_node_info(thread_name, request_ip):
    from socket import *
    from NodeManager import NodeController
    from StorageManager import FileController

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

            try:
                node_list = FileController.get_ip_list()

                for check_list in node_list:
                    check_list = str(check_list)
                    print check_list
                    if check_list not in data:
                        print "Syncronize Node"
                        NodeController.add_new_node(data)
                    else:
                        print "Already Sync"

                break
            except:
                print ""
                break

    tcp_socket.close()
    receive_socket.close()

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