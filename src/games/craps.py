from src.core.casino import player, admin
import random

class craps:

    def __init__(self, uid, odds):
        self.player = player()
        self.admin = admin()
        self.uid = uid
        self.flag = 0

        run = True
        while run:
            userInput = input("Would you like to play a round of craps? (y/n): ")

            if userInput == 'y':
                #self.admin.addWinnings(self.uid, -100)             #no buy-in for craps
                money = self.playGame()
                self.admin.addWinnings(self.uid, money)
                self.admin.addGame('Craps', self.uid, money)
                print(f"You earned: {money}, your balance is now {self.player.getWinnings(self.uid)}")
            else:
                run = False
        ui(self.uid)
    
    def playGame(self):
        '''Starts the game.'''
        print("Welcome to Craps! Let's do our come-out roll.")
        winnings += self.roundStart()
        return winnings
    
    def roundStart(self):
        '''This function starts the round.'''
        amt = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.setFlag(0)
        amt = self.bet(self.player.getWinnings(self.uid), amt)
        roll = roll()
        while(1):
            if roll in (7, 11): #pass
                # win chips bet on 7, 11 : lose on 2, 3, 12
                winnings = amt[5] + amt[9] - amt[0] - amt[1] - amt[10]
                print(f"You won ${winnings}! ")
                return winnings
            elif roll in (2, 3, 12): #dont pass
                # win chips bet on 2, 3, 12 : lose on 7, 11
                winnings = amt[0] + amt[1] + amt[10] - amt[5] - amt[9]
                print(f"You won ${winnings}! ")
                return winnings
            else:
                self.setFlag(1)
                winnings = self.point(roll, amt)
                print(f"You won ${winnings}! ")
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
            roll = roll()
            if roll in (7, 11): #lose don't passes, win passes, break
                winnings = amt[5] + amt[9] - amt[0] - amt[1] - amt[10]
                return winnings
            elif roll in (2, 3, 12): #lose passes, win don't passes, continue   
                winnings = amt[0] + amt[1] + amt[10] - amt[5] - amt[9]
                amt[0], amt[1], amt[10], amt[5], amt[9] = 0
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
                while(1):
                    i = input("Which number will you bet on? (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12): ")
                    if i in num:
                        break
                    else:
                        print("Invalid bet.")
            elif self.flag == 0:
                while(1):
                    i = input("Which number will you bet on? (2, 3, 7, 11, 12): ")
                    if i in (2, 3, 7, 11, 12):
                        break
                    else:
                        print("Invalid bet.")

            while(1):
                print(f"Available balance: {balance}")
                temp = input("How much will you bet? ")
                if temp <= balance | temp >= 0:
                    amt[i-2] += temp
                    break
                else:
                    print("Insufficient balance.")
            if input("Would you like to bet more? (y/n): ") == 'y':
                pass
            else:
                break
        return amt

    def roll(self):
        '''This function rolls the dice. Returns the sum.'''
        _ = input("Press enter to roll the dice. ")
        d1 = random.randint(1,6)
        d2 = random.randint(1,6)
        total = d1 + d2
        print(f"[{d1}] + [{d2}] = [{total}]")
        return total