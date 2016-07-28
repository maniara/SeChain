class MainController(object):
    myNode = None
    nodeList = None

    def __init__(self):
        return 0

    @staticmethod
    def start():
        import socket
        from Node import NodeController

        ip_address = socket.gethostbyname(socket.gethostname())
        print ip_address
        if NodeController.is_node(ip_address) == True:
            print "T"
        else:
            print NodeController.create_node(ip_address)

MainController.start()



