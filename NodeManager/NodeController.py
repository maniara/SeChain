import JsonEncoder


def get_node(ip_address):
    import Node, os, ast, json
    from KeyGenerator import generation_key_pair
    from StorageManager import FileController

    # Check node list (NodeInfo.txt)
    if FileController.get_node(ip_address) is False:

        gen_public_key, gen_private_key = generation_key_pair(2**256)

        node = Node.Node(ip_address)
        node.public_key = gen_public_key
        node.private_key = gen_private_key

        json_node = {
            'is_disabled' : False,
            'public_key' : node.public_key,
            'private_key' : node.private_key,
            'ip_address' : node.ip_address
        }
        new_json_node = json.dumps(json_node, cls=JsonEncoder.json_encoder)

        file_path = os.path.abspath(os.path.dirname(__file__))
        file_path = file_path[:-4] + 'DataBase'
        path_info = file_path + '\NodeInfo.txt'

    # add node to file and send node to other nodes
        FileController.write(path_info, new_json_node)
        send_my_node_info(new_json_node)
        return json_node

    else:
        print("Node is already in the list")
        existed_node = FileController.get_node(ip_address)
        existed_node_json = json.loads(existed_node)
        return existed_node_json


def send_my_node_info(my_node):
    from StorageManager import Sender
    Sender.send(my_node)


def add_new_node(node_info_entity):
    #todo : add node info into file
    return true



