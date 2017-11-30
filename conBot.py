import time
import socket 
import sys 

# Get response from Bot 
def getResponse():
    try:
        # Get response from bot
        msg = ircSocket.recv(1024).decode('utf-8')

# COMMANDS
def botStatus():
    sendCommand("status")

def botAttack(host, port, channel):
    pass

def botMove(host, port, channel):
    pass 

def botQuit():
    pass 

def botShutdown(): 
    pass

def sendCommand(msg):
    pass 

# CONNECT TO IRC SERVER CHANNEL
# This next line goes to a function
# ircSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def serverConnect(ircSocket, host, port):
    try:
        ircSocket.connect((host,port))
        print("Connection successful")
        return True
    except:
        print("Connection failed")
        return False 



if __name == "__main__":

    # Get sys.argv

    # Keep connection to IRC server 