from SeChainController import NodeInformation

class MainController(object):

    def __init__(self):
        return 0

    @staticmethod
    def initiate_node():
        import thread, time
        from StorageManager import FileController
        from CommunicationManager import Receiver
        from NodeInitializer import NodeListSynchronizer
        from BlockManager import BlockGenerator
        from NodeInitializer import BlockSynchronizer
        from CommunicationManager import Sender
        from SeChainUI import MainUI

        #my ip check
        MainController.set_my_node()
        print ("Have got node information")
        MainUI.MainFrame.write_console(NodeInformation.ui_frame, "Have got node information")

        # sync blocks
        MainUI.MainFrame.write_console(NodeInformation.ui_frame, "Blocks are synchronizing now")
        BlockSynchronizer.sync_blocks()

        while(True):
           if(NodeInformation.block_sync == True):
                break
        MainUI.MainFrame.write_console(NodeInformation.ui_frame, "Blocks are synchronized")

        # sync node list
        MainUI.MainFrame.write_console(NodeInformation.ui_frame, "Downloading node list")
        NodeListSynchronizer.download_node_list(MainController.my_node_json)

        #time.sleep(3)
        #MainController.command_control()

    @staticmethod
    def node_start():
        import NodeInformation
        import thread
        from StorageManager import FileController
        from CommunicationManager import Receiver

        #node listener start
        NodeInformation.nodeList = FileController.get_node_list()
        thread.start_new_thread(Receiver.start, ("Listener_Thread", NodeInformation.my_ip_address, NodeInformation.port))


    @staticmethod
    def get_ip_address():
        import socket
        import NodeInformation
        NodeInformation.my_ip_address = socket.gethostbyname(socket.gethostname())
        return NodeInformation.my_ip_address

    @staticmethod
    def set_my_node():
        from NodeManager import NodeController
        import NodeInformation
        NodeInformation.myNode, NodeInformation.my_node_json = NodeController.get_node()

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
#MainController.start()
