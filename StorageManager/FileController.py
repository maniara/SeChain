import os

database_path = os.path.dirname(os.path.dirname(__file__)) + '\DataBase' + '\\'
block_storage_path = os.path.dirname(os.path.dirname(__file__)) + '\BlockStorage' + '\\'
node_info_file = 'NodeInfo.txt'
ledger_file = 'Transactions.txt'


def write(file_name, message):
    import io
    f = open(file_name, 'a')
    f.write(message)
    f.write('\n')
    f.close()


def read_all_line(file_name):
    import io
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
    print "\nTransaction added"


def get_ip_list():
    import json
    f = open(database_path+node_info_file, 'r')
    ip_list = []
    while True:
        line = f.readline()
        if not line:
            break
        node_info = json.loads(line)
        ip_list.append(node_info['ip_address'])

    return ip_list


def get_transaction_list():
    line_list = read_all_line(database_path + ledger_file)
    return line_list


def get_node(ip_address):
    import json, ast

    node_list = get_node_list()
    for node_string in node_list:
        node = json.loads(node_string)

        if node['ip_address'] == ip_address:
            return node_string
        else:
            continue
    return False


def get_node_list():
    f = open(database_path + node_info_file, 'r')
    node_list = []
    while True:
        line = f.readline()
        if not line: break
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


def get_last_block():
    '''return last block file contents'''
    return last_block_file_name, last_block
