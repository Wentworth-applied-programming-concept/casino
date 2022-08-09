#simulation.py is used to create random database information for testing purposes.
from src.core.database import *
from datetime import datetime
from faker import Faker
from src.core.casino import admin


import random
class simulation:
    def __init__(self, dp):
        self.administrator = admin()


        self.faker = Faker()
        self.datapoints = dp
        self.uids = ["bobby123", "harry4959", "jimmy612", "hanky213", "kevin12", "ericrox", "chrisGNU", "joe", "andrewww", "tessac"]
        self.firstNames = ["Bob", "Harry", "Jimmy", "Hank", "Kevin", "Eric", "Chris", "Joe", "Andrew", "Tessa"]
        self.lastNames = ["Dylan", "Oliver", "Moreno", "Pham", "Huang", "Savage", "Gnome", "Walsh", "Jones", "Rose"]
        self.passwords = ["default", "default", "default", "default", "default", "default", "default", "default", "default", "default"]
        self.games = []
        with open('src/games/games.json') as data: #create entry for each game
            gameList = json.load(data)
            for game in gameList['games']:
                self.games.append(game)
                
        self.create_players()
        self.generate_games()

    def create_players(self): #function to create players
        for count, idVal in enumerate(self.uids):
            Player.create(userID=idVal, firstName=self.firstNames[count], lastName=self.lastNames[count], password=self.passwords[count], winnings=5000, admin=False)

    def generate_games(self):
        for points in range(0, self.datapoints):
            gameType = random.randint(0, len(self.games)-1)
            user = random.randint(0, len(self.uids)-1)
            dateVal = self.faker.date_between_dates(date_start=datetime(2022,5,1), date_end=datetime(2022,8,25))
            won = random.randint(0,15)
            if won == 0:
                winnings = 1000
            else:
                winnings = 0
            self.administrator.addGame(self.games[gameType], self.uids[user], 100, winnings, datePlayed=dateVal)

if __name__=='__main__':
    sim = simulation(100) #change this to change the number of games to be generated
