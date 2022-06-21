import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror
from src.core.casino import player, admin

user = player()
administrator = admin()

class login:
    def __init__(self):
        root = tk.Tk()
        root.title('Casino')
        root.geometry('500x100')
        root.resizable(False, False)

        frame = ttk.Frame(root)

        options = {'padx': 5, 'pady': 5}


        uname_label = ttk.Label(frame, text='Username')
        uname_label.grid(column=0, row=0, sticky='W', **options)

        pass_label = ttk.Label(frame, text='Password')
        pass_label.grid(column=1, row=0, sticky='W', **options)

        username = tk.StringVar()
        username = ttk.Entry(frame, textvariable=username)
        username.grid(column=0, row=1, **options)
        username.focus()

        password = tk.StringVar()
        password = ttk.Entry(frame, textvariable=username)
        password.grid(column=1, row=1, **options)
        password.focus()


        def checkLogin():
            try:
                login = user.checkLogin(username.get(), password.get())
                if login:
                    adminCheck = administrator.checkAdmin(username.get(), password.get())
                    root.destroy() #close login page
                    if adminCheck:
                        #launch admin
                        admin()
                    else:
                        #TODO: launch user
                        pass
                else:
                    result = f'Invalid Login, Try Again'
                    result_label.config(text=result)
            except ValueError as error:
                showerror(title='Error', message=error)


        convert_button = ttk.Button(frame, text='Login')
        convert_button.grid(column=2, row=1, sticky='W', **options)
        convert_button.configure(command=checkLogin)

        result_label = ttk.Label(frame)
        result_label.grid(row=2, columnspan=3, **options)

        frame.grid(padx=10, pady=10)

        root.mainloop()

class admin: #table based on https://www.geeksforgeeks.org/python-tkinter-treeview-scrollbar/
    def __init__(self):
        self.uidInTable = [] #list of uids already in table so users do not getting added multiple times
        self.window = tk.Tk()
        self.window.title('Casino Admin Dashboard')
        self.window.geometry('1020x900')

        self.window.resizable(False, False)
        
        self.treev = ttk.Treeview(self.window, selectmode ='browse')
        
        self.treev.pack(side ='right')

        verscrlbar = ttk.Scrollbar(self.window,
                                orient ="vertical",
                                command = self.treev.yview)
        
        verscrlbar.pack(side ='right', fill ='x')
        
        self.treev.configure(xscrollcommand = verscrlbar.set)
        
        self.treev["columns"] = ("1", "2", "3", "4")
        
        self.treev['show'] = 'headings'
        
        self.treev.column("1", width = 250, anchor ='c')
        self.treev.column("2", width = 250, anchor ='se')
        self.treev.column("3", width = 250, anchor ='se')
        self.treev.column("4", width = 250, anchor ='se')

        self.treev.heading("1", text ="Username")
        self.treev.heading("2", text ="First Name")
        self.treev.heading("3", text ="Last Name")
        self.treev.heading("4", text ="Balance")

        self.update_clock() #update table on clock
        self.window.mainloop()

    def update_clock(self):
        players = user.getPlayers()
        if players is not None: #check if any players are in db
            for player in players:
                if player.userID not in self.uidInTable: #check if player is already in table, if not add
                    self.uidInTable.append(player.userID)
                    self.treev.insert("", 'end', values =(player.userID, player.firstName, player.lastName, player.winnings))
                else: #If name already in table, update table entry
                    for entry in self.treev.get_children():
                        if player.userID in  self.treev.item(entry)['values']:
                            self.treev.item(entry, text="", values =(player.userID, player.firstName, player.lastName, player.winnings))
                        elif self.treev.item(entry)['values'][0] not in [pl.userID for pl in players]: #check to see if player was deleted or modified
                            self.treev.delete(entry)

        self.window.after(1000, self.update_clock) #callback every 1 second

if __name__=='__main__':
    login()