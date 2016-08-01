def start(thread_name, ip_address):
    import json
    from socket import *
    from StorageManager import FileController
    port = 2001
    addr = (ip_address,port)
    buf_size = 4000

    tcp_socket = socket(AF_INET, SOCK_STREAM)
    tcp_socket.bind(addr)
    tcp_socket.listen(5)
    print "Receiver is started"

    while True:
        receive_socket, sender_ip = tcp_socket.accept()
        print "\nTransaction received from ", sender_ip
        print ">"

        while True:
            data = receive_socket.recv(buf_size)
            data_entity = json.loads(data)
            print data_entity
            if data_entity['type'] == 'T':
                FileController.add_transaction(data)
                break
            elif data_entity['type'] == 'N':
                from NodeManager import NodeController
                NodeController.add_new_node(data_entity)
                break
            elif data_entity['type'] == 'B':
                from BlockManager import BlockVerifyer
                BlockVerifyer.verify(data_entity)
                #add ledger
                break

    tcp_socket.close()
    receive_socket.close()