from src.core.casino import player, admin
from src.ui.ui import player as ui

import random

class blackjack:
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
                    self.admin.addGame('blackjack', self.uid, 100, money)
                    print(f"You earned: {money}, your balance is now {self.player.getWinnings(self.uid)}")
                else:
                    print("You do not have enough to play")
            else:
                run = False
        ui(self.uid)

    def playGame(self):
        playerbet = 100
        playerinput = ''
        cards = ['2','3','4','5','6','7','8','9','10','Jack','Queen','King','Ace']
        values = [2,3,4,5,6,7,8,9,10,10,10,10,11]
        suites = ['Hearts', 'Clubs', 'Diamonds', 'Spades']
        playerpoints = 0 
        dealerpoints = 0

        playercard1 = [ random.randint(0, 12) , random.randint(0,3) ]
        playercard2 = [ random.randint(0, 12) , random.randint(0,3) ] 

        dealercard1 = [ random.randint(0, 12) , random.randint(0,3) ]
        dealercard2 = [ random.randint(0, 12) , random.randint(0,3) ] 

        print('You have a ' + str(cards[playercard1[0]]) + ' of ' + str(suites[playercard1[1]]))
        print('and a ' + str(cards[playercard2[0]]) + ' of ' + str(suites[playercard2[1]]))
        print('Dealer\'s face card is a ' + str(cards[dealercard1[0]]) + ' of ' + str(suites[dealercard1[1]]))
    

        playerpoints += values[playercard1[0]] + values[playercard2[0]]
        if (values[playercard1[0]] == 11 and values[playercard2[0]] == 11):
          playerpoints -= 10
        playerinput = input('Add aditional card? q to stop')
        while (playerinput != 'q' and playerpoints <= 21):
          tablecard1 = [ random.randint(0, 12) , random.randint(0,3) ]
          print('You got a ' + str(cards[tablecard1[0]]) + ' of ' + str(suites[tablecard1[1]]))
          if (values[tablecard1[0]] == 11) :
            playerpoints += int(input('You got an ace, use it as a (1) or (11)?'))
          else :
            playerpoints += values[tablecard1[0]]
          if (playerpoints > 21):
            print('Player has over 21')
            break
          else :
            print('Player has ' + str(playerpoints) + ' points')
          playerinput = input('Add aditional card? q to stop')
    
    
        dealerpoints += values[dealercard1[0]] + values[dealercard2[0]]
        if (values[dealercard1[0]] == 11 and values[dealercard2[0]] == 11):
          dealerpoints -= 10
        while (dealerpoints < 17) :
          tablecard1 = [ random.randint(0, 12) , random.randint(0,3) ]
          print('Dealer got a ' + str(cards[tablecard1[0]]) + ' of ' + str(suites[tablecard1[1]]))
          dealerpoints += values[tablecard1[0]]
          if (values[tablecard1[0]] == 11 and dealerpoints > 21) :
            dealerpoints -= 10
          if (dealerpoints > 21):
            print('Dealer has over 21 and busts')
            break

        if (playerpoints > dealerpoints and playerpoints < 22) :
          print('Player wins!')
          return 5000 * (1 / self.difficulty)
        elif (dealerpoints > playerpoints and dealerpoints < 22) : 
          print('Dealer wins!')
          return 0
        else  :
          print('It\'s a tie!')
          return 100 * (1 / self.difficulty)

if __name__ == '__main__':
    blackjack()