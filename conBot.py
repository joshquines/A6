import time
import socket 
import sys 


HOST = None
PORT = None 
CHANNEL = None 
IRCSOCKET = None 

# CONTROLLER INFO
conNick = "CONTROLLER "
liveConnection = False # Flag to see if controller connection to IRC Server is active


# Get response from Bot 
def getResponse():
    try:
        # Get response from bot
        msg = ircSocket.recv(1024).decode('utf-8')

# COMMANDS
# Get bot status
def botStatus():
    pass

# Tell bot to attack
def botAttack(host, port, channel):
    pass

# Tell bot to move channel
def botMove(host, port, channel):
    pass 

# Tell bot to quit
def botQuit():
    pass 

# Tell bot to shutdown
def botShutdown(): 
    pass

def sendCommand(msg):
    pass 

def botHandler():
    global liveConnection
    while liveConnection:
        pass
        # Do stuff 


# CONNECT TO IRC SERVER CHANNEL
# This next line goes to a function
# ircSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def serverConnect(host, port):
    global IRCSOCKET, liveConnection 
    try:
        IRCSOCKET = connect((host,port))
        print("Connection successful")
        liveConnection = True 
        return True
    except:
        print("Connection failed")
        return False 



if __name == "__main__":
    global HOST, PORT, CHANNEL, PHRASE, IRCSOCKET

    # Get sys.argv
    if len(sys.argv) != 4:
        print("Wrong numnber of arguments")
        sys.exit() 
    
    HOST = sys.argv[0]
    PORT = sys.argv[1]
    CHANNEL = sys.argv[2]
    PHRASE = sys.argv[3]

    if not PORT.isdigit():
        print("Invalid port.")
        sys.exit() 
    
    # Keep connection to IRC server 
    while True:
        connectStatus = serverConnect(HOST, PORT)
        if connectStatus == True:
            # Start giving commands to bot
            botHandler()
