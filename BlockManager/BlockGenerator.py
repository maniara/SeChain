def check_status():
    return False

def generate_block():
    from CommunicationManager import Sender
    Sender.send("Block")