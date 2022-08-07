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
        '''update player, set any vals that should not be changed to null'''
        try:
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
            return True
        except Exception as e:
            return False

    def getNameFromUID(self, uid):
        try:
            player = Player.select().where(Player.userID == uid).get()
            return player.firstName + ' ' + player.lastName
        except Exception as e:
            return None

    def createPlayer(self, uid, fName, lName, pword, bal):
        try:
            Player.create(userID=uid, firstName=fName, lastName=lName, password=pword, winnings=bal, admin=False)
            return True
        except Exception as e:
            return False
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
        try:
            Player.create(userID=uid, firstName=fName, lastName=lName, password=pword, admin=True)
            return True
        except Exception as e:
            return False

    def updateAdminInfo(self, idVal, uid='', fName='', lName='', pwd=''):
        '''update admin, set any vals that should not be changed to null'''
        try:
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
            return True
        except Exception as e:
            return False

    def addGame(self, gameName, uid, cost, win, datePlayed=None):
        try:
            try:
                gid = game.select(fn.Max(game.gameID)).scalar() + 1
            except Exception as e:
                gid = 0
            
            if datePlayed == None:
                time = datetime.now().strftime("%Y-%m-%d")
            else:
                time = datePlayed
                
            game.create(gameID = gid, gameType=gameName, userID=uid, winnings=win, timeStamp=time)

            user = Player.select().where(Player.userID == uid).get()
            if(user.winnings == None):
                user.winnings = (win - cost)
            else:
                user.winnings = (user.winnings + (win - cost))
            user.save()

            #update total casino and per game winnings
            gameTotal = casino.select().where(casino.entryName == gameName).get()
            gameTotal.winnings = gameTotal.winnings + cost - win
            gameTotal.save()

            casinoTotal = casino.select().where(casino.entryName == "casino").get()
            casinoTotal.winnings = casinoTotal.winnings + cost - win
            casinoTotal.save()

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

    def checkPlayerBalance(self, uid):
        user = Player.select().where(Player.userID == uid).get()
        return user.winnings
    
    def checkIfEnough(self, uid, cost): #function to check if player has enough money to play
        user = Player.select().where(Player.userID == uid).get()
        if user.winnings >= cost:
            return True
        else:
            return False
    
    def generateGraphData(self, uid = "", gameName = "", startTime = "", endTime = ""):
        try:
            if uid != "":
                if gameName != "":
                    if startTime != "" and endTime != "":
                        return game.select().where(game.userID == uid).where(game.gameType == gameName).where(game.timeStamp < endTime).where(game.timeStamp > startTime)
                    else:
                        return game.select().where(game.userID == uid).where(game.gameType == gameName)
                else:
                    if startTime != "" and endTime != "":
                        return game.select().where(game.userID == uid).where(game.timeStamp < endTime).where(game.timeStamp > startTime)
                    else:
                        return game.select().where(game.userID == uid)
            else:
                if gameName != "":
                    if startTime != "" and endTime != "":
                        return game.select().where(game.gameType == gameName).where(game.timeStamp < endTime).where(game.timeStamp > startTime)
                    else:
                        return game.select().where(game.gameType == gameName)
                else:
                    if startTime != "" and endTime != "":
                        return game.select().where(game.timeStamp < endTime).where(game.timeStamp > startTime)
                    else:
                        return game.select()

        except Exception as e:
            print("Error: ", e)
            return None

    def searchForGame(self, dataType, entry, uid = None): #function to search for a game by game type, user id, or time stamp
        try:
            if dataType == "gameType" and uid == None: #admin search options, no uid provided
                return game.select().where(game.gameType == entry)
            elif dataType == "winnings" and uid == None:
                return game.select().where(game.winnings == entry)
            elif dataType == "timeStamp" and uid == None:
                return game.select().where(game.timeStamp == entry)
            elif dataType == "userID":
                return game.select().where(game.userID == entry)
            elif dataType == "gameID":
                return game.select().where(game.gameID == entry)

            elif dataType == "gameType": #user search options when uid is not None
                return game.select().where(game.gameType == entry).where(game.userID == uid)
            elif dataType == "winnings":
                return game.select().where(game.winnings == entry).where(game.userID == uid)
            elif dataType == "timeStamp":
                return game.select().where(game.timeStamp == entry).where(game.userID == uid)
            else:
                return None
        except Exception as e:
            print("Error: ", e)
            return None

    def searchForAdmin(self, dataType, entry):
        try:
            if dataType == "userID":
                return Player.select().where(Player.userID == entry).where(Player.admin == True)
            elif dataType == "firstName":
                return Player.select().where(Player.firstName == entry).where(Player.admin == True)
            elif dataType == "lastName":
                return Player.select().where(Player.lastName == entry).where(Player.admin == True)
        except Exception as e:
            pass

    def searchForPlayer(self, dataType, entry):
        try:
            if dataType == "userID":
                return Player.select().where(Player.userID == entry).where(Player.admin == False)
            elif dataType == "firstName":
                return Player.select().where(Player.firstName == entry).where(Player.admin == False)
            elif dataType == "lastName":
                return Player.select().where(Player.lastName == entry).where(Player.admin == False)
            elif dataType == "winnings":
                return Player.select().where(Player.winnings == entry).where(Player.admin == False)
        except Exception as e:
            pass

    def setGameDifficulty(self, game, diff):
        try:
            if diff <= 5:
                gameTracker = casino.select().where(casino.entryName == game).get()
                gameTracker.difficulty = diff
                gameTracker.save()
                return True
            else:
                return False
        except Exception as e:
            return False

    def getGameDifficulty(self, game):
        return casino.select().where(casino.entryName == game).get().difficulty

    def checkCasinoWinnings(self):
        return casino.select().where(casino.entryName == "casino").get().winnings
    
    def checkGameWinnings(self, game):
        return casino.select().where(casino.entryName == game).get().winnings