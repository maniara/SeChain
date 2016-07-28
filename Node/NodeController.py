
# create new node
# return JSON OBJECT
def get_node(ip_address):
    import Node, json, os
    from KeyGenerator import generation_key_pair
    from DataStorage import FileController
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

    return new_json_node

# # Add node to file
# def add_node(node):
#     import os
#
#     new_line ='\n'
#
    file_path = os.path.abspath(os.path.dirname(__file__))
    file_path = file_path[:-4] + 'DataBase'
    path_info = file_path +'\NodeInfo.txt'
#
#     f = open(path_info, 'a')
#     f.write(node)
#     f.write(new_line)
#
#     return True


