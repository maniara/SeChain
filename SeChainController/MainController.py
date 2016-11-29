from SeChainController import Property
from NodeManager import NodeController

class MainController(object):

    def __init__(self):
        return 0

    @staticmethod
    def initiate_node(*args):

        from NodeInitializer import NodeListSynchronizer

        from NodeInitializer import BlockSynchronizer

        from SeChainUI import MainUI

        from StorageManager import NodeInfoDB, utxoDB

        '''
            create Database
        '''
        NodeInfoDB.create_nodeinfo_table()
        utxoDB.create_utxo_table()

        # sync blocks
        MainUI.MainFrame.write_console(Property.ui_frame, "Blocks are synchronizing now")
        BlockSynchronizer.sync_blocks()
        #
        while(True):
           if(Property.block_sync == True):
                break

        MainUI.MainFrame.write_console(Property.ui_frame, "Blocks are synchronized")


        # sync node list
        MainUI.MainFrame.write_console(Property.ui_frame, "Downloading node list")
        NodeListSynchronizer.download_node_list(Property.my_node_json)

        while (True):
            if (Property.node_sync == True):
                break

        # start node
        MainController.node_start()
        Property.myNode['ip_address']
        MainUI.MainFrame.write_console(Property.ui_frame, "Node Start")


    @staticmethod
    def node_start():
        import Property
        import thread
        from StorageManager import FileController
        from CommunicationManager import Receiver
        from SeChainUI import MainUI
        from CommunicationManager import ConnectionChecker

        #my node check
        MainController.set_my_node()
        print ("Have got node information")
        MainUI.MainFrame.write_console(Property.ui_frame, "Have got node information")


        '''
            2016/11/11
            connection check point
            find out the alive nodes through ping test
        '''
        ping = ConnectionChecker.Pinger()
        ping.thread_count = 8
        ping.hosts = FileController.get_ip_list()
        Property.alive_nodes = ping.start()


        # broadcast my node to all others and local if this is not the trust node
        MainUI.MainFrame.write_console(Property.ui_frame, "Broadcast my node information")

        NodeController.add_new_node(Property.myNode)

        if Property.my_ip_address != Property.trust_node_ip:
            NodeController.send_my_node_info(Property.myNode['ip_address'])

        #node listener start
        Property.nodeList = FileController.get_node_list()
        thread.start_new_thread(Receiver.start, ("Listener_Thread", Property.my_ip_address, Property.port))

        Property.node_started = True


    @staticmethod
    def get_ip_address():
        import socket
        import Property
        Property.my_ip_address = socket.gethostbyname(socket.gethostname())
        return Property.my_ip_address

    @staticmethod
    def set_my_node():
        from NodeManager import NodeController
        import Property
        Property.myNode, Property.my_node_json = NodeController.get_node()
        print Property.myNode
        print Property.my_node_json

    # For console based UI
    # @staticmethod
    # def command_control():
    #     from TransactionManager import TransactionController
    #     from CommunicationManager import Sender
    #     from StorageManager import FileController
    #     from BlockManager import BlockGenerator
    #     import json
    #
    #     cmd = None
    #     while cmd != 'q':
    #         cmd = raw_input('(t : send transaction, v : view transaction buffer, q : quit) >')
    #
    #         # UI
    #         if cmd == 't':
    #             receiver_ip = raw_input('Receiver IP : ')
    #             amount = raw_input('Amount : ')
    #             message = raw_input('Message : ')
    #             trx_json = TransactionController.create_transaction(MainController.myNode['public_key'],
    #                                                                 MainController.myNode['private_key'], cmd,
    #                                                                 receiver_ip, amount, message, '')
    #
    #             if FileController.get_number_of_transactions() >= 0:
    #                 block = BlockGenerator.generate_block(trx_json)
    #                 block_temp = json.dumps(block, indent=4, default=lambda o: o.__dict__, sort_keys=True)
    #                 Sender.send_to_all_node(block_temp)
    #             else:
    #                 Sender.send_to_all_node(trx_json)
    #         elif cmd == 'v':
    #             TransactionController.print_all_transaction()
    #
    #         elif cmd == 'ct':
    #             receiver_ip = raw_input('Receiver IP : ')
    #             amount = raw_input('Amount : ')
    #             message = raw_input('Message : ')
    #             source = raw_input('Soruce Name : ')
    #             args = raw_input('Args (split by ' ') : ')
    #             contract_datas = {'source' : source , 'args' : args}
    #             trx_json = TransactionController.create_transaction(MainController.myNode['public_key'],
    #                                                                 MainController.myNode['private_key'], cmd,
    #                                                                 receiver_ip, amount, message, contract_datas)
    #
    #             if FileController.get_number_of_transactions() >= 0:
    #                 block = BlockGenerator.generate_block(trx_json)
    #                 block_temp = json.dumps(block, indent=4, default=lambda o: o.__dict__, sort_keys=True)
    #                 Sender.send_to_all_node(block_temp)
    #             else:
    #                 Sender.send_to_all_node(trx_json)
    #
    #         elif cmd == 'rt':
    #             receiver_ip = raw_input('Receiver IP : ')
    #             amount = raw_input('Amount : ')
    #             message = raw_input('Message : ')
    #             contractAddr = raw_input('contractAddr : ')
    #             function = raw_input('functionName : ')
    #             args = raw_input('Args (split by ' ') : ')
    #             contract_datas = {'contractAddr' : contractAddr ,'function' : function,  'args' : args}
    #
    #             trx_json = TransactionController.create_transaction(MainController.myNode['public_key'],
    #                                                                 MainController.myNode['private_key'], cmd,
    #                                                                 receiver_ip, amount, message, contract_datas)
    #             print 'now transaction num : ',FileController.get_number_of_transactions()
    #             if FileController.get_number_of_transactions() >= 0:
    #                 block = BlockGenerator.generate_block(trx_json)
    #                 block_temp = json.dumps(block, indent=4, default=lambda o: o.__dict__, sort_keys=True)
    #                 Sender.send_to_all_node(block_temp)
    #             else:
    #                 Sender.send_to_all_node(trx_json)
    #         else:
    #             continue
    #
    #     return 0
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

