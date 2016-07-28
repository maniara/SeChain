def get_node(ip_address):
    import Node, json, os, ast
    from KeyGenerator import generation_key_pair
    from DataStorage import FileController

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
        new_json_node = json.dumps(json_node)

        file_path = os.path.abspath(os.path.dirname(__file__))
        file_path = file_path[:-4] + 'DataBase'
        path_info = file_path + '\NodeInfo.txt'

    # add node to file
        FileController.write(path_info, new_json_node)
        return json_node

    else:
        print("Node is already in the list")
        existed_node = FileController.get_node(ip_address)
        existed_node_json = json.loads(existed_node)
        return existed_node_json



