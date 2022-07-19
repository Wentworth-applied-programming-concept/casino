from peewee import *
import argparse
import sys
import json


db = SqliteDatabase('src/core/casino.db')


class Player(Model):
    userID = CharField(unique=True)
    firstName = CharField()
    lastName = CharField()
    password = CharField()
    winnings = FloatField(null=True)
    banned = BooleanField(null=True)
    admin = BooleanField()

    class Meta:
        database = db

class game(Model):
    gameID = IntegerField(unique=True) #unique ID of each game
    gameType = CharField() #unique ID of each game
    userID = CharField() #user who played game
    winnings = FloatField(null=True)
    timeStamp = DateField(null=True)

    class Meta:
        database = db

class casino(Model): #table to keep track of total casino and per game winnings
    entryName = CharField(unique=True) #unique ID of each game type
    winnings = FloatField() #total winnings of game
    difficulty = FloatField(null=True) #optional field, saved difficulty of game


    class Meta:
        database = db


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Create databases or delete databases.")
    parser.add_argument('mode', type=str,
                        help='flag, if c then create database tables if d delete')


    args = parser.parse_args(sys.argv[1:])
    db.connect()

    if args.mode == 'c':
        db.create_tables([Player, game, casino])
        Player.create(userID='admin', firstName='default',
            lastName='default', password='admin', admin=True)
        Player.create(userID='bobby123', firstName='Bob',
            lastName='Dylan', password='admin', winnings=0, admin=False)
        Player.create(userID='harry4959', firstName='Harry',
            lastName='Dad', password='admin', winnings=0, admin=False)
        
        casino.create(entryName="casino", winnings=0.0, difficulty=1) #create casino tracker

        with open('src/games/games.json') as data: #create entry for each game
            gameList = json.load(data)
            for game in gameList['games']:
                casino.create(entryName=game, winnings=0.0, difficulty=1)

    elif args.mode == 'd':
        db.drop_tables([Player, game, casino])
    else:
        print("No Args specified. Try again.")
