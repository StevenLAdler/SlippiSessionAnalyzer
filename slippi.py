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
        self.__GAME_LIST = []
        self.__ALL_PLAYERS = []
        
    def setGame(self, slp):
        self.__GAME = Game(slp)
        self.__PLAYERS.clear()
        

    def buildPlayersList(self):
        for player in self.__GAME.metadata.players:
            if player == None or player.netplay == None:
                continue
            self.__PLAYERS.append(player.netplay.name)
            if player.netplay.name not in self.__ALL_PLAYERS:
                self.__ALL_PLAYERS.append(player.netplay.name)
        if len(self.__PLAYERS)!=2:
            return False
        else:
            return True
            
    def determineWinner(self):
        last_frame = self.__GAME.frames[-1]
        lframe_data = []
        
        for port in last_frame.ports:
            if port == None:
                continue        
            lframe_data.append({'stocks': port.leader.post.stocks,
                         'damage': port.leader.post.damage})
                    
        if lframe_data[0]['stocks']>lframe_data[1]['stocks']:
            winner = self.__PLAYERS[0]
            loser = self.__PLAYERS[1]
            
        elif lframe_data[0]['stocks']<lframe_data[1]['stocks']:
            winner = self.__PLAYERS[1]
            loser = self.__PLAYERS[0]
            
        elif lframe_data[0]['damage']<lframe_data[1]['damage']:
            winner = self.__PLAYERS[0]
            loser = self.__PLAYERS[1]
            
        elif lframe_data[0]['damage']>lframe_data[1]['damage']:
            winner = self.__PLAYERS[1]
            loser = self.__PLAYERS[0]
            
        else: #tie?
            return
        
        self.__GAME_LIST.append({winner: 1,
                                 loser: 0})
      

    def playerList(self):
        return self.__ALL_PLAYERS
    
    def getWins(self, p1, p2):
        p1_cnt = 0
        p2_cnt = 0
        for game in self.__GAME_LIST :
            if set([p1, p2]).issubset(list(game.keys())):
                p1_cnt += game[p1]
                p2_cnt += game[p2]
        print(f"{p1}: {p1_cnt} win(s)\n{p2}: {p2_cnt} win(s)")
  
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
  
plist = slip.playerList()  
if len(plist) == 2:
    slip.getWins(plist[0], plist[1])
elif len(plist) > 2:
    [print(f"{plist.index(name)}: {name}, ", end='') for name in plist[1:]]
    sel = input("select the two players you want to see the session W/L for (ex. '1 2')\n")
    sel = sel.split(' ')
    slip.getWins(plist[int(sel[0])], plist[int(sel[1])])
    