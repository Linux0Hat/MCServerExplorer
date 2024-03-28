# MCServerExplorer

MCServerExplorer is a python program for searching and testing servers

## DISCLAMER

**/!\ I'M NOT RESPONSIBLE FOR WHAT YOU DO WITH THIS PROGRAMME !**  
**/!\ USE THIS ONLY ON YOUR EQUIPMENT**

## Run

### Dependencies

- `python3`

### Install

1. Clone the repository:

   ```
   git clone https://github.com/Linux0Hat/MCServerExplorer.git
   ```

2. Navigate to the project directory:

   ```
   cd MCServerExplorer
   ```

3. Install pip3 dependencies:

   ```
   pip3 install -r requirement.txt
   ```

## How to Use

### Explorer

Explore, find and save random minecraft server.  
Use explorer like this :

```
python3 explorer.py [-h] [--threads THREADS] [--timeout TIMEOUT] [--datafile DATAFILE] [--port PORT]

options:
  -h, --help           show this help message and exit
  --threads THREADS    Threads (default = 300)
  --timeout TIMEOUT    Timeout (ms, default = 100)
  --datafile DATAFILE  Datafile (default = database.db)
  --port PORT          Port (default = 25565)
```

### Tester

Test and update servers in your database.  
User tester like this :

```
python3 tester.py [-h] [--minplayers MINPLAYERS] [--players PLAYERS] [--maxplayers MAXPLAYERS] [--timeout TIMEOUT] [--capacity CAPACITY] [--version VERSION] [--threads THREADS]

options:
  -h, --help            show this help message and exit
  --minplayers MINPLAYERS
                        Minimum of players connected on the server
  --players PLAYERS     Players connected on the server
  --maxplayers MAXPLAYERS
                        Maximum of players connected on the server
  --timeout TIMEOUT     Timout (ms)
  --capacity CAPACITY   Server's player capacity
  --version VERSION     Server's version
  --threads THREADS     Threads (default = 300)
```

### Merge

Merge multiple database files.  
Use merge like this :

```
merge.py [-h] [--datafile DATAFILE]

options:
  -h, --help           show this help message and exit
  --datafile DATAFILE  Database file name.
```

Project maintained by Linux_Hat
