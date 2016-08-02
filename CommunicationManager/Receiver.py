def start(thread_name, ip_address):
    import json
    from socket import *
    from StorageManager import FileController
    from NodeManager import NodeController

    port = 2001
    addr = (ip_address, port)
    buf_size = 4000

    tcp_socket = socket(AF_INET, SOCK_STREAM)
    tcp_socket.bind(addr)
    tcp_socket.listen(5)
    print "Receiver is started"

    while True:
        receive_socket, sender_ip = tcp_socket.accept()

        while True:
            data = receive_socket.recv(buf_size)
            try:
                data_entity = json.loads(data)
                print "\nTransaction received from ", sender_ip
                print ">"

                if data_entity['type'] == 'T':
                    print data_entity
                    FileController.add_transaction(data)
                    break
                elif data_entity['type'] == 'N':
                    print "New node is connected"
                    from NodeManager import NodeController
                    NodeController.add_new_node(data)
                    break
                elif data_entity['type'] == 'B':
                    from BlockManager import BlockVerifyer
                    BlockVerifyer.verify(data_entity)
                    #add ledger
                    break
            except:
                NodeController.add_new_node(data)
                print "EXCEPTION"
                break

    tcp_socket.close()
    receive_socket.close()
    print "socket closed."