import socket
import os
import sys
import time
import random 


HOST = None 
PORT = None 
CHANNEL = None 
PHRASE = None 
IRCSOCKET = None 

# DETERMINES IF BOT STAYS UP OR NOT
BOTONLINE = False
CONSTATUS = False 
SHUTDOWN = False 

# Bot Info
botNick = "IRC_BOT" str(random.randrange(10000))
conNick = None 
attackCount = 0

# Bot joins a channel
def joinChannel(HOST, PORT, CHANNEL, PHRASE):
    global IRCSOCKET, botNick 
    try:
        # Connect to Server 
        IRCSOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        IRCSOCKET.connect((HOST,PORT))
        # Connect to Channel
        sendMsg(IRCSOCKET, "USER " + botNick + " " + botNick + " " + botNick + ": Connecting to server\n")
        sendMsg(IRCSOCKET, "NICK " + botNick + "\n")
        sendMsg(IRCSOCKET, "JOIN " + CHANNEL + "\n")
        return True
    except:
        print(str(botNick) + " unable to join channel.")
        return False 
    

# Bot communicates with Controller
def sendPrivate() 

# Bot listens for commands from IRC
def getCommand():

    # Parse commands

    if command == "status":
        botStatus()
    elif command == "attack":
        botAttack()
    elif command == "move":
        # Parse newHost 
        # Parse newPort 
        # Parse newChannel
        canMove = botMove(newHost, newPort, newChannel)
        if canMove:
            pass 
            # Let Controller know that successful 
        else:
            pass 
            # Let Controller know that it failed to move
    elif command == "quit":
        botQuit() 
    elif command == "shutdown":
        botShutdown()

# Do pingPong protocol
def pingPong():
    # Receive data here 
    if data.


# DO COMMAND ACTIONS HERE -----------------------------

# Send Stats
def botStatus()

# Attack Server
def botAttack():
    global conNick, botNick, attackCount 
    try:
        attackCount = attackCount + 1 
        # Send private message that attack was successful
    except:
        pass 
        # Send private message that attack failed 


# Move Server
def botMove(newHost, newPort, newChannel):
    global HOST, PORT, CHANNEL, botNick 
    # First attempt to connect to new server 
    try:
        newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        newSocket.connect((newHost, newPort))
        # At this point, if it doesn't throw an exception, it should be good 
        # Now connect bot to channel
        sendMsg(newSocket, "USER " + botNick + " " + botNick + " " + botNick + ": Connecting to server\n")
        sendMsg(newSocket, "NICK " + botNick + "\n")
        sendMsg(newSocket, "JOIN " + CHANNEL + "\n")

        # Disconnect from old Channel
        IRCSOCKET.close()

        # If it reaches this point, connection is successful. Change globals
        HOST = newHost 
        PORT = newPort 
        CHANNE: = newChannel 
        IRCSOCKET = newSocket 
        return True 
    except:
        print("ERROR: Unable to move to new channel\nBot still in old channel")
        return False 



# Controller disconnect
def botQuit():
    global CONSTATUS 
    CONSTATUS = False 
    print("Controller has gone offline ")

# Shutdown
def botShutdown():
    global SHUTDOWN 
    SHUTDOWN == TRUE 
    return


# Main Handler Loop
def handler(self):

    # Connect to IRC Server 
    if self.CONSTATUS == False:
        joinChannel()

    # Receive Data here 




# Main Start
if __name__ == "__main__":

    # Get args here
    global HOST, PORT, CHANNEL, PHRASE, SHUTDOWN

    if len(sys.argv) != 4:
        print("Wrong number of inputs")
        sys.exit()

    HOST = sys.argv[0]
    PORT = sys.argv[1]
    CHANNEL = sys.argv[2]
    PHRASE = sys.argv[3]

    # Check for valid port
    if not PORT.isdigit():
        print("Invalid port")
        sys.exit()

    # Attempt connection if bot is not currently online
    if not BOTONLINE:
        preCheck = joinChannel(HOST, PORT, CHANNEL, PHRASE)

    # Terminate if unable to initially join
    if not preCheck:
        sys.exit()
    
    # Run the Bot forever until close
    while not SHUTDOWN:
        handler()

  


