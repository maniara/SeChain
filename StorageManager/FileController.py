import os

database_path = os.path.dirname(os.path.dirname(__file__)) + '\_DataStorage' + '\\'
block_storage_path = os.path.dirname(os.path.dirname(__file__)) + '\_BlockStorage' + '\\'
node_info_file = 'NodeInfo.txt'
ledger_file = 'Transactions.txt'


def write(file_name, message):

    f = open(file_name, 'a')
    f.write(message)
    f.write('\n')
    f.close()


def read_all_line(file_name):

    f = open(file_name, 'r')
    line_list = []
    while True:
        line = f.readline()
        if not line:
            break
        else:
            line_list.append(line)
    f.close()
    return line_list


def add_transaction(trx):
    write(database_path + ledger_file, trx)


def get_ip_list():
    import json
    f = open(database_path+node_info_file, 'r')
    ip_list = []
    while True:
        line = f.readline()
        line = line[:-1]
        if not line:
            break
        if line =="":
            break
        node_info = json.loads(line)
        ip_list.append(node_info['ip_address'])

    return ip_list


def get_transaction_list():
    line_list = read_all_line(database_path + ledger_file)
    return line_list


def get_node():
    import json
    from SeChainController import Property

    node_list = get_node_list()

    if len(node_list) == 0:
        return False

    for node_string in node_list:
        node = json.loads(node_string)

        if node['ip_address'] == Property.my_ip_address:
            return node_string
        else:
            continue
    return False


def get_node_list():
    f = open(database_path + node_info_file, 'r')
    node_list = []
    while True:
        line = f.readline()
        if not line:
            break
        if line == "":
            break
        node_list.append(line)
    return node_list


def get_number_of_transactions():
    return len(get_transaction_list())


def remove_all_transactions():
    f = open(database_path+ledger_file, 'w')
    f.write("")
    f.close()


def create_new_block(file_name, block_json):
    f = open(block_storage_path + file_name, 'w')
    f.write(block_json)
    f.close()

def save_my_block(block_json):
    create_new_block('a_my_block',block_json)

def get_my_block():
    f = open(block_storage_path + 'a_my_block', 'r')
    block = f.read()
    f.close()
    return block
def get_last_file():
    import os
    for root, dirs, files in os.walk(block_storage_path):
        print
    return files[-1]

def get_last_block():

    block_list = []
    for (path, dir, files) in os.walk(block_storage_path):
        block_list = files

    last_block_file_name = block_list[-1]
    last_block_tx_list = read_all_line(block_storage_path + last_block_file_name)
    last_block = "\n".join(last_block_tx_list)

    return last_block_file_name, last_block

def get_block_height():
    return len(os.walk(block_storage_path).next()[2])

def add_node_info(node_info):
    path_info = database_path + '\NodeInfo.txt'
    write(path_info, node_info)

