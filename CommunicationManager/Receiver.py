def start(thread_name, ip_address):
    import json, sys
    from socket import *
    from StorageManager import FileController
    from NodeManager import NodeController

    port = 2001
    addr = (ip_address, port)
    buf_size = 8000
    sync_flag = False

    tcp_socket = socket(AF_INET, SOCK_STREAM)
    tcp_socket.bind(addr)
    tcp_socket.listen(5)
    print "Receiver is started"

    while True:
        receive_socket, sender_ip = tcp_socket.accept()

        while True:
            data = receive_socket.recv(buf_size)
            sync_flag = False
            try:
                data_entity = json.loads(data)

                if data_entity['type'] == 'T':
                    print "\nTransaction received from ", sender_ip
                    print ">"

                    FileController.add_transaction(data)
                    break

                elif data_entity['type'] == 'N':
                    from NodeManager import NodeController
                    from StorageManager import FileController

                    node_list = FileController.get_ip_list()

                    for outer_list in node_list:
                        outer_list = str(outer_list)
                        if outer_list in data:
                            sync_flag = True

                    if sync_flag is False:
                        NodeController.add_new_node(data)

                    print "New node is connected"

                    break

                elif data_entity['type'] == 'B':
                    print "Block received"

                    from BlockManager import BlockVerifyer
                    FileController.create_new_block(data_entity['block_id'], data)

                    if BlockVerifyer.verify(data_entity) is True:
                        FileController.remove_all_transactions()
                        FileController.create_new_block(data_entity['block_id'], data)
                    break

            except:
                print sys.exc_info()
                break

    tcp_socket.close()
    receive_socket.close()
    print "socket closed."