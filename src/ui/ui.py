import enum
from socketserver import DatagramRequestHandler
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror
from src.core.casino import player, admin
import json
import importlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

user = player()
administrator = admin()


class login:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Casino')
        self.root.geometry('500x100')
        self.root.resizable(False, False)

        self.frame = ttk.Frame(self.root)

        options = {'padx': 5, 'pady': 5}

        self.uname_label = ttk.Label(self.frame, text='Username')
        self.uname_label.grid(column=0, row=0, sticky='W', **options)

        self.pass_label = ttk.Label(self.frame, text='Password')
        self.pass_label.grid(column=1, row=0, sticky='W', **options)

        self.username = tk.StringVar()
        self.username = ttk.Entry(self.frame, textvariable=self.username)
        self.username.grid(column=0, row=1, **options)
        self.username.focus()

        self.password = tk.StringVar()
        self.password = ttk.Entry(
            self.frame, textvariable=self.username, show="*")
        self.password.grid(column=1, row=1, **options)
        self.password.focus()

        convert_button = ttk.Button(self.frame, text='Login')
        convert_button.grid(column=2, row=1, sticky='W', **options)
        convert_button.configure(command=self.checkLogin)

        self.result_label = ttk.Label(self.frame)
        self.result_label.grid(row=2, columnspan=3, **options)

        self.frame.grid(padx=10, pady=10)

        self.root.mainloop()

    def checkLogin(self):
        try:
            uname = self.username.get()
            login = user.checkLogin(self.username.get(), self.password.get())
            if login:
                adminCheck = administrator.checkAdmin(
                    self.username.get(), self.password.get())
                self.root.destroy()  # close login page
                if adminCheck:
                    # launch admin
                    admin_overview_dashboard()
                else:
                    player(uname)
            else:
                result = f'Invalid Login, Try Again'
                self.result_label.config(text=result)
        except ValueError as error:
            showerror(title='Error', message=error)


class table:  # abstract table based on https://www.geeksforgeeks.org/python-tkinter-treeview-scrollbar/
    def __init__(self, window, headers, dataHeaders, size):
        self.window = window
        self.headers = headers
        self.size = size
        self.dataHeaders = dataHeaders
        self.treev = ttk.Treeview(
            self.window, column=self.headers, height=30, selectmode='browse')

    def createTable(self):
        # list of uids already in table so users do not getting added multiple times
        self.uidInTable = []
        self.window = self.window

        for value in self.headers:
            self.treev.column(value, width=int(
                self.size/(len(self.headers))), anchor='c')

            self.treev.heading(value, text=value)

        self.treev['show'] = 'headings'

        return self.treev

    def clearTable(self):
        for entry in self.treev.get_children():
            self.treev.delete(entry)
        self.uidInTable = []

    def update(self, data):  # do not allow repeating values in table
        if data is not None:  # check if any players are in db
            for val in data:
                insertValues = []
                for count, value in enumerate(self.dataHeaders):
                    valCheck = getattr(val, self.dataHeaders[count])
                    if isinstance(valCheck, float): #check to see if entry is float, if so it is related to money, so use 2 decimals
                        float2string = f"{valCheck:.2f}"
                        insertValues.append(float2string)
                    else: 
                        insertValues.append(getattr(val, self.dataHeaders[count]))

                # check if player is already in table, if not add
                if getattr(val, self.dataHeaders[0]) not in self.uidInTable:
                    self.uidInTable.append(getattr(val, self.dataHeaders[0]))
                    self.treev.insert("", 'end', values=insertValues)

                else:  # If name already in table, update table entry

                    for entry in self.treev.get_children():
                        if getattr(val, self.dataHeaders[0]) in self.treev.item(entry)['values']:
                            self.treev.item(
                                entry, text="", values=insertValues)
                        # check to see if player was deleted or modified
                        elif self.treev.item(entry)['values'][0] not in [getattr(pl, self.dataHeaders[0]) for pl in data]:
                            self.treev.delete(entry)


class admin_menu_bar:
    def __init__(self, window):
        # Based off https://pythonspot.com/tk-menubar/
        self.window = window

        self.menubar = Menu(self.window)
        self.menu = Menu(self.menubar, tearoff=0)
        self.menu.add_command(label="Casino View", command=self.casinoOverview)
        self.menu.add_command(label="Player View", command=self.userView)
        self.menu.add_command(label="Admin View", command=self.adminView)
        self.menu.add_command(label="Game History", command=self.gameView)
        self.menu.add_command(label="Generate Graphs", command=self.graph)

        self.menu.add_separator()
        self.menu.add_command(label="Logout", command=self.logout)

        self.menubar.add_cascade(label="Menu", menu=self.menu)
        self.window.config(menu=self.menubar)

    def casinoOverview(self):
        self.window.destroy()
        admin_overview_dashboard()

    def userView(self):
        self.window.destroy()
        admin_user_dashboard()

    def gameView(self):
        self.window.destroy()
        admin_game_history()

    def adminView(self):
        self.window.destroy()
        admin_admin_dashboard()

    def graph(self):
        self.window.destroy()
        admin_graph()

    def logout(self):
        self.window.destroy()
        login()


class player_menu_bar:
    def __init__(self, window, uid):
        # Based off https://pythonspot.com/tk-menubar/
        self.uid = uid

        self.window = window
        self.menubar = Menu(self.window)
        self.menu = Menu(self.menubar, tearoff=0)
        self.menu.add_command(label="Main", command=self.userView)
        self.menu.add_command(label="Launch Games", command=self.gameSelection)
        self.menu.add_command(label="Game History", command=self.gameHistory)
        self.menu.add_command(label="Generate Graphs", command=self.graph)

        self.menu.add_separator()
        self.menu.add_command(label="Logout", command=self.logout)

        self.menubar.add_cascade(label="Menu", menu=self.menu)
        self.window.config(menu=self.menubar)

    def userView(self):
        self.window.destroy()
        player(self.uid)

    def gameHistory(self):
        self.window.destroy()
        player_game_history(self.uid)

    def gameSelection(self):
        self.window.destroy()
        player_game_selection(self.uid)

    def logout(self):
        self.window.destroy()
        login()

    def graph(self):
        self.window.destroy()
        player_graph(self.uid)


class player:
    def __init__(self, uid):
        self.uid = uid

        self.window = tk.Tk()
        self.window.title('Casino User Dashboard')
        self.window.geometry('400x500')
        self.frame = ttk.Frame(self.window)

        self.window.resizable(False, False)
        player_menu_bar(self.window, self.uid)

        options = {'padx': 5, 'pady': 5}

        self.welcome_label = ttk.Label(
            self.frame, text=f"Welcome {self.uid}!", font='Helvetica 18 bold')
        self.welcome_label.grid(
            column=0, row=0, columnspan=2, sticky='W', **options)

        self.balance_label = ttk.Label(
            self.frame, text=f"Your balance is: {administrator.checkPlayerBalance(self.uid):.2f}$", font='Helvetica 12 bold')
        self.balance_label.grid(
            column=0, row=1, columnspan=2, sticky='W', **options)

        self.update_lab = ttk.Label(self.frame, text="Change your settings, fields left blank will not be updated")
        self.update_lab.grid(column=0, row=2, columnspan=2,
                             sticky='W', **options)

        self.uname_label = ttk.Label(self.frame, text='New Username:')
        self.uname_label.grid(column=0, row=3, sticky='W', **options)

        self.pass_label = ttk.Label(self.frame, text='New Password:')
        self.pass_label.grid(column=1, row=3, sticky='W', **options)

        self.fname_label = ttk.Label(self.frame, text='New First Name:')
        self.fname_label.grid(column=0, row=5, sticky='W', **options)

        self.lname_label = ttk.Label(self.frame, text='New Last Name:')
        self.lname_label.grid(column=1, row=5, sticky='W', **options)

        self.userID = tk.StringVar()
        self.userID = ttk.Entry(self.frame)
        self.userID.grid(column=0, row=4)
        self.userID.focus()

        self.password = tk.StringVar()
        self.password = ttk.Entry(self.frame)
        self.password.grid(column=1, row=4, **options)
        self.password.focus()

        self.firstName = tk.StringVar()
        self.firstName = ttk.Entry(self.frame)
        self.firstName.grid(column=0, row=6, **options)
        self.firstName.focus()

        self.lastName = tk.StringVar()
        self.lastName = ttk.Entry(self.frame)
        self.lastName.grid(column=1, row=6, **options)
        self.lastName.focus()

        update_button = ttk.Button(self.frame, text='Update Info')
        update_button.grid(column=1, row=7, sticky='e', **options)
        update_button.configure(command=self.update)

        self.frame.grid(padx=10, pady=10)

        self.window.mainloop()

    def clock(self):
        self.user_table.update(user.getPlayers())
        self.window.after(1000, self.clock)  # callback every 1 second

    def update(self):
        newUID = self.userID.get()
        out = user.updateInfo(self.uid, newUID, self.firstName.get(
        ), self.lastName.get(), self.password.get())
        if out:
            self.uid = newUID
            self.update_lab['text'] = "Update successful!"
            
            self.window.after(3000, self.resetUpdateLabel)  # reset label after 3 seconds

            self.welcome_label['text'] = f"Welcome {self.uid}!" #print updated welcome label
        else:
            self.update_lab['text'] = "Error: user not updated, check inputs"
            self.window.after(3000, self.resetUpdateLabel)  # reset label after 3 seconds

    def resetUpdateLabel(self):
        self.update_lab['text'] = "Change your settings, fields left blank will not be updated"
class player_game_history:
    def __init__(self, uid):
        self.uid = uid

        self.window = tk.Tk()
        self.window.title('Player Game History')
        self.window.geometry('1000x700')
        self.frame = ttk.Frame(self.window)

        self.window.resizable(False, False)
        player_menu_bar(self.window, self.uid)

        options = {'padx': 5, 'pady': 5}

        self.headerMap = {"ID": "gameID", "Game": "gameType",
                          "Winnings": "winnings", "Time Stamp": "timeStamp"}

        self.headers = list(self.headerMap.keys())
        self.dataHeaders = list(self.headerMap.values())

        self.user_table = table(
            self.window, self.headers, self.dataHeaders, 1000)

        self.user_tree = self.user_table.createTable()
        self.user_tree.grid(row=0, column=0, sticky=tk.NSEW)
        self.window.after(1000, self.clock)  # callback every 1 second

        self.searchBy = ttk.Label(self.frame, text='Select To Search By:')
        self.searchBy.grid(column=0, row=1, sticky='W', **options)

        self.clicked = StringVar()
        self.clicked.set("Game")
        self.drop = OptionMenu(self.frame, self.clicked, *self.headers)
        self.drop.grid(column=1, row=1, sticky='W', **options)

        self.sPhrase = ttk.Label(self.frame, text='Search Phrase:')
        self.sPhrase.grid(column=2, row=1, sticky='W', **options)

        self.sEntry = tk.StringVar()
        self.sEntry = ttk.Entry(self.frame)
        self.sEntry.grid(column=3, row=1)
        self.sEntry.focus()

        searchButton = ttk.Button(self.frame, text='Search')
        searchButton.grid(column=4, row=1, sticky='e', **options)
        searchButton.configure(command=self.search)

        clearSearch = ttk.Button(self.frame, text='Clear Search')
        clearSearch.grid(column=5, row=1, sticky='e', **options)
        clearSearch.configure(command=self.clock)

        self.frame.grid(padx=10, pady=10)

        self.window.mainloop()

    def clock(self):
        try:
            self.window.after_cancel(self.refresh)
        except:
            pass
        self.user_table.update(administrator.getGameByPlayer(self.uid))
        self.refresh = self.window.after(
            1000, self.clock)  # callback every 1 second

    def search(self):
        self.window.after_cancel(self.refresh)
        self.user_table.clearTable()
        self.user_table.update(administrator.searchForGame(
            self.headerMap[self.clicked.get()], self.sEntry.get(), self.uid))


class player_game_selection:
    def __init__(self, uid):
        self.uid = uid

        self.window = tk.Tk()
        self.window.title('Game Launcher')
        self.window.geometry('180x400')
        self.frame = ttk.Frame(self.window)

        self.window.resizable(False, False)
        player_menu_bar(self.window, self.uid)

        options = {'padx': 5, 'pady': 5}

        self.label = []
        self.button = []

        with open('src/games/games.json') as data:
            self.gameList = json.load(data)

        for count, game in enumerate(self.gameList['games']):
            self.label.append(ttk.Label(self.frame, text=game))
            self.label[count].grid(column=0, row=count,
                                   columnspan=2, sticky='W', **options)

            self.button.append(ttk.Button(self.frame, text='Play'))
            self.button[count].grid(column=2, row=count, sticky='e', **options)
            self.button[count].configure(command=lambda temp=game: self.launch(temp)) # lamba trick from https://stackoverflow.com/questions/10865116/tkinter-creating-buttons-in-for-loop-passing-command-arguments

        self.frame.grid(padx=10, pady=10)
 
        self.window.mainloop()

    def launch(self, game):
        self.window.destroy()

        game_diff = administrator.getGameDifficulty(game)

        mod = importlib.import_module(f'src.games.{game}')
        eval('mod.' + game + '(self.uid, game_diff)')


class player_graph:
    def __init__(self, uid):
        self.uid = uid

        self.window = tk.Tk()
        self.window.title('Casino Graph Dashboard')
        self.window.geometry('1000x900')
        self.frame = ttk.Frame(self.window)

        self.navbar = player_menu_bar(self.window, self.uid)

        self.window.resizable(False, False)

        options = {'padx': 5, 'pady': 5}

        self.welcome_label = ttk.Label(
            self.frame, text=f"Fill out any combination of the following options:", font='Helvetica 12 bold')
        self.welcome_label.grid(
            column=0, row=0, columnspan=2, sticky='W', **options)

        self.game_label = ttk.Label(self.frame, text='Game:')
        self.game_label.grid(column=0, row=2, sticky='W', **options)

        self.time_label = ttk.Label(
            self.frame, text='Time Range as yyyy/mm/dd-yyyy/mm/dd:')
        self.time_label.grid(column=2, row=2, sticky='W', **options)

        self.dataPoints = ttk.Label(
            self.frame, text='Number of data points to show:')
        self.dataPoints.grid(column=0, row=4, sticky='W', **options)

        self.game = tk.StringVar()
        self.game = ttk.Entry(self.frame)
        self.game.grid(column=0, row=3, **options)
        self.game.focus()

        self.time = tk.StringVar()
        self.time = ttk.Entry(self.frame)
        self.time.grid(column=2, row=3, **options)
        self.time.focus()

        self.dataPoints = tk.StringVar()
        self.dataPoints = ttk.Entry(self.frame)
        self.dataPoints.grid(column=0, row=5, **options)
        self.dataPoints.focus()

        update_button = ttk.Button(self.frame, text='Generate Graph')
        update_button.grid(column=2, row=5, sticky='e', **options)
        update_button.configure(command=self.generate)

        self.frame.grid(padx=10, pady=10)

        self.window.mainloop()

    def generate(self):
        try:
            if self.time.get() != "":
                dates = self.time.get().split('-')
                startDates = dates[0].split('/')
                endDates = dates[1].split('/')
                start = datetime.datetime(int(startDates[0]), int(
                    startDates[1]), int(startDates[2]))
                end = datetime.datetime(int(endDates[0]), int(
                    endDates[1]), int(endDates[2]))
            else:
                start = ""
                end = ""

            data = administrator.generateGraphData(
                self.uid, self.game.get(), start, end)

            times = []
            winnings = []
            for val in data:
                times.append(val.timeStamp)
                winnings.append(val.winnings)

            if self.game.get() != "":
                dp = -1*int(self.dataPoints.get())
            else:
                dp = -5
            winnings = winnings[dp:]
            times = times[dp:]

            # formatting from https://stackoverflow.com/questions/9627686/plotting-dates-on-the-x-axis-with-pythons-matplotlib
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            plt.gca().xaxis.set_major_locator(mdates.DayLocator())
            plt.bar(times, winnings, linewidth=2.0)
            plt.xticks(times)
            plt.yticks(winnings)
            plt.gcf().autofmt_xdate()
            plt.show()

        except Exception as e:
            print(e)

class admin_overview_dashboard: #displays casino winnings, per game winnings, and difficulty of games
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Casino Admin Dashboard')
        self.window.geometry('1000x900')
        self.frame = ttk.Frame(self.window)
        self.navbar = admin_menu_bar(self.window)

        self.window.resizable(False, False)

        options = {'padx': 5, 'pady': 5}

        self.balance_label = ttk.Label(
            self.frame, text=f"The All Time Casino Balance Is: {administrator.checkCasinoWinnings():.2f}$", font='Helvetica 16 bold')
        self.balance_label.grid(
            column=0, row=0, columnspan=2, sticky='W', **options)

        self.update_lab = ttk.Label(self.frame, text="View game data and update game difficulties:")
        self.update_lab.grid(column=0, row=1, columnspan=3,
                             sticky='W', **options)

        with open('src/games/games.json') as data:
            self.gameList = json.load(data)

        self.winningslabel = []
        self.difficultyLabel = []
        self.update_label = []
        self.textBox = []

        for count, game in enumerate(self.gameList['games']):
            self.winningslabel.append(ttk.Label(self.frame, text=f"{game} total: {administrator.checkGameWinnings(game):.2f}$"))
            self.winningslabel[count].grid(column=0, row=count + 2,
                                   sticky='W', **options)

            self.difficultyLabel.append(ttk.Label(self.frame, text=f"{game} difficulty: {administrator.getGameDifficulty(game)}"))
            self.difficultyLabel[count].grid(column=1, row=count + 2,
                                   sticky='W', **options)

            self.update_label.append(ttk.Label(self.frame, text="Update difficulty: "))
            self.update_label[count].grid(column=2, row=count + 2,
                                   sticky='W', **options) 

            self.textBox.append(tk.StringVar())
            self.textBox[count] = ttk.Entry(self.frame)
            self.textBox[count].grid(column=3, row=count + 2)
            self.textBox[count].focus()

        self.button = ttk.Button(self.frame, text='Update')
        self.button.grid(column=4, row=count + 2, sticky='e', **options)
        self.button.configure(command=self.update)

        self.frame.grid(padx=10, pady=10)

        self.window.mainloop()
    
    def update(self):
        error = False
        for count, game in enumerate(self.gameList['games']):
            data = self.textBox[count].get()
            if data != "": #check to make sure a difficulty was entered
                out = administrator.setGameDifficulty(game, float(data))
                if out:
                    self.difficultyLabel[count].configure(text=f"{game} difficulty: {float(data)}")
                    if not error:
                        self.update_lab['text'] = "Update successful!"
                        self.window.after(3000, self.resetUpdateLabel)  # reset label after 3 seconds
                else:
                    if not error:
                        self.update_lab['text'] = "Error: some or all values not updated, inputs cannot be over 5.0"
                        self.window.after(3000, self.resetUpdateLabel)  # reset label after 3 seconds 
                        error = True                       


    def resetUpdateLabel(self):
        self.update_lab['text'] = "View game data and update game difficulties:"           

class admin_user_dashboard:  # table based on https://www.geeksforgeeks.org/python-tkinter-treeview-scrollbar/
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Casino Admin Dashboard')
        self.window.geometry('1000x900')
        self.frame = ttk.Frame(self.window)
        self.navbar = admin_menu_bar(self.window)

        self.window.resizable(False, False)

        options = {'padx': 5, 'pady': 5}

        self.headerMap = {"Username": "userID", "First Name": "firstName",
                          "Last Name": "lastName", "Balance": "winnings"}

        self.headers = list(self.headerMap.keys())
        self.dataHeaders = list(self.headerMap.values())

        self.user_table = table(
            self.window, self.headers, self.dataHeaders, 1000)

        self.user_tree = self.user_table.createTable()
        self.user_tree.grid(row=1, column=0, sticky=tk.NSEW)
        self.window.after(1000, self.clock)  # callback every 1 second

        self.searchBy = ttk.Label(self.frame, text='Select To Search By:')
        self.searchBy.grid(column=0, row=1, sticky='W', **options)

        self.clicked = StringVar()
        self.clicked.set("Username")
        self.drop = OptionMenu(self.frame, self.clicked, *self.headers)
        self.drop.grid(column=1, row=1, sticky='W', **options)

        self.sPhrase = ttk.Label(self.frame, text='Search Phrase:')
        self.sPhrase.grid(column=2, row=1, sticky='W', **options)

        self.sEntry = tk.StringVar()
        self.sEntry = ttk.Entry(self.frame)
        self.sEntry.grid(column=3, row=1)
        self.sEntry.focus()

        self.update_lab = ttk.Label(self.frame, text="Highlight user to update settings, fields left blank will not be updated:")
        self.update_lab.grid(column=0, row=2, columnspan=4,
                             sticky='W', **options)

        searchButton = ttk.Button(self.frame, text='Search')
        searchButton.grid(column=4, row=1, sticky='e', **options)
        searchButton.configure(command=self.search)

        clearSearch = ttk.Button(self.frame, text='Clear Search')
        clearSearch.grid(column=5, row=1, sticky='e', **options)
        clearSearch.configure(command=self.clock)

        self.uname_label = ttk.Label(self.frame, text='Username:')
        self.uname_label.grid(column=0, row=3, sticky='W', **options)

        self.pass_label = ttk.Label(self.frame, text='Password:')
        self.pass_label.grid(column=2, row=3, sticky='W', **options)

        self.fname_label = ttk.Label(self.frame, text='First Name:')
        self.fname_label.grid(column=0, row=5, sticky='W', **options)

        self.lname_label = ttk.Label(self.frame, text='Last Name:')
        self.lname_label.grid(column=2, row=5, sticky='W', **options)

        self.balance_label = ttk.Label(self.frame, text='Balance:')
        self.balance_label.grid(column=0, row=7, sticky='W', **options)

        self.userID = tk.StringVar()
        self.userID = ttk.Entry(self.frame)
        self.userID.grid(column=0, row=4)
        self.userID.focus()

        self.password = tk.StringVar()
        self.password = ttk.Entry(self.frame)
        self.password.grid(column=2, row=4, **options)
        self.password.focus()

        self.firstName = tk.StringVar()
        self.firstName = ttk.Entry(self.frame)
        self.firstName.grid(column=0, row=6, **options)
        self.firstName.focus()

        self.lastName = tk.StringVar()
        self.lastName = ttk.Entry(self.frame)
        self.lastName.grid(column=2, row=6, **options)
        self.lastName.focus()

        self.balance = tk.StringVar()
        self.balance = ttk.Entry(self.frame)
        self.balance.grid(column=0, row=8, **options)
        self.balance.focus()

        update_button = ttk.Button(self.frame, text='Delete User')
        update_button.grid(column=5, row=4, sticky='e', **options)
        update_button.configure(command=self.delete)

        update_button = ttk.Button(self.frame, text='Update Existing')
        update_button.grid(column=5, row=6, sticky='e', **options)
        update_button.configure(command=self.update)

        update_button = ttk.Button(self.frame, text='Add New User')
        update_button.grid(column=5, row=8, sticky='e', **options)
        update_button.configure(command=self.add)

        self.frame.grid(padx=10, pady=10)

        self.window.mainloop()

    def clock(self):
        try:
            self.window.after_cancel(self.refresh)
        except:
            pass
        self.user_table.update(user.getPlayers())
        self.refresh = self.window.after(
            1000, self.clock)  # callback every 1 second

    def update(self):
        data = self.user_tree.item(self.user_tree.focus(), 'values')
        out = user.updateInfo(data[0], self.userID.get(), self.firstName.get(
        ), self.lastName.get(), self.password.get(), self.balance.get())

        if out:
            self.update_lab['text'] = "Update successful!"
            
            self.window.after(3000, self.resetUpdateLabel)  # reset label after 3 seconds

        else:
            self.update_lab['text'] = "Error: user not updated, check inputs"
            self.window.after(3000, self.resetUpdateLabel)  # reset label after 3 seconds

    def resetUpdateLabel(self):
        self.update_lab['text'] = "Highlight user to update settings, fields left blank will not be updated:"

    def delete(self):
        data = self.user_tree.item(self.user_tree.focus(), 'values')
        user.removePlayer(data[0])
        self.user_tree.delete(self.user_tree.focus())
        self.update_lab['text'] = f"{data[0]} deleted"
        self.window.after(3000, self.resetUpdateLabel)  # reset label after 3 seconds

    def add(self):
        out = user.createPlayer(self.userID.get(), self.firstName.get(
        ), self.lastName.get(), self.password.get(), self.balance.get())

        if out:
            self.update_lab['text'] = "User added!"
            
            self.window.after(3000, self.resetUpdateLabel)  # reset label after 3 seconds

        else:
            self.update_lab['text'] = "Error: user not added, check inputs"
            self.window.after(3000, self.resetUpdateLabel)  # reset label after 3 seconds

    def search(self):
        self.window.after_cancel(self.refresh)
        self.user_table.clearTable()
        self.user_table.update(administrator.searchForPlayer(
            self.headerMap[self.clicked.get()], self.sEntry.get()))


class admin_admin_dashboard:  # table based on https://www.geeksforgeeks.org/python-tkinter-treeview-scrollbar/
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Casino Admin Dashboard')
        self.window.geometry('1000x900')
        self.frame = ttk.Frame(self.window)
        self.navbar = admin_menu_bar(self.window)

        self.window.resizable(False, False)

        options = {'padx': 5, 'pady': 5}

        self.headerMap = {"Username": "userID",
                          "First Name": "firstName", "Last Name": "lastName"}

        self.headers = list(self.headerMap.keys())
        self.dataHeaders = list(self.headerMap.values())

        self.user_table = table(
            self.window, self.headers, self.dataHeaders, 1000)

        self.user_tree = self.user_table.createTable()
        self.user_tree.grid(row=1, column=0, sticky=tk.NSEW)
        self.window.after(1000, self.clock)  # callback every 1 second

        self.searchBy = ttk.Label(self.frame, text='Select To Search By:')
        self.searchBy.grid(column=0, row=1, sticky='W', **options)

        self.clicked = StringVar()
        self.clicked.set("Username")
        self.drop = OptionMenu(self.frame, self.clicked, *self.headers)
        self.drop.grid(column=1, row=1, sticky='W', **options)

        self.sPhrase = ttk.Label(self.frame, text='Search Phrase:')
        self.sPhrase.grid(column=2, row=1, sticky='W', **options)

        self.sEntry = tk.StringVar()
        self.sEntry = ttk.Entry(self.frame)
        self.sEntry.grid(column=3, row=1)
        self.sEntry.focus()
        
        self.update_lab = ttk.Label(self.frame, text="Highlight user to update settings, fields left blank will not be updated:")
        self.update_lab.grid(column=0, row=2, columnspan=4,
                             sticky='W', **options)

        searchButton = ttk.Button(self.frame, text='Search')
        searchButton.grid(column=4, row=1, sticky='e', **options)
        searchButton.configure(command=self.search)

        clearSearch = ttk.Button(self.frame, text='Clear Search')
        clearSearch.grid(column=5, row=1, sticky='e', **options)
        clearSearch.configure(command=self.clock)

        self.uname_label = ttk.Label(self.frame, text='Username:')
        self.uname_label.grid(column=0, row=3, sticky='W', **options)

        self.pass_label = ttk.Label(self.frame, text='Password:')
        self.pass_label.grid(column=2, row=3, sticky='W', **options)

        self.fname_label = ttk.Label(self.frame, text='First Name:')
        self.fname_label.grid(column=0, row=5, sticky='W', **options)

        self.lname_label = ttk.Label(self.frame, text='Last Name:')
        self.lname_label.grid(column=2, row=5, sticky='W', **options)

        self.userID = tk.StringVar()
        self.userID = ttk.Entry(self.frame)
        self.userID.grid(column=0, row=4)
        self.userID.focus()

        self.password = tk.StringVar()
        self.password = ttk.Entry(self.frame)
        self.password.grid(column=2, row=4, **options)
        self.password.focus()

        self.firstName = tk.StringVar()
        self.firstName = ttk.Entry(self.frame)
        self.firstName.grid(column=0, row=6, **options)
        self.firstName.focus()

        self.lastName = tk.StringVar()
        self.lastName = ttk.Entry(self.frame)
        self.lastName.grid(column=2, row=6, **options)
        self.lastName.focus()

        update_button = ttk.Button(self.frame, text='Delete User')
        update_button.grid(column=5, row=4, sticky='e', **options)
        update_button.configure(command=self.delete)

        update_button = ttk.Button(self.frame, text='Update Existing')
        update_button.grid(column=5, row=6, sticky='e', **options)
        update_button.configure(command=self.update)

        update_button = ttk.Button(self.frame, text='Add New User')
        update_button.grid(column=5, row=8, sticky='e', **options)
        update_button.configure(command=self.add)

        self.frame.grid(padx=10, pady=10)

        self.window.mainloop()

    def clock(self):
        try:
            self.window.after_cancel(self.refresh)
        except:
            pass
        self.refresh = self.user_table.update(administrator.getAdmins())
        self.window.after(1000, self.clock)  # callback every 1 second

    def update(self):
        data = self.user_tree.item(self.user_tree.focus(), 'values')
        out = administrator.updateAdminInfo(data[0], self.userID.get(
        ), self.firstName.get(), self.lastName.get(), self.password.get())

        if out:
            self.update_lab['text'] = "Update successful!"
            
            self.window.after(3000, self.resetUpdateLabel)  # reset label after 3 seconds

        else:
            self.update_lab['text'] = "Error: user not updated, check inputs"
            self.window.after(3000, self.resetUpdateLabel)  # reset label after 3 seconds

    def resetUpdateLabel(self):
        self.update_lab['text'] = "Highlight user to update settings, fields left blank will not be updated:"

    def delete(self):
        data = self.user_tree.item(self.user_tree.focus(), 'values')
        user.removePlayer(data[0])
        self.user_tree.delete(self.user_tree.focus())
        self.update_lab['text'] = f"{data[0]} deleted"
        self.window.after(3000, self.resetUpdateLabel)  # reset label after 3 seconds

    def add(self):
        out = administrator.createAdmin(self.userID.get(), self.firstName.get(
        ), self.lastName.get(), self.password.get())

        if out:
            self.update_lab['text'] = "User added!"
            
            self.window.after(3000, self.resetUpdateLabel)  # reset label after 3 seconds

        else:
            self.update_lab['text'] = "Error: user not added, check inputs"
            self.window.after(3000, self.resetUpdateLabel)  # reset label after 3 seconds

    def search(self):
        self.window.after_cancel(self.refresh)
        self.user_table.clearTable()
        self.user_table.update(administrator.searchForAdmin(
            self.headerMap[self.clicked.get()], self.sEntry.get()))


class admin_game_history:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Casino Admin Dashboard')
        self.window.geometry('1000x700')
        self.frame = ttk.Frame(self.window)

        self.window.resizable(False, False)
        self.navbar = admin_menu_bar(self.window)
        options = {'padx': 5, 'pady': 5}

        self.headerMap = {"ID": "gameID", "Game": "gameType",
                          "Player": "userID", "Winnings": "winnings", "Time Stamp": "timeStamp"}

        self.headers = list(self.headerMap.keys())
        self.dataHeaders = list(self.headerMap.values())

        self.user_table = table(
            self.window, self.headers, self.dataHeaders, 1000)

        self.user_tree = self.user_table.createTable()
        self.user_tree.grid(row=1, column=0, sticky=tk.NSEW)
        self.window.after(1000, self.clock)  # callback every 1 second

        self.searchBy = ttk.Label(self.frame, text='Select To Search By:')
        self.searchBy.grid(column=0, row=1, sticky='W', **options)

        self.clicked = StringVar()
        self.clicked.set("Game")
        self.drop = OptionMenu(self.frame, self.clicked, *self.headers)
        self.drop.grid(column=1, row=1, sticky='W', **options)

        self.sPhrase = ttk.Label(self.frame, text='Search Phrase:')
        self.sPhrase.grid(column=2, row=1, sticky='W', **options)

        self.sEntry = tk.StringVar()
        self.sEntry = ttk.Entry(self.frame)
        self.sEntry.grid(column=3, row=1)
        self.sEntry.focus()

        searchButton = ttk.Button(self.frame, text='Search')
        searchButton.grid(column=4, row=1, sticky='e', **options)
        searchButton.configure(command=self.search)

        clearSearch = ttk.Button(self.frame, text='Clear Search')
        clearSearch.grid(column=5, row=1, sticky='e', **options)
        clearSearch.configure(command=self.clock)

        self.frame.grid(padx=10, pady=10)

        self.window.mainloop()

    def clock(self):
        try:
            self.window.after_cancel(self.refresh)
        except:
            pass
        self.user_table.update(administrator.getGameHistory())
        self.refresh = self.window.after(
            1000, self.clock)  # callback every 1 second

    def search(self):
        self.window.after_cancel(self.refresh)
        self.user_table.clearTable()
        self.user_table.update(administrator.searchForGame(
            self.headerMap[self.clicked.get()], self.sEntry.get()))


class admin_graph:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Casino Admin Dashboard')
        self.window.geometry('1000x900')
        self.frame = ttk.Frame(self.window)
        self.navbar = admin_menu_bar(self.window)

        self.window.resizable(False, False)

        options = {'padx': 5, 'pady': 5}

        self.welcome_label = ttk.Label(
            self.frame, text=f"Fill out any combination of the following options:", font='Helvetica 12 bold')
        self.welcome_label.grid(
            column=0, row=0, columnspan=2, sticky='W', **options)

        self.uname_label = ttk.Label(self.frame, text='Username:')
        self.uname_label.grid(column=0, row=2, sticky='W', **options)

        self.game_label = ttk.Label(self.frame, text='Game:')
        self.game_label.grid(column=2, row=2, sticky='W', **options)

        self.time_label = ttk.Label(
            self.frame, text='Time Range as yyyy/mm/dd-yyyy/mm/dd:')
        self.time_label.grid(column=0, row=4, sticky='W', **options)

        self.dataPoints = ttk.Label(
            self.frame, text='Number of data points to show:')
        self.dataPoints.grid(column=2, row=4, sticky='W', **options)

        self.userID = tk.StringVar()
        self.userID = ttk.Entry(self.frame)
        self.userID.grid(column=0, row=3)
        self.userID.focus()

        self.game = tk.StringVar()
        self.game = ttk.Entry(self.frame)
        self.game.grid(column=2, row=3, **options)
        self.game.focus()

        self.time = tk.StringVar()
        self.time = ttk.Entry(self.frame)
        self.time.grid(column=0, row=5, **options)
        self.time.focus()

        self.dataPoints = tk.StringVar()
        self.dataPoints = ttk.Entry(self.frame)
        self.dataPoints.grid(column=2, row=5, **options)
        self.dataPoints.focus()

        update_button = ttk.Button(self.frame, text='Generate Graph')
        update_button.grid(column=2, row=6, sticky='e', **options)
        update_button.configure(command=self.generate)

        self.frame.grid(padx=10, pady=10)

        self.window.mainloop()

    def generate(self):
        try:
            if self.time.get() != "":
                dates = self.time.get().split('-')
                startDates = dates[0].split('/')
                endDates = dates[1].split('/')
                start = datetime.datetime(int(startDates[0]), int(
                    startDates[1]), int(startDates[2]))
                end = datetime.datetime(int(endDates[0]), int(
                    endDates[1]), int(endDates[2]))
            else:
                start = ""
                end = ""

            data = administrator.generateGraphData(
                self.userID.get(), self.game.get(), start, end)

            times = []
            winnings = []
            for val in data:
                times.append(val.timeStamp)
                winnings.append(val.winnings)
            if self.dataPoints.get() != "":
                dp = -1*int(self.dataPoints.get())
            else:
                dp = -5
            winnings = winnings[dp:]
            times = times[dp:]

            # formatting from https://stackoverflow.com/questions/9627686/plotting-dates-on-the-x-axis-with-pythons-matplotlib
            plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=15))

            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            plt.scatter(times, winnings)

            plt.gcf().autofmt_xdate()
            plt.show()



        except Exception as e:
            print(e)


if __name__ == '__main__':
    login()
