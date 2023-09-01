import sqlite3
import os
import argparse

def Main():   
    # Initialize     
    parser = argparse.ArgumentParser()
    parser.add_argument('--datafile', type=str, action='append', help='Database file name.')
    args = parser.parse_args()
    filenames = args.datafile
    databases = []
    for filename in filenames:
        db = sqlite3.connect(filename)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM servers")
        databases.append(cursor.fetchall())
        db.close()
    
    db = sqlite3.connect("database.db")
    cursor = db.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS "servers" ( id INTEGER PRIMARY KEY AUTOINCREMENT, addr TEXT, port INTEGER, first_seen DATETIME, last_seen DATETIME);''')
    db.commit()

    total_compt = 0
    for database in databases:
        compt = 0
        print(f"Addition {filenames[databases.index(database)]} to database.db")
        for i in database : 
            cursor.execute(f"SELECT * FROM servers WHERE addr='{i[1]}' AND port={i[2]}")
            if not cursor.fetchall():
                compt += 1
                total_compt += 1
                cursor.execute(f"INSERT INTO servers (addr, port, first_seen, last_seen) VALUES('{i[1]}',{i[2]},'{i[3]}','{i[4]}')")
                db.commit()
        print(f"{compt} adress has been added")

    print(f"End with {total_compt}")


if __name__ == "__main__":
    Main()