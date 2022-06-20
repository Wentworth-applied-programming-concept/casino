from peewee import *
import argparse
import sys

db = SqliteDatabase('src/core/casino.db')


class Player(Model):
    userID = CharField(unique=True)
    firstName = CharField()
    lastName = CharField()
    password = CharField()
    winnings = FloatField(null=True)
    banned = BooleanField(null=True)
    admin = BooleanField(null=True)

    class Meta:
        database = db


class gameModel(Model):
    gameID = IntegerField(unique=True) #unique ID of each game
    userID = CharField() #user who played game
    winnings = FloatField(null=True)
    timeStamp = DateField(null=True)

    class Meta:
        database = db

class Slots(gameModel):
    '''One of these needs to be added for every game, additionally the table needs to be added in main below'''
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Create databases or delete databases.")
    parser.add_argument('mode', type=str,
                        help='flag, if c then create database tables if d delete')


    args = parser.parse_args(sys.argv[1:])
    db.connect()

    if args.mode == 'c':
        db.create_tables([Player, Slots])
        Player.create(userID='admin', firstName='default',
            lastName='default', password='admin', admin=True)
    elif args.mode == 'd':
        db.drop_tables([Player, Slots])
    else:
        print("No Args specified. Try again.")

import argparse