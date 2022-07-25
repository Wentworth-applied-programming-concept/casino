from matplotlib.style import available
from src.core.casino import player, admin
from src.ui.ui import player as ui

from tkinter import *
from tkinter import messagebox
import random
import pygame
import time
from PIL import ImageTk, Image


root = Tk()
root.geometry("600x500")
root.iconbitmap('src/games/slotAssets/images/slotsLogo.ico')
root.title("Casino Slots")

pygame.mixer.init()
winSound=pygame.mixer.Sound("src/games/slotAssets/sounds/Winning.MP3")

class Player():
    def __init__(self, name, availableAmt):
        self.name=name
        self.availableAmt=availableAmt
        self.betAmount=0
        self.score=0 
       
    def play (self,boardStatus, mainMenuCanvas, canvasAvailableAmt):
        
        if(self.availableAmt>=self.betAmount):
            
            if(boardStatus[0][0] == boardStatus[1][1] and boardStatus[1][1] == boardStatus[2][2]):
                self.availableAmt = self.availableAmt+self.betAmount*4
                mainMenuCanvas.itemconfig(canvasAvailableAmt,text=f"Available Cash: ${self.availableAmt}")
                messagebox.showinfo("CONGRATS", f"You won ${self.betAmount*4}.")
                time.sleep(1)
                #winSound.play(0)
            
            elif(boardStatus[0][0] == boardStatus[0][1] and boardStatus[0][1] == boardStatus[0][2]):
                self.availableAmt = self.availableAmt+self.betAmount*4
                mainMenuCanvas.itemconfig(canvasAvailableAmt,text=f"Available Cash: ${self.availableAmt}")
                messagebox.showinfo("CONGRATS", f"You won ${self.betAmount*4}.")
                time.sleep(1)
                #winSound.play(0)
        
            elif(boardStatus[1][0] == boardStatus[1][1] and boardStatus[1][1] == boardStatus[1][2]):
                self.availableAmt = self.availableAmt+self.betAmount*4
                mainMenuCanvas.itemconfig(canvasAvailableAmt,text=f"Available Cash: ${self.availableAmt}")
                messagebox.showinfo("CONGRATS", f"You won ${self.betAmount*4}.")
                time.sleep(1)
                #winSound.play(0)
            
            elif(boardStatus[2][0] == boardStatus[2][1] and boardStatus[2][1] == boardStatus[2][2]):
                self.availableAmt = self.availableAmt+self.betAmount*4
                mainMenuCanvas.itemconfig(canvasAvailableAmt,text=f"Available Cash: ${self.availableAmt}")
                messagebox.showinfo("CONGRATS", f"You won ${self.betAmount*4}.")
                
                time.sleep(1)
                #winSound.play(0)
            
            elif(boardStatus[0][0] == boardStatus[1][0] and boardStatus[1][0] == boardStatus[2][0]):
                self.availableAmt = self.availableAmt+self.betAmount*4
                messagebox.showinfo("CONGRATS", f"You won ${self.betAmount*4}.")
                mainMenuCanvas.itemconfig(canvasAvailableAmt,text=f"Available Cash: ${self.availableAmt}")
                time.sleep(1)
                #winSound.play(0)
            
            elif(boardStatus[0][1] == boardStatus[1][1] and boardStatus[1][1] == boardStatus[2][1]):
                self.availableAmt = self.availableAmt+self.betAmount*4
                mainMenuCanvas.itemconfig(canvasAvailableAmt,text=f"Available Cash: ${self.availableAmt}")
                messagebox.showinfo("CONGRATS", f"You won ${self.betAmount*4}.")
                time.sleep(1)
                #winSound.play(0)
            
            elif(boardStatus[0][2] == boardStatus[1][2] and boardStatus[1][2] == boardStatus[2][2]):
                self.availableAmt = self.availableAmt+self.betAmount*4
                mainMenuCanvas.itemconfig(canvasAvailableAmt,text=f"Available Cash: ${self.availableAmt}")
                messagebox.showinfo("CONGRATS", f"You won ${self.betAmount*4}.")
                time.sleep(1)
                #winSound.play(0)
                
            elif(boardStatus[0][2] == boardStatus[1][1] and boardStatus[1][1] == boardStatus[2][0]):
                self.availableAmt = self.availableAmt+self.betAmount*4
                mainMenuCanvas.itemconfig(canvasAvailableAmt,text=f"Available Cash: ${self.availableAmt}")
                messagebox.showinfo("CONGRATS", f"You won ${self.betAmount*4}.")
                time.sleep(1)
                #winSound.play(0)
                
            else:
                self.availableAmt=self.availableAmt-self.betAmount
            
            mainMenuCanvas.itemconfig(canvasAvailableAmt,text=f"Available Cash: ${self.availableAmt}")
        else:
            messagebox.showinfo("Error", "Not enough money for that bet. Check available amount")

class Card():
    def __init__(self, imgPath, number):
        load = Image.open(imgPath).resize((80,80))
        img= ImageTk.PhotoImage(image=load)
        self.image=img
        self.number=number
    


Cards=[Card("src/games/slotAssets/images/slot_cherry.jpg",1),Card("src/games/slotAssets/images/slot_diamond.jpg",2),
        Card("src/games/slotAssets/images/slot_watermelon.jpg",3), Card("src/games/slotAssets/images/slot7pic.png",4),
        Card("src/games/slotAssets/images/slotJackpot.jpg",5),Card("src/games/slotAssets/images/slot_lemon.jpg",6), 
        Card("src/games/slotAssets/images/slot_bar.jpg",8)]


global randNums   
randNums=[random.randint(0,6), random.randint(0,6),random.randint(0,6),
          random.randint(0,6),random.randint(0,6),random.randint(0,6),
          random.randint(0,6),random.randint(0,6),random.randint(0,6)]


def spin():
    global randNums, boardStatus
    random.shuffle(randNums)
    random.shuffle(Cards)
    krankSound=pygame.mixer.Sound("src/games/slotAssets/sounds/Krank.MP3")
    krankSound.play(loops=0)
    
    for i in range(0,9):
        mainMenuCanvas.itemconfig(canvasCards[i], image=Cards[randNums[i]].image)
    
    boardStatus= [[Cards[randNums[0]].number,Cards[randNums[1]].number,Cards[randNums[2]].number],
                  [Cards[randNums[3]].number,Cards[randNums[4]].number,Cards[randNums[5]].number],
                  [Cards[randNums[6]].number,Cards[randNums[7]].number,Cards[randNums[8]].number]]
    
    Player1.play(boardStatus,mainMenuCanvas,canvasAvailableAmt)
    


def increaseBet():
    Player1.betAmount=Player1.betAmount+5
    mainMenuCanvas.itemconfig(betText, text=f"${Player1.betAmount}")

def decreaseBet():
    if(Player1.betAmount>=5):
        Player1.betAmount=Player1.betAmount-5
        mainMenuCanvas.itemconfig(betText, text=f"${Player1.betAmount}")
    else:
        messagebox.showinfo("WARNING", "Bet amount has to be greater than 0")

def exitGame():
    root.destroy()
    

def startGame():
    global mainMenuCanvas
    mainMenuCanvas = Canvas(root, width=400, height=400) 
    mainMenuCanvas.pack(fill="both", expand=True)
     
    if(Player1.availableAmt>=0):
        mainMenuCanvas.delete("all")

        global canvasAvailableAmt, imgBottom, topImg, betText
        global canvasCards
        
        backgrdMusic=pygame.mixer.Sound("src/games/slotAssets/sounds/background.MP3")
        backgrdMusic.play(loops=10)
        mainMenuCanvas.create_text(590, 10, anchor ="ne", text=Player1.name,font=('Helvetica','12'))
        canvasAvailableAmt=mainMenuCanvas.create_text(590, 30, anchor ="ne", text=f"Available Cash: ${Player1.availableAmt}",font=('Helvetica','11'))
        spinButton = Button(root, text="Spin",font=('Helvetica','8', 'bold'),height=5, width=3, command=spin, borderwidth=2)
        mainMenuCanvas.create_window(330, 340, anchor="nw",window=spinButton)
        
        mainMenuCanvas.create_text(570, 400, anchor ="ne", text="Bet Amount:",font=('Helvetica','12'))
        betPlusButton=Button(root, text="+",font=('Helvetica','8', 'bold'),height=1,bg="#2EFF2E",fg="black", width=3, command=increaseBet, borderwidth=1)
        betminusButton=Button(root, text="-",font=('Helvetica','8', 'bold'),height=1, bg="red",fg="black",width=3, command=decreaseBet, borderwidth=1)
        mainMenuCanvas.create_window(580, 440, anchor="center",window=betPlusButton)
        mainMenuCanvas.create_window(540, 440, anchor="center",window=betminusButton)
        betText=mainMenuCanvas.create_text(570, 470, anchor ="ne", text=f"${Player1.betAmount}",font=('Helvetica','12'))
        
        exitButton=Button(root, text="Exit",font=('Helvetica','8', 'bold'),height=1, width=3, command=exitGame)
        mainMenuCanvas.create_window(30, 470, anchor="center",window=exitButton)
        
        bottomload=Image.open("src/games/slotAssets/images/bottom.png").resize((120,85))
        imgBottom= ImageTk.PhotoImage(image=bottomload)
        topImg=ImageTk.PhotoImage(image=Image.open("src/games/slotAssets/images/machine.png").resize((200,200)))
        canvasCards=[]
        mainMenuCanvas.create_image(265,383, anchor="center", image=imgBottom)
        mainMenuCanvas.create_image(265, 130,anchor="center", image=topImg)
        canvasCards.append(mainMenuCanvas.create_image(140, 100, anchor="nw",image=Cards[randNums[0]].image))
        canvasCards.append(mainMenuCanvas.create_image(220, 100,anchor="nw", image=Cards[randNums[1]].image))
        canvasCards.append(mainMenuCanvas.create_image(300, 100,anchor="nw", image=Cards[randNums[2]].image))
        canvasCards.append(mainMenuCanvas.create_image(140, 180,anchor="nw", image=Cards[randNums[3]].image))
        canvasCards.append(mainMenuCanvas.create_image(220, 180,anchor="nw", image=Cards[randNums[4]].image))
        canvasCards.append(mainMenuCanvas.create_image(300, 180, anchor="nw",image=Cards[randNums[5]].image))
        canvasCards.append(mainMenuCanvas.create_image(140, 260, anchor="nw",image=Cards[randNums[6]].image))
        canvasCards.append(mainMenuCanvas.create_image(220, 260, anchor="nw",image=Cards[randNums[7]].image))
        canvasCards.append(mainMenuCanvas.create_image(300, 260, anchor="nw",image=Cards[randNums[8]].image))
            
    else: 
        messagebox.showinfo("Warning", "Not enough money available")

    root.mainloop() 


class slots:
    def __init__(self, uid, difficulty):
        self.player = player()
        self.admin = admin()
        self.uid = uid
        self.difficulty = difficulty
        self.winnings=0
        self.cost=0
        
        global Player1
        Player1=Player(self.uid, self.player.getWinnings(self.uid))
        
        
        startGame()
        if (Player1.availableAmt>self.player.getWinnings(self.uid)):
            self.winnings= Player1.availableAmt-self.player.getWinnings(self.uid)
        elif(Player1.availableAmt<self.player.getWinnings(self.uid)):
            self.cost=self.player.getWinnings(self.uid)-Player1.availableAmt
            
        self.admin.addGame('slots', self.uid,self.cost,self.winnings)
        ui(self.uid)
        
            
  
    
if __name__ == '__main__':
    slots()


    
