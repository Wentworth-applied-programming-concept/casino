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
    admin = BooleanField()

    class Meta:
        database = db

class game(Model):
    gameType = CharField() #unique ID of each game
    userID = CharField() #user who played game
    winnings = FloatField(null=True)
    timeStamp = DateField(null=True)

    class Meta:
        database = db

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Create databases or delete databases.")
    parser.add_argument('mode', type=str,
                        help='flag, if c then create database tables if d delete')


    args = parser.parse_args(sys.argv[1:])
    db.connect()

    if args.mode == 'c':
        db.create_tables([Player, game])
        Player.create(userID='admin', firstName='default',
            lastName='default', password='admin', admin=True)
        Player.create(userID='bobby123', firstName='Bob',
            lastName='Dylan', password='admin', winnings=0, admin=False)
        Player.create(userID='harry4959', firstName='Harry',
            lastName='Dad', password='admin', winnings=0, admin=False)
    elif args.mode == 'd':
        db.drop_tables([Player, game])
    else:
        print("No Args specified. Try again.")
