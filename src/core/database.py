from peewee import *
import argparse
import sys

db = SqliteDatabase('casino.db')

class Player(Model):
    userID = IntegerField()
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
        Player.create(userID = uid, firstName = fName, lastName = lName, password = pword)

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
            user.winnings=(user.winnings + winnings)

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Create databases or delete databases.")
    parser.add_argument('createTables', type=bool, help='bool flag, if true then create database tables', default=False)
    parser.add_argument('dropTables', type=bool, help='bool flag, if true then drop database tables', default=False)

    args = parser.parse_args(sys.argv[1:])

    if args.createTables == True:
        Player.create_table()
        default = PlayerControl()
        default.createPlayer('admin', 'default', 'default', 'admin')
    elif args.dropTables == True:
        Player.drop_table()
    else:
        print("No Args specified. Try again.")
