import PodSixNet.Channel
import PodSixNet.Server
import random
from time import sleep
colors = ["Black","White"]
class ClientChannel(PodSixNet.Channel.Channel):
    def Network(self, data):
        print data
    def Network_receive(self, data):
        #deconsolidate all of the data from the dictionary     
        #horizontal or vertical?
        #x of placed line
        x = data["x"]     
        #y of placed line
        y = data["y"]     
        #player number (1 or 0)
        num=data["num"]     
        #id of game given by server at start of game
        self.gameid = data["gameid"]
        #tells server to place line
        self._server.placeLine(x, y, data, self.gameid, num)
    def Close(self):
        self._server.close(self.gameid)
class BoxesServer(PodSixNet.Server.Server):
 
    channelClass = ClientChannel
    def __init__(self, *args, **kwargs):
        PodSixNet.Server.Server.__init__(self, *args, **kwargs)
        self.games = []
        self.queue = None
        self.currentIndex=0
    def Connected(self, channel, addr):
        print 'new connection:', channel
        color_0,color_1 = 0,0
        color_0= random.randint(0,1)
        color_1 = 1-color_0
        if self.queue==None:
            self.currentIndex+=1
            channel.gameid=self.currentIndex
            self.queue=Game(channel, self.currentIndex)
        else:
            channel.gameid=self.currentIndex
            self.queue.player1=channel
            self.queue.player0.Send({"action": "startgame","player":0, "gameid": self.queue.gameid,"cindex":color_0})
            self.queue.player1.Send({"action": "startgame","player":1, "gameid": self.queue.gameid,"cindex":1-color_0})
            self.games.append(self.queue)
            self.queue=None
    def placeLine(self, x, y, data, gameid, num):
        game = [a for a in self.games if a.gameid==gameid]
        if len(game)==1:
            game[0].placeLine(x, y, data, num)
    def close(self, gameid):
        try:
            game = [a for a in self.games if a.gameid==gameid][0]
            game.player0.Send({"action":"close"})
            game.player1.Send({"action":"close"})
        except:
            pass
    def tick(self):
        # Check for any wins
        # Loop through all of the squares
        index=0
        change=3
        for game in self.games:
            change=3
            for time in range(2):
                for y in range(6):
                    for x in range(6):
                        if game.boardh[y][x] and game.boardv[y][x] and game.boardh[y+1][x] and game.boardv[y][x+1] and not game.owner[x][y]:
                            if self.games[index].turn==0:
                                self.games[index].owner[x][y]=2
                                game.player1.Send({"action":"win", "x":x, "y":y})
                                game.player0.Send({"action":"lose", "x":x, "y":y})
                                change=1
                            else:
                                self.games[index].owner[x][y]=1
                                game.player0.Send({"action":"win", "x":x, "y":y})
                                game.player1.Send({"action":"lose", "x":x, "y":y})
                                change=0
            self.games[index].turn = change if change!=3 else self.games[index].turn
            game.player1.Send({"action":"yourturn", "torf":True if self.games[index].turn==1 else False})
            game.player0.Send({"action":"yourturn", "torf":True if self.games[index].turn==0 else False})
            index+=1
        self.Pump()
class Game:
    def __init__(self, player0, currentIndex):
        # whose turn (1 or 0)
        self.turn = 0
        #owner map
        self.owner=[[False for x in range(6)] for y in range(6)]
        # Seven lines in each direction to make a six by six grid.
        self.boardh = [[False for x in range(6)] for y in range(7)]
        self.boardv = [[False for x in range(7)] for y in range(6)]
        #initialize the players including the one who started the game
        self.player0=player0
        self.player1=None
        #gameid of game
        self.gameid=currentIndex
    def placeLine(self,x, y, data, num):
		if num == 0:
			self.player1.Send({"action":"theirturn","x_2":x,"y_2":y})
		else:	
			self.player0.Send({"action":"theirturn","x_2":x,"y_2":y})	
print "STARTING SERVER ON LOCALHOST"
# try:
address=raw_input("Host:Port (localhost:8000): ")
if not address:
    host, port="localhost", 8000
else:
    host,port=address.split(":")
boxesServe = BoxesServer(localaddr=(host, int(port)))
while True:
    boxesServe.tick()
    sleep(0.01)
