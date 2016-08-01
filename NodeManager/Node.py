class Node(object):

    def __init__(self, ip_address):
        self.type = 'N'
        self.is_disabled = False
        self.ip_address = ip_address
        self.public_key = ''
        self.private_key = ''
