class ValueData(object):

    def __init__(self, sender, receiver, amount, msg):
        self.sender_ip = sender
        self.receiver_ip = receiver
        self.amount = amount
        self.message = msg