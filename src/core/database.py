from numpy import False_
from peewee import *
import argparse
import sys

db = SqliteDatabase('casino.db')

class Player(Model):
    userID = IntegerField()
    firstName = CharField()
    lastName = CharField()
    winnings = FloatField(null=True)
    banned = BooleanField(null=True)
    class Meta:
        database = db

class PlayerControl():
    '''control player database'''    
    def createPlayer(self, uid, fName, lName):
        Player.create(userID = uid, firstName = fName, lastName = lName).execute()

    def removePlayer(self, uid):
        Player.delete().where(Player.userID == uid).execute()

    def getWinnings(self, uid):
        user = Player.select().where(Player.userID == uid).get()
        return user.winnings

    def addWinings(self, uid, winnings):
        '''add a negative value to decreate winnings, add a positive value to increate winnings'''
        user = Player.select().where(Player.userID == uid).get()
        if(user.winnings == None):
            Player.update(winnings=(winnings).where(Player.userID == uid)).execute()
        else:
            Player.update(winnings=(user.winnings + winnings).where(Player.userID == uid)).execute()

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Create databases or delete databases.")
    parser.add_argument('createTables', type=bool, help='bool flag, if true then create database tables', default=False)
    parser.add_argument('dropTables', type=bool, help='bool flag, if true then drop database tables', default=False)

    args = parser.parse_args(sys.argv[1:])

    if args.createTables == True:
        Player.create_table()
    elif args.dropTables == True:
        Player.drop_table()
    else:
        print("No Args specified. Try again.")
