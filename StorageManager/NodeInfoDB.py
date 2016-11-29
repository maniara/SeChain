import sqlite3
from SeChainController import Property

path = Property.DB_PATH + 'nodeinfo.db'


def create_nodeinfo_table():
    con = sqlite3.connect(path)
    cursor = con.cursor()
    cursor.execute("CREATE TABLE nodeinfo(idx, ip)")
    con.close()


def insert_node_db(idx, ip):
    con = sqlite3.connect(path)
    cursor = con.cursor()
    passed_node_info = [idx, ip]
    cursor.execute("INSERT INTO nodeinfo VALUES (?, ?)", passed_node_info)
    con.commit()

    con.close()


def read_db():
    con = sqlite3.connect(path)
    cursor = con.cursor()
    cursor.execute("SELECT * FROM nodeinfo")

    for result in cursor:
        print result


if __name__ == '__main__':
    create_nodeinfo_table()
    insert_node_db('1', '1.1.1.1')
    insert_node_db('2', '2.2.2.2')
    read_db()