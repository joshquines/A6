import time
import socket 
import sys 
import threading

class Bot:
    
    def setup(self, host, port, channel, phrase):
        self.HOST = host
        self.PORT = int(port)
        self.CHANNEL = channel
        self.PHRASE = phrase
        self.IRCSOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # CONTROLLER INFO
        self.botNick = "SLAVE778"
        self.liveConnection = False # Flag to see if controller connection to IRC Server is active
        self.command = None

        # BOT INFO
        self.botList = []
        self.botsSuccessful = []
        self.botsFailed = []
        self.botsMoved = []
        self.botsDisconnected = []
        self.acceptedCons = []

        self.connectLoop()


        

    def IRCconnect(self):
        self.sendData("NICK {}\n" .format(self.botNick))
        self.sendData("USER bot * * :{}\n" .format(self.botNick))
        self.sendData("JOIN #{}\n" .format(self.CHANNEL))
        resp = self.getData()
        print(resp)
        return "433" in resp

    def connectLoop(self):
        while not self.liveConnection:
            try:
                self.IRCSOCKET.connect((self.HOST, self.PORT))
                self.liveConnection = True
            except Exception as e:
                print("{} Trying to reconnect..." .format(e))
                time.sleep(5)
                continue

    # Get response from Bot 
    def getData(self):
        return self.IRCSOCKET.recv(2048).decode().strip('\n\r')

    def sendData(self, msg):
        self.IRCSOCKET.send(msg.encode())

    def privateMsg(self, receiver, msg):
        self.sendData("PRIVMSG {} :{}\n" .format(receiver, msg))

    def handleResponse(self, prefix, message):
        if message == self.PHRASE:
            self.acceptedCons.append(prefix)
        if prefix in self.acceptedCons:
            print("from " + prefix + " to do " + message)
            if message == "status":
                print("sending back status")
                self.privateMsg(prefix, "Correct pass - " + self.botNick)
            if message == "shutdown":
                print("shutting down")
                self.privateMsg(prefix, "Shutdown successful - " + self.botNick)
                self.IRCSOCKET.close()
                sys.exit(0)
                    

        

    def reader(self):
        try:
            while True:
                response = self.getData()
                print(response)   
                if(response != ""):                                         
                        if response.find("PRIVMSG") != -1:                           
                            name = response.split('!',1)[0][1:]
                            message = response.split('PRIVMSG',1)[1].split(':',1)[1]
                            print("message from " + name + ": " + message)   
                            self.handleResponse(name, message)                               
                        elif response.find("PING") != -1:
                            self.sendData("PONG {}: :\r\n".format(self.HOST))                                                                          
                        elif response.find('433') != -1:
                            self.createNick(self.NICK)
                            self.connectIRC(self.s,self.NICK, self.chan)  
        except Exception as e:
            while not self.liveConnection:
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

        print("setting up bot")
        bot.setup(HOST, PORT, CHANNEL, PHRASE)


        print("bot set up")
        print("connecting")
        while noConnection:
            noConnection = bot.IRCconnect()
        
        print("Controller is running. Connected with nick: " + bot.botNick)

        bot.reader()



if __name__ == "__main__":
    main()


