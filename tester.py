import threading
import sqlite3
from mcstatus import JavaServer
import colorama
import argparse
import random

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
args = parser.parse_args()

def ping_server(addr, port):
    server = JavaServer.lookup(f"{addr}:{port}")
    try:
        status = server.status()
    except:
        return
        
    if not status:
        return
    minplayers = args.minplayers
    players = args.players
    maxplayers = args.maxplayers
    timeout = args.timeout
    capacity = args.capacity
    version = args.version

    if minplayers and minplayers>=status.players.online:
        return
    if players and players!=status.players.online:
        return
    if maxplayers and maxplayers<=status.players.online:
        return
    if timeout:
        if timeout <= status.latency:
            return
    else:
        if 100 <= status.latency:
            return
    if capacity and capacity != status.players.max:
        return
    if version and not version in str(status.version.name):
        return
            
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
    return

def Main():
    threads = []
    for server in database:
        thread = threading.Thread(target=ping_server, args=[server[1], server[2]])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    print("Complete")

if __name__ == "__main__":
    Main()