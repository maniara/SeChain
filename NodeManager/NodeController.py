import JsonEncoder
import os
import json
from StorageManager import FileController

def get_node():
    import Node, json
    from SeChainController import Property
    from KeyGenerator import generation_key_pair

    # Check node list (NodeInfo.txt)
    # Create New Node and Send node information to SEZIP.
    if FileController.get_node() is False:
        print "Joining SeChain"



        '''

            need to change -> Ecdsa key pair
        '''
        gen_public_key, gen_private_key = generation_key_pair(2 ** 256)

        node = Node.Node(Property.my_ip_address)
        node.public_key = gen_public_key
        node.private_key = gen_private_key

        '''
            Date: 2016/11/11
            remove redundancy field
        '''
        json_node = {
            'type' : 'N',
            'ip_address' : node.ip_address,
            'public_key' : node.public_key,
            'private_key' : node.private_key
        }
        new_json_node = json.dumps(json_node, cls=JsonEncoder.json_encoder)

        return json_node, new_json_node

    # Node exist
    else:
        print("Node is already in the list")
        existed_node = FileController.get_node()
        existed_node_json = json.loads(existed_node)
        return existed_node_json, existed_node

'''
node information: ip address, public key, type, is_disabled(redundant yet)
'''
def send_my_node_info(_ip):
    from CommunicationManager import Sender
    # json string -> json object
    json_node = {
        'type': 'N',
        'ip_address': _ip
    }
    send_json_node = json.dumps(json_node, cls=JsonEncoder.json_encoder_send)

    Sender.send_to_all_node(send_json_node)


def add_new_node(node_info_entity):
    sync_flag = False
    # Parameter : data_entity(JSON object)
    node_list = FileController.get_ip_list()

    for outer_list in node_list:
        outer_list = str(outer_list)
        if outer_list in node_info_entity['ip_address']:
            sync_flag = True

    if sync_flag is False:
        FileController.add_node_info(json.dumps(node_info_entity))
        print "New node("+ node_info_entity['ip_address'] +") is added in local storage"

    else :
        print "Node(" + node_info_entity['ip_address'] + ") is already listed"

    return True



