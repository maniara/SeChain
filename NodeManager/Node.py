class Node(object):
    '''
        public key & private key
    '''
    def __init__(self, ip_address):
        self.type = 'N'
        self.ip_address = ip_address
        self.public_key = None
        self.private_key = None
