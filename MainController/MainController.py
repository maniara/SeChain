class MainController(object):
    myNode = None
    my_node_json = None
    nodeList = None

    def __init__(self):
        return 0

    @staticmethod
    def start():
        import thread, time
        from StorageManager import FileController
        from CommunicationManager import Receiver
        from DataInitializer import DataInitializer
        from BlockManager import BlockGenerator
        from BlockManager import BlockSync
        from CommunicationManager import Sender

        #my ip check
        ip_address = MainController.get_ip_address()
        print "Your IP : ", ip_address
        MainController.set_my_node(ip_address)

        # transaction listener start
        MainController.nodeList = FileController.get_node_list()
        thread.start_new_thread(BlockSync.block_check, ("BlockSync", ip_address))
        thread.start_new_thread(Receiver.start, ("Thread-1", ip_address))
        #sync file database
        DataInitializer.initialize_node_info(MainController.my_node_json)
        #DataInitializer.initialize_block()
        #check condition for creating block
        #thread.start_new_thread(BlockGenerator.check_status, ())

        time.sleep(3)
        MainController.command_control()

    @staticmethod
    def get_ip_address():
        import socket

        ip_address = socket.gethostbyname(socket.gethostname())
        return ip_address

    @staticmethod
    def set_my_node(ip_address):
        from NodeManager import NodeController
        MainController.myNode, MainController.my_node_json = NodeController.get_node(ip_address)


    @staticmethod
    def command_control():
        from TransactionManager import TransactionController
        from CommunicationManager import Sender
        from StorageManager import FileController
        from BlockManager import BlockGenerator
        import json

        cmd = None
        while cmd != 'q':
            cmd = raw_input('(t : send transaction, v : view transaction buffer, q : quit) >')

            # UI
            if cmd == 't':
                receiver_ip = raw_input('Receiver IP : ')
                amount = raw_input('Amount : ')
                message = raw_input('Message : ')
                trx_json = TransactionController.create_transaction(MainController.myNode['public_key'],
                                                                    MainController.myNode['private_key'], cmd,
                                                                    receiver_ip, amount, message, '')

                if FileController.get_number_of_transactions() >= 0:
                    block = BlockGenerator.generate_block(trx_json)
                    block_temp = json.dumps(block, indent=4, default=lambda o: o.__dict__, sort_keys=True)
                    Sender.send_to_all_node(block_temp)
                else:
                    Sender.send_to_all_node(trx_json)
            elif cmd == 'v':
                TransactionController.print_all_transaction()

            elif cmd == 'ct':
                receiver_ip = raw_input('Receiver IP : ')
                amount = raw_input('Amount : ')
                message = raw_input('Message : ')
                source = raw_input('Soruce Name : ')
                args = raw_input('Args (split by ' ') : ')
                contract_datas = {'source' : source , 'args' : args}
                trx_json = TransactionController.create_transaction(MainController.myNode['public_key'],
                                                                    MainController.myNode['private_key'], cmd,
                                                                    receiver_ip, amount, message, contract_datas)

                if FileController.get_number_of_transactions() >= 0:
                    block = BlockGenerator.generate_block(trx_json)
                    block_temp = json.dumps(block, indent=4, default=lambda o: o.__dict__, sort_keys=True)
                    Sender.send_to_all_node(block_temp)
                else:
                    Sender.send_to_all_node(trx_json)

            elif cmd == 'rt':
                receiver_ip = raw_input('Receiver IP : ')
                amount = raw_input('Amount : ')
                message = raw_input('Message : ')
                contractAddr = raw_input('contractAddr : ')
                function = raw_input('functionName : ')
                args = raw_input('Args (split by ' ') : ')
                contract_datas = {'contractAddr' : contractAddr ,'function' : function,  'args' : args}

                trx_json = TransactionController.create_transaction(MainController.myNode['public_key'],
                                                                    MainController.myNode['private_key'], cmd,
                                                                    receiver_ip, amount, message, contract_datas)
                print 'now transaction num : ',FileController.get_number_of_transactions()
                if FileController.get_number_of_transactions() >= 0:
                    block = BlockGenerator.generate_block(trx_json)
                    block_temp = json.dumps(block, indent=4, default=lambda o: o.__dict__, sort_keys=True)
                    Sender.send_to_all_node(block_temp)
                else:
                    Sender.send_to_all_node(trx_json)
            else:
                continue

        return 0
    '''
    @staticmethod
    def receive_user_data():
        receiver_ip = raw_input('Receiver IP : ')
        amount = raw_input('Amount : ')
        message = raw_input('Message : ')

        return receiver_ip,amount,message
    '''
    '''
def makeTransaction(tx_type,receiver_ip,amount,message,contract_datas):

    trx_json = TransactionController.create_transaction(MainController.myNode['public_key'], MainController.myNode['private_key'],tx_type, receiver_ip, amount, message,contract_datas)

    if FileController.get_number_of_transactions() == 5:
        block = BlockGenerator.generate_block(trx_json)
        block_temp = json.dumps(block,  indent=4, default=lambda o: o.__dict__, sort_keys=True)
        Sender.send_to_all_node(block_temp)
    else:
        Sender.send_to_all_node(trx_json)


'''
MainController.start()
