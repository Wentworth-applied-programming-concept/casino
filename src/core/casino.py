from src.core.database import Player, PlayerControl

class user:
    def __init__(self, firstName, lastName, idNum):
        self.firstName = firstName
        self.lastName = lastName
        self.uid = idNum
    
    def setFirstName(self, name):
        '''function to return set first name'''
        self.firstName = name

    def setLastName(self, name):
        '''function to return set last name'''
        self.lastName = name
    
    def setId(self, idNum):
        '''function to return set uid'''
        self.uid = idNum
    
    def getFirstName(self):
        '''function to return first name'''
        return self.firstName

    def getLastName(self):
        '''function to return last name'''
        return self.lastName

    def getId(self):
        '''function to return uid'''
        return self.uid

class player(user):    
    def checkLogin(self, uid, password):
        return PlayerControl.checkLogin(uid, password)

    def checkWinnings(self, uid):
        return PlayerControl.getWinnings()

class admin(user):
    def checkLogin(self, uid, password):
        return PlayerControl.checkLogin(uid, password)

    def addWinnings(self, uid, winnings):
        PlayerControl.addWinings(uid, winnings)

    def checkWinnings(self, uid):
        return PlayerControl.getWinnings()

    def addPlayer(self, uid, firstName, lastName):
        PlayerControl.createPlayer(uid, firstName, lastName)
    
    def removeUser(self, uid):
        return "Function called successfully"
