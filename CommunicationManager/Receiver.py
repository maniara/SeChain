def start(thread_name, ip_address, port):
    import json, sys, time
    from socket import *
    from StorageManager import FileController
    from MainController import NodeInformation

    addr = (ip_address, port)
    buf_size = 10000

    tcp_socket = socket(AF_INET, SOCK_STREAM)
    tcp_socket.bind(addr)
    tcp_socket.listen(5)
    print "Receiver is started " + str(ip_address)+":"+str(port)

    while True:
        receive_socket, sender_ip = tcp_socket.accept()
        print sender_ip

        while True:
            data = receive_socket.recv(buf_size)
            if not data == "":
                print "Receiving " + data
            sync_flag = False
            try:
                data_entity = json.loads(data)
                if data_entity['type'] == 't' or data_entity['type'] == 'ct' or  data_entity['type'] == 'rt':
                    print "\nTransaction received from ", sender_ip
                    print ">"

                    FileController.add_transaction(data)
                    break

                # When new node is added
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

                #When new block is received
                elif data_entity['type'] == 'B':
                    print "Block received"
                    from BlockManager import BlockVerifyer

                    if BlockVerifyer.verify(data_entity) is True:
                        FileController.remove_all_transactions()
                        FileController.create_new_block(data_entity['block_id'], data)
                    break

                #When other node request sync block
                elif data_entity['type'] == 'C':
                    from StorageManager import FileController
                    from CommunicationManager import Sender
                    last_file = FileController.get_last_file()
                    #print 'my_last_file = ' + last_file
                    #print 'last_file = ' + data_entity['last_file']

                    #blocks are synchronized
                    if last_file == data_entity['last_file']:
                        json_data = {
                            'type': 'Q',
                            'ip_address': data_entity['ip_address']
                        }
                        json_dump = json.dumps(json_data)
                        Sender.send(data_entity['ip_address'], json_dump, port)

                    # blocks are not synchronized
                    else:
                        import os
                        for root, dirs, files in os.walk(FileController.block_storage_path):
                            for file in files:
                                if file <= data_entity['last_file']:
                                    continue
                                # send block
                                else:
                                    f = open(FileController.block_storage_path + file, 'r')
                                    mess = f.read()
                                    write_file = {
                                        'type': 'W',
                                        'file_name': file,
                                        'message': mess
                                    }
                                    print 'Sending block #' + file
                                    f.close()
                                    datas = json.dumps(write_file)
                                    Sender.send(data_entity['ip_address'], datas, port)

                                    time.sleep(3)


                        json_data = {
                            'type': 'Q',
                            'ip_address': data_entity['ip_address']
                        }
                        json_dump = json.dumps(json_data)
                        Sender.send(data_entity['ip_address'], json_dump, port)
                        break


            except:
                print "Except"
                break

    tcp_socket.close()
    receive_socket.close()
    print "socket closed."
