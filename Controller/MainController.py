class MainController(object):
    myNode = None
    nodeList = None

    def __init__(self):
        return 0

    @staticmethod
    def start():
        import thread
        from DataStorage import FileController
        from Network import Receiver

        ip_address = MainController.get_ip_address()
        print ip_address
        MainController.set_my_node(ip_address)
        MainController.nodeList = FileController.get_node_list()
        thread.start_new_thread(Receiver.start(ip_address))
        MainController.command_control()


    @staticmethod
    def get_ip_address():
        import socket

        ip_address = socket.gethostbyname(socket.gethostname())
        return ip_address

    @staticmethod
    def set_my_node(ip_address):
        from Node import NodeController
        MainController.myNode = NodeController.get_node(ip_address)

    @staticmethod
    def command_control():
        from Transaction import TransactionController
        from Network import Sender

        while
        cmd = raw_input('(t : send transaction, v : view ledgers, q : quit) >')

        # UI
        if cmd == 't':
            receiver_ip = raw_input('Receiver IP : ')
            amount = raw_input('Amount : ')
            message = raw_input('Message : ')
            trx_json = TransactionController.create_transaction(MainController.myNode, receiver_ip, amount, message)
            Sender.send(trx_json)

        elif cmd == 'v':
            TransactionController.print_all_transaction()

            elif cmd == 'q':
            return 0

MainController.start()



