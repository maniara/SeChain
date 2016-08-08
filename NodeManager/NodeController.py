import JsonEncoder
import os
from StorageManager import FileController

def get_node(ip_address):
    import Node, json
    from KeyGenerator import generation_key_pair

    # Check node list (NodeInfo.txt)
    # Create New Node and Send node information to SEZIP.
    if FileController.get_node(ip_address) is False:

        gen_public_key, gen_private_key = generation_key_pair(2**256)

        node = Node.Node(ip_address)
        node.public_key = gen_public_key
        node.private_key = gen_private_key

        json_node = {
            'type' : 'N',
            'is_disabled' : False,
            'public_key' : node.public_key,
            'private_key' : node.private_key,
            'ip_address' : node.ip_address
        }
        new_json_node = json.dumps(json_node, cls=JsonEncoder.json_encoder)

        file_path = os.path.dirname(os.path.dirname(__file__)) + '\DataBase' + '\\'
        path_info = file_path + '\NodeInfo.txt'

    # add node to file and send node to other nodes
        FileController.write(path_info, new_json_node)
        send_my_node_info(new_json_node)
        return json_node, new_json_node

    # Node exist
    else:
        print("Node is already in the list")
        existed_node = FileController.get_node(ip_address)
        existed_node_json = json.loads(existed_node)
        return existed_node_json, existed_node


def send_my_node_info(my_node):
    from CommunicationManager import Sender
    print "send node info"
    Sender.send_sync('163.239.27.32', my_node)


def add_new_node(node_info_entity):
    # Parameter : data_entity(JSON object)
    file_path = os.path.dirname(os.path.dirname(__file__)) + '\DataBase' + '\\'
    path_info = file_path + '\NodeInfo.txt'

    FileController.write(path_info, node_info_entity)
    print "New node information is added"

    return True



