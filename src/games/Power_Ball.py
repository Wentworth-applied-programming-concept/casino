#created by Cameron Avellani
#Powerball lottery picker
import random


class powerball:
    print("Welcome to Power ball!!")

    print("In order to get the Powerball Jackpot you must match all 5 of your numbers in order to win!!\n")
    while True:
        game = 1
        print("\n -----POWERBALL PAYOUTS-----","\nMatch PB - $4", "\nMatch 1 +PB - $4", "\nMatch 2 + PB - $7", "\nMatch 3 - $7","\nMatch 3 + PB - $100", "\nMatch 4 - $100", "\nMatch 4 + PB - $1,000", "\nMatch 5 - $5,000", "\nMatch 5 + PB - $10,000")
        print("\nEach Power ball ticket costs $5\n")
    
    
        print("You have bought $5 worth of tickets!! Good luck\n")
   
    #generates numbers for each ticket
        for i in range(0,game):
            #this series of while statments makes sure that no number are the same
            num_1 = random.randint(1,69)
            num_2 = random.randint(1,69)
            while num_1 == num_2:
                num_2 =random.randint(1,69)

            num_3 = random.randint(1,69)
            while num_3 == num_2 or num_3 == num_1:
                num_3 = random.randint(1,69)

            num_4 = random.randint(1,69)
            while num_4 == num_2 or num_4 == num_1 or num_4 == num_3:
                num_4 = random.randint(1,69)

            num_5 = random.randint(1,69)
            while num_5 == num_2 or num_5 == num_1 or num_5 == num_3 or num_5 == num_4:
                num_5 = random.randint(1,69)

            powerball = random.randint(1,26)
            print("\n-----------------------PLAYER-------------------------\n" + "Your Numbers "+ ": {0:3d}{1:3d}{2:3d}{3:3d}{4:4d} Powerball {5}".format(num_1,num_2,num_3,num_4,num_5, powerball))

  
            com_num_1 = random.randint(1,69)
            com_num_2 = random.randint(1,69)
            while com_num_1 == com_num_2:
                com_num_2 =random.randint(1,69)

            com_num_3 = random.randint(1,69)
            while com_num_3 == com_num_2 or com_num_3 == com_num_1:
                com_num_3 = random.randint(1,69)

            com_num_4 = random.randint(1,69)
            while com_num_4 == com_num_2 or com_num_4 == com_num_1 or com_num_4 == com_num_3:
                com_num_4 = random.randint(1,69)

            com_num_5 = random.randint(1,69)
            while com_num_5 == com_num_2 or com_num_5 == com_num_1 or com_num_5 == com_num_3 or com_num_5 == com_num_4:
                com_num_5 = random.randint(1,69)

            com_powerball = random.randint(1,26)

        print("\n-----------------------POWER BALL-------------------------\n" + "Winning Numbers" + ": {0:3d}{1:3d}{2:3d}{3:3d}{4:4d} Powerball {5}".format(com_num_1,com_num_2,com_num_3,com_num_4,com_num_5, com_powerball))
        match = 0
        powerball_match = 0
        #if the powerballs match

        if powerball == com_powerball:
            print("You matched the power ball!")
            powerball_match = powerball_match + 1
        #if u match num 1
        if num_1 == com_num_1:
            print("You matched Ball 1!")
            match = match + 1
        #if u match num 2
        if num_2 == com_num_2:
            print("You matched Ball 2!")
            match = match + 1
        #if u match num 3
        if num_3 == com_num_3:
            print("You matched Ball 3!")
            match = match + 1
        #if u match num 4
        if num_4 == com_num_4:
            print("You matched Ball 4!")
            match = match + 1
        #if u match num 5
        if num_5 == com_num_5:
            print("You matched Ball 5!")
            match = match + 1
        #if computer 1 matches any of ur numbers
        elif powerball_match == 1:
            print("Congrats you win $4 ")
        elif match == 1 and powerball_match == 1:
            print("Congrats you win $4 ")

        elif match == 2 and powerball_match == 1:
            print("Congrats you win $7")

        elif match == 3:
            print("Congrats you win $7")

        elif match == 3 and powerball_match == 1:
            print("Congrats you win $100")

        elif match == 4:
            print("Congrats you win $100")

        elif match == 4 and powerball_match == 1:
            print("Congrats you win $1000")

        elif match == 5:
            print("Congrats you win $5000")

        elif match == 5 and powerball_match == 1:
            print("Congrats you win $10000")

        else:
            print("You lose!! Better luck next time!!")

        print("Would you like to play again?\n")
        play = input("1 - Yes\n" "2 - No\n")
        if play == '2':
            print("Thank you for playing!! Please try again soon!!")
            break
