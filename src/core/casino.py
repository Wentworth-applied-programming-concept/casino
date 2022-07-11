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
    def getPlayers(self):
        '''return player info as dict, excludes admins'''
        try:
            players = Player.select().where(Player.admin == False)
            return players
        except Exception as e:
            return None

    def updateInfo(self, idVal, uid='', fName='', lName='', pwd='', balance=''):
        '''update STUDENT, set any vals that should not be changed to null'''
        usr = Player.select().where(Player.userID == idVal).get()
        if fName != '':
            usr.firstName = fName
        if lName != '':
            usr.lastName = lName
        if uid != '':
            usr.userID = uid
        if pwd != '':
            usr.password = pwd
        if balance != '':
            usr.winnings = balance

        usr.save()

    def getNameFromUID(self, uid):
        try:
            player = Player.select().where(Player.userID == uid).get()
            return player.firstName + ' ' + player.lastName
        except Exception as e:
            return None

    def createPlayer(self, uid, fName, lName, pword, bal):
        Player.create(userID=uid, firstName=fName, lastName=lName, password=pword, winnings=bal, admin=False)

    def removePlayer(self, uid):
        Player.delete().where(Player.userID == uid).execute()


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

    def getAdmins(self):
        '''return admins as dict'''
        try:
            players = Player.select().where(Player.admin == True)
            return players
        except Exception as e:
            return None

    def createAdmin(self, uid, fName, lName, pword):
        Player.create(userID=uid, firstName=fName, lastName=lName, password=pword, admin=True)

    def updateAdminInfo(self, idVal, uid='', fName='', lName='', pwd=''):
        '''update STUDENT, set any vals that should not be changed to null'''
        usr = Player.select().where(Player.userID == idVal).get()
        if fName != '':
            usr.firstName = fName
        if lName != '':
            usr.lastName = lName
        if uid != '':
            usr.userID = uid
        if pwd != '':
            usr.password = pwd

        usr.save()

    def addWinnings(self, uid, winnings):
        '''add a negative value to decreate winnings, add a positive value to increate winnings'''
        user = Player.select().where(Player.userID == uid).get()
        if(user.winnings == None):
            user.winnings = (winnings)
        else:
            user.winnings = (user.winnings + winnings)

        user.save()

    def addGame(self, gameName, uid, win):
        try:
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            game.create(gameType=gameName, userID=uid, winnings=win, timeStamp=time)
        except Exception as e:
            print("Error: ", e)

    def getGameHistory(self):
        return game.select()

    def getGameByName(self, gameName):
        return game.select().where(game.gameType == gameName)

    def getGameByPlayer(self, uid):
        return game.select().where(game.userID == uid)

    def removeGame(self, gameName, gid):
        game.delete().where(game.gameType == gameName).where(game.id == gid).execute()