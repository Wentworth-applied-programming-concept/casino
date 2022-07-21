from src.core.casino import player, admin
from src.ui.ui import player as ui
import random

class craps:

    def __init__(self, uid, diff):
        self.player = player()
        self.administrator = admin()
        self.uid = uid
        self.spent = 0
        self.flag = 0

        run = True
        
        while run:
            userInput = input("Would you like to play a round of craps? (y/n): ")

            if userInput == 'y':
                money = self.playGame()
                self.administrator.addGame('Craps', self.uid, self.spent, money)
                print(f"You earned: ${money-self.spent}, your balance is now {self.player.getWinnings(self.uid)}")
            else:
                run = False
        ui(self.uid)
    
    def playGame(self):
        '''Starts the game.'''
        print("Welcome to Craps! Let's do our come-out roll.")
        return self.roundStart()
    
    def roundStart(self):
        '''This function starts the round.'''
        amt = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.setFlag(0)
        self.spent = 0
        amt = self.bet(self.player.getWinnings(self.uid), amt)
        roll = 0
        roll = self.rollDie()
        while(1):
            if roll in (7, 11): #pass
                # win chips bet on 7, 11 : lose on 2, 3, 12
                winnings = amt[5] + amt[9]
                print(f"You won ${winnings} and spent a total of ${self.spent}. ")
                return winnings
            elif roll in (2, 3, 12): #dont pass
                # win chips bet on 2, 3, 12 : lose on 7, 11
                winnings = amt[0] + amt[1] + amt[10]
                print(f"You won ${winnings} and spent a total of ${self.spent}. ")
                return winnings
            else:
                self.setFlag(1)
                winnings = self.point(roll, amt)
                print(f"You won ${winnings} and spent a total of ${self.spent}. ")
                return winnings

    def getFlag(self):
        return self.flag

    def setFlag(self, state):
        self.flag = state

    def point(self, p, amt):
        '''Point routine.'''
        while(1):
            print(f"Point established on {p}. ")
            amt = self.bet(self.player.getWinnings(self.uid), amt)
            roll = 0
            roll = self.rollDie()
            if roll in (7, 11): #lose don't passes, win passes, break
                winnings = amt[5] + amt[9]
                return winnings
            elif roll in (2, 3, 12): #lose passes, win don't passes, continue   
                winnings = amt[0] + amt[1] + amt[10]
                amt[0] = 0; amt[1] = 0; amt[10] = 0; amt[5] = 0; amt[9] = 0
                continue
            elif roll == p: # win point, break
                winnings = amt[p]
                return winnings
            else: # win whatever u bet on, continue
                winnings = amt[roll-2]
                amt[roll-2] = 0
                continue

    def bet(self, balance, amt):
        '''This function allows the user to place multiple bets.'''
        #amt.indexOf(i) = bet on the number i+2
        num = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        while(1):
            if self.flag == 1: # point bets
                    if input("Would you like to bet more? (y/n): ") == 'y':
                        while(1):        
                            i = int(input("Which number will you bet on? (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12): "))
                            if i in num:
                                break
                            else:
                                print("Invalid bet.")
                    else:
                        break
                    
            elif self.flag == 0:
                while(1):
                    i = int(input("Which number will you bet on? (2, 3, 7, 11, 12): "))
                    if i in (2, 3, 7, 11, 12):
                        break
                    else:
                        print("Invalid bet.")

            while(1):
                print(f"Available balance: {balance-self.spent}")
                temp = int(input("How much will you bet? "))
                if temp <= balance-self.spent and temp >= 0:
                    amt[i-2] += temp
                    self.spent += temp
                    break
                else:
                    print("Insufficient balance.")
            if input("Would you like to bet more? (y/n): ") == 'y':
                pass
            else:
                break
        return amt

    def rollDie(self):
        '''This function rolls the dice. Returns the sum.'''
        _ = input("Press enter to roll the dice. ")
        d1 = random.randint(1,6)
        d2 = random.randint(1,6)
        total = d1 + d2
        print(f"[{d1}] + [{d2}] = [{total}]")
        return total