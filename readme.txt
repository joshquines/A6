CPSC 526 Assignment	#6
Steven Leong 10129668 T01	
Josh Quines	10138118 T03	

How to Run:

bot.py 
python3 bot.py <HOST> <PORT> <CHANNEL> <PHRASE>

conBot.py 
python3 conBot.py <HOST> <PORT> <CHANNEL> <PHRASE>

conBot commands:
    Status: 
    Get status of bots. How many are connected and their names
    Usage: status
    
    Attack: 
    Attack a server. Send botName + number of attacks 
    Usage: attack <hostname> <port> 

    Move:
    Move to a new IRC server/channel 
    Usage: move <hostname> <port> <channel>

    Quit:
    Only conBot quits. Bots still stay online 
    Usage: quit 

    Shutdown:
    Kill all bots 
    Usage: shutdown
