import os

database_path = os.path.dirname(os.path.dirname(__file__)) + '\DataBase' + '\\'
node_info_file = 'NodeInfo.txt'
ledger_file = 'Ledger.txt'


def write(file_name, message):
    f = open(file_name,'a')
    f.write(message)
    f.write('\n')
    f.close()


def read_all_line(file_name):
    f=open(file_name,'r')
    line_list=[]
    while True:
        line = f.readline()
        if not line : break
        else : line_list.append(line)
    f.close()
    return line_list


def add_transaction(trx):
    write(database_path + ledger_file, trx)


def get_ip_list():

    return ip_list


def get_transaction_list():
    line_list = read_all_line(database_path + ledger_file)
    return line_list


def get_node(ip_address):
    import json

    node_list = get_node_list()
    for node_string in node_list:
        node = json.loads(node_string)
        if node.ip_address == ip_address:
            return node_string
        else :
            continue
    return False
