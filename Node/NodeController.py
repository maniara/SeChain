class NodeController(object):

    @staticmethod
    def is_node(ip_address):
        return True;

    @staticmethod
    def create_node(ip_address):
        import Node
        return Node()