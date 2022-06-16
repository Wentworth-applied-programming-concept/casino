import random

# TODO: What are our assumptions? I know that there will be money, wins, and other data associated with each player, but how can we integrate?

balance = 1000

def bet(balance):
    """This function allows the user to place multiple bets."""
    i = 0
    num = []
    amt = []
    while(cont == 'y'):
        while(1):
            num[i] = input("Which number will you bet on? (4, 5, 6, 8, 9, 10)")
            if num[i] in (4, 5, 6, 8, 9, 10):
                break
            else:
                print("Invalid bet.")
        while(1):
            print(f"Available balance: {balance}")
            amt[i] = input("How much will you bet?")
            if amt[i] <= balance:
                break
            else:
                print("Insufficient balance.")
        while(1):
            cont = input("Would you like to bet more? (y/n)")
            if cont in ('y', 'n'):
                if cont == 'y':
                    i += 1
                break
            else:
                print("Sorry, what was that?")
    return num, amt # I don't know if this return statement is what we want, we just need a way to save the bets that were placed
            
def comeOut():
    """This function starts the game."""
    bet(balance)
    d1 = random.randint(1,6)
    d2 = random.randint(1,6)
    roll = d1+d2
    while(1):
        if roll in (7, 11):
            # win
            pass # remove later
        elif roll in (2, 3, 12):
            # lose, roll again
            pass # remove later
        else:
            # point routine
            pass # remove later
    
print("Welcome to Craps! Let's do our come-out roll.")
comeOut()