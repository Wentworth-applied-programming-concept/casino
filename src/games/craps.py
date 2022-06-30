from src.core.casino import player, admin
import random

class craps:
    def __init__(self):
        self.player = player()
        self.admin = admin()

        run = False
        while not run:
            userID = input("Enter your player ID: ")
            pword = input("Enter your password: ")

            if self.player.checkLogin(userID, pword):
                run = True
                self.uid = userID                           #why is this not self.player.uid?
            else:
                print("Login invalid, please try again")
        while run:
            userInput = input("Would you like to play craps? (y/n): ")

            if userInput == 'y':
                #self.admin.addWinnings(self.uid, -100)             #no buy-in for craps
                money = self.playGame()
                self.admin.addWinnings(self.uid, money)
                self.admin.addGame('Craps', self.uid, money)
                print(f"You earned: {money}, your balance is now {self.player.getWinnings(self.uid)}")
            else:
                quit()
    

    def playGame(self):
        '''Starts the game. TODO: return money'''
        print("Welcome to Craps! Let's do our come-out roll.")
        winnings += self.comeOut()
        return winnings
          
    def comeOut(self):
        '''This function starts the round.'''
        amtBet = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        amtBet = self.bet(self.player.getWinnings(self.uid), amtBet)
        d1 = random.randint(1,6)
        d2 = random.randint(1,6)
        roll = d1+d2
        while(1):
            if roll in (7, 11):
                # win chips bet on 4-11 (numbers and pass)    #THESE ARE SO F**KIN CONFUSING YOU'RE JUST BETTING ON DICE WHY IS IT THIS COMPLICATED
                pass # remove later
            elif roll in (2, 3, 12):
                # win chips bet on all except 7/11 , lose chips bet on 7/11
                pass # remove later
            else:
                # point routine
                pass # remove later
    
    def bet(self, balance, amt):
        '''This function allows the user to place multiple bets.'''
        #amt.indexOf(i) = bet on the number i+2
        num = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        while(1):
            while(1):
                i = input("Which number will you bet on? (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12): ")
                if i in num:
                    break
                else:
                    print("Invalid bet.")
            while(1):
                print(f"Available balance: {balance}")
                temp = input("How much will you bet? ")
                if temp <= balance:
                    amt[i-2] += temp
                    break
                else:
                    print("Insufficient balance.")
            if input("Would you like to bet more? (y/n): ") == 'y':
                pass
            else:
                break
        return amt