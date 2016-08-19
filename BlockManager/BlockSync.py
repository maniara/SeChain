def block_check(thread_name,ip_address):
    from CommunicationManager import Sender
    import json, sys
    from socket import *
    from StorageManager import FileController

    port = 10654
    addr = (ip_address, port)
    buf_size = 10000

    tcp_socket = socket(AF_INET, SOCK_STREAM)
    tcp_socket.bind(addr)
    tcp_socket.listen(5)
    print "Block Receiver is started"

    while True:
        receive_socket, sender_ip = tcp_socket.accept()
        while True:
            data = receive_socket.recv(buf_size)
            sync_flag = False
            try:
                data_entity = json.loads(data)

                if data_entity['type'] == 'C':
                    from StorageManager import FileController
                    from CommunicationManager import Sender
                    last_file = FileController.get_last_file()
                    print 'my_last_file = ' + last_file
                    print 'last_file = ' + data_entity['last_file']
                    if last_file == data_entity['last_file']:  # block sync
                        json_data = {
                            'type': 'Q',
                            'ip_address': data_entity['ip_address']
                        }
                        json_dump = json.dumps(json_data)
                        Sender.send(data_entity['ip_address'], json_dump,10654)

                    else:  # block non sync
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
                                    print 'file_name : ' + file
                                    print 'message : ' + mess
                                    f.close()
                                    datas = json.dumps(write_file)
                                    Sender.send(data_entity['ip_address'], datas,10654)
                        break

                elif data_entity['type'] == 'Q':
                    print 'Block Sync Complete'
                    break

                elif data_entity['type'] == 'W':
                    try:
                        FileController.write(FileController.block_storage_path + data_entity['file_name'], data_entity['message'])
                    except:
                        print "write error"
                        break
            except:
                break