def initialize_node_info(my_node):
    #todo: Get Node information from online-node
    from CommunicationManager import Sender
    import socket, thread
    import DataSyncThread

    print "Syncronization starting..."
    print ''

    # sezip : 163.239.27.32
    fetch_node_ip = '163.239.27.32'
    request_ip = socket.gethostbyname(socket.gethostname())

    # Node is SEZIP
    # Response ip information
    if request_ip == fetch_node_ip:
        thread.start_new_thread(DataSyncThread.response_node_info, ("SyncThrd", request_ip))

    # Other Node
    # Send request ip information
    else:
        Sender.send_sync(fetch_node_ip, request_ip)
        thread.start_new_thread(DataSyncThread.request_node_info, ("SyncThrd2", request_ip))


    return False

def initialize_ledger():
    #todo:
    return False