def start(thread_name, ip_address):
    import json, sys
    from socket import *
    from StorageManager import FileController

    port = 2001
    addr = (ip_address, port)
    buf_size = 8000

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

                elif data_entity['type'] == 'C':
                    from StorageManager import FileController
                    import Sender
                    last_file = FileController.get_last_file()
                    print 'my_last_file = ' + last_file
                    print 'last_file = ' + data_entity['last_file']
                    if last_file == data_entity['last_file']: #block sync
                        json_data = {
                            'type' : 'Q',
                            'is_disabled': False,
                            'public_key': data_entity['public_key'],
                            'private_key': data_entity['private_key'],
                            'ip_address': data_entity['ip_address']
                        }
                        json_dump = json.dumps(json_data)
                        Sender.send(data_entity['ip_address'],json_dump)

                    else: #block non sync
                        import os
                        block_storage_path = os.path.dirname(os.path.dirname(__file__)) + '\BlockStorage' + '\\'
                        for root, dirs, files in os.walk(block_storage_path):
                            for file in files:
                                if file <= data_entity['last_file']:
                                    continue
                                # send block
                                else:
                                    f = open(block_storage_path + file, 'r')
                                    mess = f.read()
                                    json_data = {
                                        'type' : 'W',
                                        'file_name' : file,
                                        'message' : '11'
                                    }
                                    print 'file_name : ' + file
                                    print 'message : ' + mess
                                    f.close()
                                    datas = json.dumps(json_data)
                                    Sender.send(data_entity['ip_address'],datas)


                elif data_entity['type'] == 'Q':
                    print 'Block Sync Complete'

                elif data_entity['type'] == 'W':
                    from StorageManager import FileController
                    print data_entity['file_name'] + ' ' + data_entity['message']
                    block_storage_path = os.path.dirname(os.path.dirname(__file__)) + '\BlockStorage' + '\\'
                    FileController.write(block_storage_path + data_entity['file_name'], data_entity['message'])


            except:
                print sys.exc_info()
                break

    tcp_socket.close()
    receive_socket.close()
    print "socket closed."