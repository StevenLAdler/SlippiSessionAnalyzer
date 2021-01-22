from slippi import Game
import os, datetime, pathlib, argparse

parser = argparse.ArgumentParser()
parser.add_argument('date', type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'))
parser.add_argument('-d', dest='dir', help='(string)', type=str)
args = parser.parse_args()
date = args.date.date()

class SlippiWinLoss:
    def __init__(self):
        self.__GAME = None
        self.__PLAYERS = []
        self.__WINS = {}
        
    def setGame(self, slp):
        self.__GAME = Game(slp)
        self.__PLAYERS.clear()
        

    def buildPlayersList(self):
        for player in self.__GAME.metadata.players:
            if player == None or player.netplay == None:
                continue
            self.__PLAYERS.append(player.netplay.name)
        if len(self.__PLAYERS)!=2:
            return False
        else:
            return True
            
    def determineWinner(self):
        last_frame = self.__GAME.frames[-1]
        port_num = -1
        for port in last_frame.ports:
            if port == None:
                continue
            port_num+=1
            if "DEAD" not in str(port.leader.post.flags):
                winner = self.__PLAYERS[port_num]
                if winner not in self.__WINS:
                    self.__WINS[winner] = 1
                else:
                    self.__WINS[winner]+=1
    
    def getWins(self):
        return self.__WINS
  
slip = SlippiWinLoss()

for entry in os.scandir(args.dir):
    if (entry.path.endswith(".slp")):
        fname = pathlib.Path(entry.path)
        mtime = datetime.date.fromtimestamp(fname.stat().st_mtime)
        if mtime != date:
            continue
        slippi = entry.path
        slip.setGame(slippi)
        if not slip.buildPlayersList():
            continue            
        slip.determineWinner()
        
print(slip.getWins())



