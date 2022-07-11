import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror
from src.core.casino import player, admin
import json

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
        self.password = ttk.Entry(self.frame, textvariable=self.username, show="*")
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
                    adminCheck = administrator.checkAdmin(self.username.get(), self.password.get())
                    self.root.destroy() #close login page
                    if adminCheck:
                        #launch admin
                        admin_user_dashboard()
                    else:
                        player(uname)
                else:
                    result = f'Invalid Login, Try Again'
                    self.result_label.config(text=result)
            except ValueError as error:
                showerror(title='Error', message=error)

class player_menu_bar:
    def __init__(self, window):
        # Based off https://pythonspot.com/tk-menubar/
        self.window = window

        self.menubar = Menu(self.window)
        self.menu = Menu(self.menubar, tearoff=0)
        self.menu.add_command(label="Main", command=self.userView)
        self.menu.add_command(label="Game History", command=self.gameHistory)
        self.menu.add_command(label="Launch Games", command=self.gameSelection)
        self.menu.add_separator()
        self.menu.add_command(label="Logout", command=self.logout)

        self.menubar.add_cascade(label="Menu", menu=self.menu)
        self.window.config(menu=self.menubar)

    def userView(self):
        self.window.destroy()
        player()

    def gameHistory(self):
        self.window.destroy()
        player_game_view()

    def gameSelection(self):
        self.window.destroy()
        player_game_view()

    def logout(self):
        self.window.destroy()
        login()


class player:
    def __init__(self, uid):
        self.uid = uid

        self.uidInTable = [] #list of uids already in table so users do not getting added multiple times
        self.window = tk.Tk()
        self.window.title('Casino User Dashboard')
        self.window.geometry('400x500')
        self.frame = ttk.Frame(self.window)

        self.window.resizable(False, False)
        player_menu_bar(self.window)
        
        options = {'padx': 5, 'pady': 5}


        self.welcome_label = ttk.Label(self.frame, text=f"Welcome {self.uid}!", font='Helvetica 18 bold')
        self.welcome_label.grid(column=0, row=0, columnspan = 2, sticky='W', **options)

        self.update_lab = ttk.Label(self.frame, text=f"Change your settings")
        self.update_lab.grid(column=0, row=1, columnspan = 2, sticky='W', **options)

        self.uname_label = ttk.Label(self.frame, text='Username:')
        self.uname_label.grid(column=0, row=2, sticky='W', **options)

        self.pass_label = ttk.Label(self.frame, text='Password:')
        self.pass_label.grid(column=1, row=2, sticky='W', **options)

        self.fname_label = ttk.Label(self.frame, text='First Name:')
        self.fname_label.grid(column=0, row=4, sticky='W', **options)

        self.lname_label = ttk.Label(self.frame, text='Last Name:')
        self.lname_label.grid(column=1, row=4, sticky='W', **options)

        self.balance_label = ttk.Label(self.frame, text='Balance:')
        self.balance_label.grid(column=0, row=6, sticky='W', **options)

        self.userID = tk.StringVar()
        self.userID = ttk.Entry(self.frame)
        self.userID.grid(column=0, row=3)
        self.userID.focus()

        self.password = tk.StringVar()
        self.password = ttk.Entry(self.frame)
        self.password.grid(column=1, row=3, **options)
        self.password.focus()

        self.firstName = tk.StringVar()
        self.firstName = ttk.Entry(self.frame)
        self.firstName.grid(column=0, row=5, **options)
        self.firstName.focus()

        self.lastName = tk.StringVar()
        self.lastName = ttk.Entry(self.frame)
        self.lastName.grid(column=1, row=5, **options)
        self.lastName.focus()

        self.balance = tk.StringVar()
        self.balance = ttk.Entry(self.frame)
        self.balance.grid(column=0, row=7, **options)
        self.balance.focus()


        update_button = ttk.Button(self.frame, text='Update Info')
        update_button.grid(column=1, row=7, sticky='e', **options)
        update_button.configure(command=self.update)

        self.frame.grid(padx=10, pady=10)

        self.window.mainloop()

    def clock(self):
        self.user_table.update(user.getPlayers())
        self.window.after(1000, self.clock) #callback every 1 second

    def update(self):
        user.updateInfo(self.uid, self.userID.get(), self.firstName.get(), self.lastName.get(), self.password.get())
    
class navbar:
    def __init__(self, window):
        # Based off https://pythonspot.com/tk-menubar/
        self.window = window

        self.menubar = Menu(self.window)
        self.menu = Menu(self.menubar, tearoff=0)
        self.menu.add_command(label="Player View", command=self.userView)
        self.menu.add_command(label="Admin View", command=self.adminView)
        self.menu.add_separator()
        self.menu.add_command(label="Logout", command=self.logout)

        self.games = Menu(self.menubar, tearoff=0)
        with open('src/games/games.json') as data:
            self.gameList = json.load(data)

        for game in self.gameList['games']:
            self.games.add_command(label=game, command=lambda:self.gameView(game))

        self.menubar.add_cascade(label="Users", menu=self.menu)
        self.menubar.add_cascade(label="Games", menu=self.games)
        self.window.config(menu=self.menubar)

    def userView(self):
        self.window.destroy()
        admin_user_dashboard()

    def gameView(self, game):
        self.window.destroy()
        games(game)
    
    def adminView(self):
        self.window.destroy()
        admin_admin_dashboard()

    def logout(self):
        self.window.destroy()
        login()

class table: #abstract table based on https://www.geeksforgeeks.org/python-tkinter-treeview-scrollbar/
    def __init__(self, window, headers, dataHeaders, size):
        self.window = window
        self.headers = headers
        self.size = size
        self.dataHeaders = dataHeaders
        self.treev = ttk.Treeview(self.window, column=self.headers, height=30, selectmode ='browse')

    def createTable(self):
        self.uidInTable = [] #list of uids already in table so users do not getting added multiple times
        self.window = self.window
            
        for value in self.headers:           
            self.treev.column(value, width = int(self.size/(len(self.headers))), anchor ='c')

            self.treev.heading(value, text =value)

        self.treev['show'] = 'headings'

        return self.treev

    def update(self, data):
        if data is not None: #check if any players are in db
            for val in data:
                insertValues = []
                for count, value in enumerate(self.dataHeaders):
                    insertValues.append(getattr(val, self.dataHeaders[count]))
                    
                if getattr(val, self.dataHeaders[0]) not in self.uidInTable: #check if player is already in table, if not add
                    self.uidInTable.append(getattr(val, self.dataHeaders[0]))
                    self.treev.insert("", 'end', values =insertValues)
                    
                else: #If name already in table, update table entry

                    for entry in self.treev.get_children():
                        if getattr(val, self.dataHeaders[0]) in self.treev.item(entry)['values']:
                            self.treev.item(entry, text="", values =insertValues)
                        elif self.treev.item(entry)['values'][0] not in [getattr(pl, self.dataHeaders[0]) for pl in data]: #check to see if player was deleted or modified
                            self.treev.delete(entry)

class admin_user_dashboard: #table based on https://www.geeksforgeeks.org/python-tkinter-treeview-scrollbar/
    def __init__(self):
        self.uidInTable = [] #list of uids already in table so users do not getting added multiple times
        self.window = tk.Tk()
        self.window.title('Casino Admin Dashboard')
        self.window.geometry('1000x900')
        self.frame = ttk.Frame(self.window)
        self.navbar = navbar(self.window)

        self.window.resizable(False, False)
        
        self.user_table = table(self.window, ["Username","First Name", "Last Name", "Balance"], ["userID","firstName", "lastName", "winnings"], 1000)

        self.user_tree = self.user_table.createTable()
        self.user_tree.grid(row=1, column=0, sticky=tk.NSEW)
        self.window.after(1000, self.clock) #callback every 1 second

        options = {'padx': 5, 'pady': 5}

        self.uname_label = ttk.Label(self.frame, text='Username:')
        self.uname_label.grid(column=0, row=2, sticky='W', **options)

        self.pass_label = ttk.Label(self.frame, text='Password:')
        self.pass_label.grid(column=2, row=2, sticky='W', **options)

        self.fname_label = ttk.Label(self.frame, text='First Name:')
        self.fname_label.grid(column=0, row=4, sticky='W', **options)

        self.lname_label = ttk.Label(self.frame, text='Last Name:')
        self.lname_label.grid(column=2, row=4, sticky='W', **options)

        self.balance_label = ttk.Label(self.frame, text='Balance:')
        self.balance_label.grid(column=0, row=6, sticky='W', **options)

        self.userID = tk.StringVar()
        self.userID = ttk.Entry(self.frame)
        self.userID.grid(column=0, row=3)
        self.userID.focus()

        self.password = tk.StringVar()
        self.password = ttk.Entry(self.frame)
        self.password.grid(column=2, row=3, **options)
        self.password.focus()

        self.firstName = tk.StringVar()
        self.firstName = ttk.Entry(self.frame)
        self.firstName.grid(column=0, row=5, **options)
        self.firstName.focus()

        self.lastName = tk.StringVar()
        self.lastName = ttk.Entry(self.frame)
        self.lastName.grid(column=2, row=5, **options)
        self.lastName.focus()

        self.balance = tk.StringVar()
        self.balance = ttk.Entry(self.frame)
        self.balance.grid(column=0, row=7, **options)
        self.balance.focus()


        update_button = ttk.Button(self.frame, text='Delete User')
        update_button.grid(column=3, row=3, sticky='e', **options)
        update_button.configure(command=self.delete)

        update_button = ttk.Button(self.frame, text='Update Existing')
        update_button.grid(column=3, row=5, sticky='e', **options)
        update_button.configure(command=self.update)

        update_button = ttk.Button(self.frame, text='Add New User')
        update_button.grid(column=3, row=7, sticky='e', **options)
        update_button.configure(command=self.add)


        self.frame.grid(padx=10, pady=10)

        self.window.mainloop()

    def clock(self):
        self.user_table.update(user.getPlayers())
        self.window.after(1000, self.clock) #callback every 1 second

    def update(self):
        data = self.user_tree.item(self.user_tree.focus(), 'values')
        user.updateInfo(data[0], self.userID.get(), self.firstName.get(), self.lastName.get(), self.password.get(), self.balance.get())
    
    def delete(self):
        data = self.user_tree.item(self.user_tree.focus(), 'values')
        user.removePlayer(data[0])
        self.user_tree.delete(self.user_tree.focus())
    
    def add(self):
        user.createPlayer(self.userID.get(), self.firstName.get(), self.lastName.get(), self.password.get(), self.balance.get())

class admin_admin_dashboard: #table based on https://www.geeksforgeeks.org/python-tkinter-treeview-scrollbar/
    def __init__(self):
        self.uidInTable = [] #list of uids already in table so users do not getting added multiple times
        self.window = tk.Tk()
        self.window.title('Casino Admin Dashboard')
        self.window.geometry('1000x900')
        self.frame = ttk.Frame(self.window)
        self.navbar = navbar(self.window)

        self.window.resizable(False, False)
        
        self.user_table = table(self.window, ["Username","First Name", "Last Name"], ["userID","firstName", "lastName"], 1000)

        self.user_tree = self.user_table.createTable()
        self.user_tree.grid(row=1, column=0, sticky=tk.NSEW)
        self.window.after(1000, self.clock) #callback every 1 second

        options = {'padx': 5, 'pady': 5}

        self.uname_label = ttk.Label(self.frame, text='Username:')
        self.uname_label.grid(column=0, row=2, sticky='W', **options)

        self.pass_label = ttk.Label(self.frame, text='Password:')
        self.pass_label.grid(column=2, row=2, sticky='W', **options)

        self.fname_label = ttk.Label(self.frame, text='First Name:')
        self.fname_label.grid(column=0, row=4, sticky='W', **options)

        self.lname_label = ttk.Label(self.frame, text='Last Name:')
        self.lname_label.grid(column=2, row=4, sticky='W', **options)

        self.userID = tk.StringVar()
        self.userID = ttk.Entry(self.frame)
        self.userID.grid(column=0, row=3)
        self.userID.focus()

        self.password = tk.StringVar()
        self.password = ttk.Entry(self.frame)
        self.password.grid(column=2, row=3, **options)
        self.password.focus()

        self.firstName = tk.StringVar()
        self.firstName = ttk.Entry(self.frame)
        self.firstName.grid(column=0, row=5, **options)
        self.firstName.focus()

        self.lastName = tk.StringVar()
        self.lastName = ttk.Entry(self.frame)
        self.lastName.grid(column=2, row=5, **options)
        self.lastName.focus()

        update_button = ttk.Button(self.frame, text='Delete User')
        update_button.grid(column=3, row=3, sticky='e', **options)
        update_button.configure(command=self.delete)

        update_button = ttk.Button(self.frame, text='Update Existing')
        update_button.grid(column=3, row=5, sticky='e', **options)
        update_button.configure(command=self.update)

        update_button = ttk.Button(self.frame, text='Add New User')
        update_button.grid(column=3, row=7, sticky='e', **options)
        update_button.configure(command=self.add)


        self.frame.grid(padx=10, pady=10)

        self.window.mainloop()

    def clock(self):
        self.user_table.update(administrator.getAdmins())
        self.window.after(1000, self.clock) #callback every 1 second

    def update(self):
        data = self.user_tree.item(self.user_tree.focus(), 'values')
        administrator.updateAdminInfo(data[0], self.userID.get(), self.firstName.get(), self.lastName.get(), self.password.get())
    
    def delete(self):
        data = self.user_tree.item(self.user_tree.focus(), 'values')
        user.removePlayer(data[0])
        self.user_tree.delete(self.user_tree.focus())
    
    def add(self):
        administrator.createAdmin(self.userID.get(), self.firstName.get(), self.lastName.get(), self.password.get())

class games:
    def __init__(self, gameName):
        self.uidInTable = [] #list of uids already in table so users do not getting added multiple times
        self.window = tk.Tk()
        self.window.title('Casino Admin Dashboard')
        self.window.geometry('1000x900')
        self.frame = ttk.Frame(self.window)
        self.gameName = gameName
        self.window.resizable(False, False)
        self.navbar = navbar(self.window)

        self.user_table = table(self.window, ["ID","Player", "Winnings", "Time"], ["gameID","userID", "winnings", "timeStamp"], 1000)

        self.user_tree = self.user_table.createTable()
        self.user_tree.grid(row=1, column=0, sticky=tk.NSEW)
        self.window.after(1000, self.clock) #callback every 1 second

        self.frame.grid(padx=10, pady=10)

        self.window.mainloop()

    def clock(self):
        self.user_table.update(administrator.getGame(self.gameName))
        self.window.after(1000, self.clock) #callback every 1 second

if __name__=='__main__':
    login()