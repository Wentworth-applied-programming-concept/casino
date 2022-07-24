from src.core.casino import player, admin
from src.ui.ui import player as ui

import random

class slots:
    def __init__(self, uid, difficulty):
        self.player = player()
        self.admin = admin()
        self.uid = uid
        self.difficulty = difficulty

        run = True

        while run:
            userInput = input("Would you like to play (y/n): ")

            if userInput == 'y':
                play = self.admin.checkIfEnough(self.uid, 100) #check if player has enought to bet
                if play == True:
                    money = self.playGame()
                    self.admin.addGame('slots', self.uid, 100, money)
                    print(f"You earned: {money}, your balance is now {self.player.getWinnings(self.uid)}")
                else:
                    print("You do not have enough to play")
            else:
                run = False
        ui(self.uid)
    
    def playGame(self):
        roll1 = random.randint(0, 10*self.difficulty) 
        roll2 = random.randint(0, 10*self.difficulty) 
        roll3 = random.randint(0, 10*self.difficulty) 

        if roll1 == roll2 == roll3:
            return 5000
        else:
            return 0

if __name__ == '__main__':
    slots()
