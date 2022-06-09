from src.core.database import *
from datetime import datetime
import importlib

class user:
    def __init__(self):
        pass

    def getWinnings(self, uid):
        user = Player.select().where(Player.userID == uid).get()
        return user.winnings

    def checkLogin(self, uid, password):
        '''check user login'''
        try:
            user = Player.select().where(Player.userID == uid).get()
            if user.password == password:
                return True
            else:
                return False
        except Exception as e:
            return False

class player(user):
    '''class for player level functions'''
    pass

class admin(user):
    '''class to hold admin level functions'''
    def checkAdmin(self, uid, password):
        '''check if a user is an admin'''
        try:
            user = Player.select().where(Player.userID == uid).get()
            if user.password == password:
                if user.admin:
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            return False

    def addWinnings(self, uid, winnings):
        '''add a negative value to decreate winnings, add a positive value to increate winnings'''
        user = Player.select().where(Player.userID == uid).get()
        if(user.winnings == None):
            user.winnings = (winnings)
        else:
            user.winnings = (user.winnings + winnings)

        user.save()

    def createPlayer(self, uid, fName, lName, pword):
        Player.create(userID=uid, firstName=fName,
                      lastName=lName, password=pword)

    def removePlayer(self, uid):
        Player.delete().where(Player.userID == uid)

    def addGame(self, gameName, uid, win):
        try:
            gid = eval(f'{gameName}').select(fn.MAX(eval(f'{gameName}').gameID)).scalar() + 1 #set GID to be highest GID + 1
        except Exception as e:
            gid = 0
        
        print(gid)

        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        eval(f'{gameName}').create(gameID=gid,userID=uid, winnings=win, timeStamp=time)

    def removeGame(self, gameName, gid):
        importlib.import_module(gameName)
        self.game = eval(f'{gameName}()')
        self.game.delete().where(self.game.gameID == gid)
