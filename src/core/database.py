from peewee import *
import argparse
import sys
from datetime import datetime

db = SqliteDatabase('src/core/casino.db')


class Player(Model):
    userID = IntegerField(unique=True)
    firstName = CharField()
    lastName = CharField()
    password = CharField()
    winnings = FloatField(null=True)
    banned = BooleanField(null=True)
    admin = BooleanField(null=True)

    class Meta:
        database = db


class PlayerControl():
    '''control player database'''

    def createPlayer(self, uid, fName, lName, pword):
        Player.create(userID=uid, firstName=fName,
                      lastName=lName, password=pword)

    def removePlayer(self, uid):
        Player.delete().where(Player.userID == uid)

    def getWinnings(self, uid):
        user = Player.select().where(Player.userID == uid).get()
        return user.winnings

    def addWinnings(self, uid, winnings):
        '''add a negative value to decreate winnings, add a positive value to increate winnings'''
        user = Player.select().where(Player.userID == uid).get()
        if(user.winnings == None):
            user.winnings = (winnings)
        else:
            user.winnings = (user.winnings + winnings)

        user.save()

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


class gameModel(Model):
    gameID = IntegerField(unique=True) #unique ID of each game
    userID = IntegerField() #user who played game
    winnings = FloatField(null=True)
    timeStamp = DateField(null=True)

    class Meta:
        database = db


class gameController():
    def __init__(self, gameName):
        self.game = eval(f'{gameName}()')

    def addGame(self, gid, uid, win, time):
        newGame = self.game.select().where(self.game.userID == uid).get()
        newGame.gameID = gid
        newGame.uid = uid
        newGame.timeStamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        newGame.winnings = win

        newGame.save()

    def removeGame(self, gid):
        self.game.delete().where(self.game.gameID == gid)


class Slots(gameModel):
    '''One of these needs to be added for every game, additionally the table needs to be added in main below'''
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Create databases or delete databases.")
    parser.add_argument('createTables', type=bool,
                        help='bool flag, if true then create database tables', default=False)
    parser.add_argument('dropTables', type=bool,
                        help='bool flag, if true then drop database tables', default=False)

    args = parser.parse_args(sys.argv[1:])
    db.connect()

    if args.createTables == True:
        db.create_table([Player, Slots])
        default = PlayerControl()
        default.createPlayer('admin', 'default', 'default', 'admin') #create a default user admin/admin
    elif args.dropTables == True:
        db.drop_table([Player, Slots])
    else:
        print("No Args specified. Try again.")
