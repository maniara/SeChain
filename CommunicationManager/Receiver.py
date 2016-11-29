from socket import *
import traceback


def start(thread_name, ip_address, port):
    import json
    import time
    import sys
    from StorageManager import FileController
    from SeChainController import Property
    from StorageManager import utxoDB

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
            sync_flag = False
            try:
                if data == "":
                    break
                data_entity = json.loads(data)
                print "Receiving " + data
                print "Receiving " + data_entity['type']

                if data_entity['type'] == 't' or data_entity['type'] == 'ct' or  data_entity['type'] == 'rt':
                    print "\nTransaction received from ", sender_ip


                    '''
                        update UTXO db
                    '''


                    FileController.add_transaction(data)
                    break

                # When new node is added
                elif data_entity['type'] == 'N':
                    from NodeManager import NodeController
                    from StorageManager import FileController

                    node_list = FileController.get_ip_list()
                    received_ip = data_entity['ip_address']

                    for outer_list in node_list:
                        outer_list = str(outer_list)
                        if outer_list == received_ip:
                            sync_flag = True

                    if sync_flag is False:
                        NodeController.add_new_node(data_entity)

                    print "New node is connected"

                    break

                #When new block is received
                elif data_entity['type'] == 'B':
                    from SmartContractManager import ContractManager

                    from BlockManager import BlockVerifier

                    received_time = time.strftime('%Y%m%d%H%M%S', time.gmtime())
                    block_size = sys.getsizeof(data_entity)
                    print "Block received: "," ", received_time
                    print "size :",  block_size


                    if BlockVerifier.verify(data_entity) is True:
                        FileController.remove_all_transactions()
                        FileController.create_new_block(data_entity['block_id'], data)
                        # Processing smart contract
                        ContractManager.process_contract(data_entity['transactions'])

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
                            "type": "Q",
                            "ip_address": data_entity['ip_address']
                        }
                        json_dump = json.dumps(json_data)
                        print 'Sending block sync complete message to ' + data_entity['ip_address']
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
                                    f.close()
                                    datas = json.dumps(write_file)
                                    print 'Sending block to ' + data_entity['ip_address']
                                    Sender.send(data_entity['ip_address'], datas, port)

                        fin_message = {
                            'type': 'Q',
                            'ip_address': data_entity['ip_address']
                        }

                        fin_json_message = json.dumps(fin_message)
                        print 'Sending block sync complete message to ' + data_entity['ip_address']
                        Sender.send(data_entity['ip_address'], fin_json_message, port)
                        break

                elif data_entity['type'] == 'RN':
                    node_list = FileController.get_node_list()
                    for n in node_list:
                        json_data = {
                            'type': 'N',
                            'message' : n
                        }
                        json_dump = json.dumps(json_data)
                        print 'Sending node information to ' + data_entity['ip_address']
                        Sender.send(data_entity['ip_address'], json_dump, port)

                    fin_data = {
                        'type': 'QN',
                    }
                    fin_dump = json.dumps(fin_data)
                    print 'Sending node info sync complete message to ' + data_entity['ip_address']
                    Sender.send(data_entity['ip_address'], fin_dump, port)
                    break

            except:
                traceback.print_exc()
                break

    tcp_socket.close()
    receive_socket.close()
    print "socket closed."
