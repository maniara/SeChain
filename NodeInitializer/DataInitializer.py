def initialize_node_info(my_node):
    #todo: Get Node information from online-node
    from CommunicationManager import Sender
    import socket, thread
    import DataSyncThread

    print "Syncronization starting..."

    trust_node_ip = NodeInformation.trust_node_ip
    request_ip = socket.gethostbyname(socket.gethostname())

    # Node is SEZIP
    # Response ip information
    if request_ip == trust_node_ip:
        thread.start_new_thread(DataSyncThread.response_node_info, ("SyncThrd", request_ip))

    # Other Node
    # Send request ip information
    else:
        from DataInitializer import BlockSynchronizer
        Sender.block_sync()
        #Sender.send_sync(fetch_node_ip, request_ip)
        thread.start_new_thread(DataSyncThread.request_node_info, ("SyncThrd2", request_ip))
        #Sender.send(fetch_node_ip, my_node)

def initialize_block():
    from CommunicationManager import ConnectionChecker
    from StorageManager import FileController

    # ip_list[0] : local ip address
    #               not need to check
    ip_list = FileController.get_ip_list()
    connected_node_address = []

    print ip_list
    for check_ip in ip_list[1:]:
        if ConnectionChecker.connection_check(check_ip) is True:
            connected_node_address.append(check_ip)

    # check block height
    print connected_node_address
