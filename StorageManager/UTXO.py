import sqlite3

con = sqlite3.connect('UTXO.db')
cursor = con.cursor()

def insert_db():
    cursor.execute("CREATE TABLE utxodb(Address , Utxo)")
    cursor.execute("INSERT INTO utxodb VALUES('1KSADM2ddf2', 0.2223)")
    cursor.execute("INSERT INTO utxodb VALUES('1sdfeDM2ddf2', 0.344)")
    cursor.execute("INSERT INTO utxodb VALUES('1xKDmwwl', 0.10001111111)")
    con.commit()
    # con.close()


def read_db():
    cursor.execute("SELECT * FROM utxodb")

    for result in cursor:
        print result

if __name__ == '__main__':
    insert_db()
    read_db()
    con.close()

