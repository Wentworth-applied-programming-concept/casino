from src.core.database import PlayerControl
import random

class slots:
    def __init__(self):
        self.player = PlayerControl()

        run = False
        while not run:
            userID = input("Enter your player ID: ")
            pword = input("Enter your password: ")

            if self.player.checkLogin(userID, pword):
                run = True
                self.uid = userID
            else:
                print("Login invalid, please try again")

        while run:
            userInput = input("Would you like to play (y/n): ")

            if userInput == 'y':
                self.player.addWinnings(self.uid, -100)
                money = self.playGame()
                self.player.addWinnings(self.uid, money)
                print(f"You earned: {money}, your balance is now {self.player.getWinnings(self.uid)}")
            else:
                quit()
    
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
