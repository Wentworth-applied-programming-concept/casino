from src.core.casino import player, admin

import random

class slots:
    def __init__(self, uid):
        self.player = player()
        self.admin = admin()
        self.uid = userID

        run = True

        while run:
            userInput = input("Would you like to play (y/n): ")

            if userInput == 'y':
                self.admin.addWinnings(self.uid, -100)
                money = self.playGame()
                self.admin.addWinnings(self.uid, money)
                self.admin.addGame('Slots', self.uid, money)
                print(f"You earned: {money}, your balance is now {self.player.getWinnings(self.uid)}")
            else:
                run = False
    
    def playGame(self):
        roll1 = random.randint(0, 10) 
        roll2 = random.randint(0, 10) 
        roll3 = random.randint(0, 10) 

        if roll1 == roll2 == roll3:
            return 5000
        else:
            return 0

if __name__ == '__main__':
    slots()
