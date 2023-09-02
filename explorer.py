import threading
import sqlite3
from mcstatus import JavaServer
import colorama
import random
import socket
import struct
from datetime import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--threads', type=int, help='Threads (default = 400)')
parser.add_argument('--timeout', type=int, help='Timeout (ms, default = 100)')
parser.add_argument('--datafile', type=str, help='Datafile (default = database.db)')
parser.add_argument('--port', type=int, help='Port (default = 25565)')
args = parser.parse_args()

num_threads = args.threads
timeout = args.timeout
datafile = args.datafile
port_ = args.port

if not num_threads:
    num_threads = 400

if not timeout:
    timeout = 100

if not datafile:
    datafile = "database.db"

if not port_ :
    port_ = 25565

results = []

db = sqlite3.connect(datafile)
cursor = db.cursor()
colorama.init()

cursor.execute('''CREATE TABLE IF NOT EXISTS "servers" ( id INTEGER PRIMARY KEY AUTOINCREMENT, addr TEXT, port INTEGER, first_seen DATETIME, last_seen DATETIME);''')
db.commit()

def ping_server(port):
    addr = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout/1000)  # Temps d'attente en secondes
            s.connect((addr, port))
    except Exception as e:
        return False

    server = JavaServer.lookup(f"{addr}:{port}")
    try:
        status = server.status()
    except:
        return
    if  status:
        players = f"{status.players.online}/{status.players.max}"
        
        ip = f"{addr}:{port}"
        
        version=str(status.version.name)
        if len(version) > 27:
            version = f"{version[:27-3]}..."
        
        latency = str(int(status.latency))+"ms"

        description = status.description
        description = description.replace("§1",colorama.Fore.BLUE)
        description = description.replace("§2",colorama.Fore.GREEN)
        description = description.replace("§3",colorama.Fore.CYAN)
        description = description.replace("§4",colorama.Fore.RED)
        description = description.replace("§5",colorama.Fore.MAGENTA)
        description = description.replace("§6",colorama.Fore.YELLOW)
        description = description.replace("§7",colorama.Fore.LIGHTBLACK_EX)
        description = description.replace("§8",colorama.Fore.LIGHTBLACK_EX)
        description = description.replace("§9",colorama.Fore.LIGHTBLUE_EX)
        description = description.replace("§a",colorama.Fore.LIGHTGREEN_EX)
        description = description.replace("§b",colorama.Fore.LIGHTCYAN_EX)
        description = description.replace("§c",colorama.Fore.LIGHTRED_EX)
        description = description.replace("§d",colorama.Fore.LIGHTMAGENTA_EX)
        description = description.replace("§e",colorama.Fore.LIGHTYELLOW_EX)
        description = description.replace("§f",colorama.Fore.WHITE)
        description = description.replace("\n"," - ")
        description = description.replace("§k","")
        description = description.replace("§l",colorama.Style.BRIGHT)
        description = description.replace("§m","")
        description = description.replace("§n","\e[4m")
        description = description.replace("§o","")
        description = description.replace("§r",colorama.Style.RESET_ALL)
        
        print(f"{colorama.Fore.LIGHTRED_EX}{players:10}{colorama.Fore.LIGHTBLUE_EX}{ip:22}{colorama.Fore.LIGHTYELLOW_EX}{version:30}{colorama.Fore.LIGHTGREEN_EX}{latency:6}{colorama.Style.RESET_ALL}{description}{colorama.Style.RESET_ALL}")

        results.append([addr, port])
    return
    
def Main():
    compter = 0
    while True:
        try : 
            if threading.active_count() < num_threads:
                thread = threading.Thread(target=ping_server, args=[port_])
                thread.start()
            for result in results:
                compter += 1
                addr = result[0]
                port = result[1]
                cursor.execute(f"SELECT * from servers WHERE addr='{addr}' AND port={port}")
                data = cursor.fetchall()
                if not data:
                    cursor.execute(f"INSERT INTO servers (addr, port, first_seen, last_seen) VALUES('{addr}',{port},'{datetime.now()}','{datetime.now()}')")
                    db.commit()
                else :
                    cursor.execute(f"UPDATE servers SET last_seen = '{datetime.now()}' WHERE id = {data[0][0]}")
                    db.commit()
                results.remove(result)
        except:
            break
    print("\nTerminated.")
    cursor.execute("SELECT * FROM servers")
    print(f"{len(cursor.fetchall())} servers in database, {compter} added.")
            

if __name__ == "__main__":
    Main()