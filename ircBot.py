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

class Bot:
    global HOST, PORT, CHANNEL, PHRASE, IRCSOCKET 

    # DETERMINES IF BOT STAYS UP OR NOT
    BOTONLINE = False
    CONSTATUS = False 
    SHUTDOWN = False 

    # Bot Info
    botNick = "SLAVE_PLEB" str(random.randrange(10000))
    conNick = None 
    attackCount = 0

    # Bot sends non privte message (For joining n stuff)
    def sendMsg(self, msg):
        global IRCSOCKET 
        try:
            IRCSOCKET.send(msg.encode())
        except:
            print("ERROR: Unable to send messge to channel")

    # Bot joins a channel
    def joinChannel(self, HOST, PORT, CHANNEL, PHRASE):
        global IRCSOCKET, botNick 
        try:
            # Connect to Server 
            IRCSOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            IRCSOCKET.connect((HOST,PORT))
            # Connect to Channel
            sendMsg("USER " + botNick + " " + botNick + " " + botNick + ": Connecting to server\n")
            sendMsg("NICK " + botNick + "\n")
            sendMsg("JOIN " + CHANNEL + "\n")
            return True
        except:
            print("ERROR: " + str(botNick) + " unable to join channel.")
            return False 
        

    # Bot communicates with Controller
    def sendPrivate(self, msg):
        global HOST, PORT, CHANNEL, IRCSOCKET
        privMsg = "PRIVMSG " + CHANNEL + " :" + msg + "\n"
        IRCSOCKET.send(privMsg.encode())

    # Bot listens for commands from IRC
    def getCommand(self, command):

        # Parse commands

        if command == "status":
            self.botStatus()
        elif command == "attack":
            self.botAttack()
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
            self.botQuit() 
        elif command == "shutdown":
            self.otShutdown()

    # Do pingPong protocol
    def pingPong(self):
        # Send PONG
        self.sendMsg('PONG')


    # DO COMMAND ACTIONS HERE ------------------------------------------------------

    # Send Stats (Just the name of bot)
    def botStatus(self):
        global botNick
        sendPrivate("My name is: " + str(botNick))

    # Attack Server
    def botAttack(self):
        global conNick, botNick, attackCount 
        try:
            attackCount = attackCount + 1 
            # Send private message that attack was successful
        except:
            pass 
            # Send private message that attack failed 


    # Move Server
    def botMove(self, newHost, newPort, newChannel):
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
    def botQuit(self):
        global CONSTATUS 
        CONSTATUS = False 
        print("Controller has gone offline ")

    # Shutdown 
    # I think the bot completely gets killed here?
    def botShutdown(self):
        global SHUTDOWN, botNick
        SHUTDOWN == True
        print("Bot: " + botNick + " is shutting down")
        sys.exit()
        return

    # Main Handler Loop
    def handler(self):

        # Connect to IRC Server 
        if self.CONSTATUS == False:
            self.joinChannel()

        # Receive Data here 

        # Parse Data 

        # If data startswith PING, send PONG
        self.pingPong()

        # Keep sending pingPong every 5-10 seconds
        # Not sure if it stays here or outside handler
        time.sleep(10)

        # elif check if data is a command
        self.getCommand(data)

        # else just pass 


    """
    WE WILL TEST THIS BOT IN KIWIIRC 
    WE MAKE OUR OWN CHANNELS N STUFF
    """

# Main Start
bot = Bot()
if __name__ == "__main__":

    # Get args here
    global HOST, PORT, CHANNEL, PHRASE, SHUTDOWN

    if len(sys.argv) != 5:
        print("Wrong number of inputs")
        sys.exit()

    HOST = sys.argv[1]
    PORT = sys.argv[2]
    CHANNEL = sys.argv[3]
    PHRASE = sys.argv[4]

    # Check for valid port
    if not PORT.isdigit():
        print("Invalid port")
        sys.exit()

    # Attempt connection if bot is not currently online
    if not BOTONLINE:
        preCheck = bot.joinChannel(HOST, PORT, CHANNEL, PHRASE)

        # Terminate if unable to initially join
        if not preCheck:
            sys.exit()
    
    # Run the Bot forever until close
    while not SHUTDOWN:
        bot.handler()

  


