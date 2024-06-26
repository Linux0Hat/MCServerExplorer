import threading
import sqlite3
from mcstatus import JavaServer
import colorama
import argparse
import random
from datetime import datetime
import sys

db = sqlite3.connect("database.db")
cursor = db.cursor()
colorama.init()

cursor.execute('''CREATE TABLE IF NOT EXISTS "servers" ( id INTEGER PRIMARY KEY AUTOINCREMENT, addr TEXT, port INTEGER, first_seen DATETIME, last_seen DATETIME);''')
db.commit()

cursor.execute("SELECT * FROM servers")
database = cursor.fetchall()
random.shuffle(database)

parser = argparse.ArgumentParser()
parser.add_argument('--minplayers', type=int, help='Minimum of players connected on the server')
parser.add_argument('--players', type=int, help='Players connected on the server')
parser.add_argument('--maxplayers', type=int, help='Maximum of players connected on the server')
parser.add_argument('--timeout', type=int, help='Timout (ms)')
parser.add_argument('--capacity', type=int, help="Server's player capacity")
parser.add_argument('--version', type=str, help="Server's version")
parser.add_argument('--threads', type=str, help="Threads (default = 300)")
args = parser.parse_args()

minplayers = args.minplayers
players = args.players
maxplayers = args.maxplayers
timeout = args.timeout
capacity = args.capacity
version = args.version

num_threads = args.threads
if not num_threads:
    num_threads = 300

event = threading.Event()
results = []

def ping_server():
    minplayers = args.minplayers
    players = args.players
    maxplayers = args.maxplayers
    timeout = args.timeout
    capacity = args.capacity
    version = args.version
    while True: 
        try :
            if not database or event.is_set():
                break
            server = database.pop(0)
            id = server[0]
            addr = server[1]
            port = server[2]
            server = JavaServer.lookup(f"{addr}:{port}")
            try:
                status = server.status()
            except:
                continue
            
            if not status:
                continue

            if minplayers and minplayers>=status.players.online:
                continue
            if players and players!=status.players.online:
                continue
            if maxplayers and maxplayers<=status.players.online:
                continue
            if timeout:
                if timeout <= status.latency:
                    continue
            else:
                if 100 <= status.latency:
                    continue
            if capacity and capacity != status.players.max:
                continue
            if version and not version in str(status.version.name):
                continue
                    
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
            
            if event.is_set():
                break

            results.append([f"{colorama.Fore.LIGHTRED_EX}{players:10}{colorama.Fore.LIGHTBLUE_EX}{ip:22}{colorama.Fore.LIGHTYELLOW_EX}{version:30}{colorama.Fore.LIGHTGREEN_EX}{latency:6}{colorama.Style.RESET_ALL}{description}{colorama.Style.RESET_ALL}", id])
        except:
            pass

def Main():
    try:
        threads = []
        for i in range(0, num_threads):
            thread = threading.Thread(target=ping_server, args=[])
            threads.append(thread)
            thread.start()
        while threading.active_count() != 1:
            for result in results:
                print(result[0])
                cursor.execute(f"UPDATE servers SET last_seen = '{datetime.now()}' WHERE id = {result[1]}")
                db.commit()
    except:
        event.set()
        print("\nStopping...")
    while threading.active_count() != 1:
        pass
    print("Complete")
    sys.exit()

if __name__ == "__main__":
    Main()