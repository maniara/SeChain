import sqlite3
from SeChainController import Property

path = Property.DB_PATH + 'UTXO.db'


def create_utxo_table():
    con = sqlite3.connect(path)
    cursor = con.cursor()

    cursor.execute("CREATE TABLE UTXO(address, utxo)")

    con.close()


def insert_utxo_db(address, coin):
    con = sqlite3.connect(path)
    cursor = con.cursor()

    passed_utxo_info = [address, coin]

    cursor.execute("INSERT INTO UTXO VALUES (?, ?)", passed_utxo_info)
    con.commit()

    con.close()


def update_utxo_db(address, coin):
    con = sqlite3.connect(path)
    cursor = con.cursor()

    passed_utxo = [coin, address]

    cursor.execute("UPDATE UTXO SET utxo=  ? WHERE address= ?", passed_utxo)

    con.commit()
    con.close()


def read_db():
    con = sqlite3.connect(path)
    cursor = con.cursor()
    cursor.execute("SELECT * FROM UTXO")

    for result in cursor:
        print result

    con.close()


'''
return tuple (address, utxo)
'''
def search_utxo(address):
    con = sqlite3.connect(path)
    cursor = con.cursor()

    cursor.execute("SELECT * FROM UTXO WHERE address=?", (address,))

    result = cursor.fetchone()

    print "UTXO IS ", result

    con.close()

    return result

'''
module test
'''

if __name__ == '__main__':
    create_utxo_table()
    insert_utxo_db('1abcd', 10)
    insert_utxo_db('2abcd', 20)

    read_db()

    update_utxo_db('1abcd', 30)

    res =search_utxo('1abcd')

    print res[0]

    read_db()