import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror
from src.core.casino import player

user = player()
# root window
root = tk.Tk()
root.title('Casino')
root.geometry('500x100')
root.resizable(False, False)

# frame
frame = ttk.Frame(root)


# field options
options = {'padx': 5, 'pady': 5}


uname_label = ttk.Label(frame, text='Username')
uname_label.grid(column=0, row=0, sticky='W', **options)

pass_label = ttk.Label(frame, text='Password')
pass_label.grid(column=1, row=0, sticky='W', **options)

# login entry
username = tk.StringVar()
username = ttk.Entry(frame, textvariable=username)
username.grid(column=0, row=1, **options)
username.focus()

password = tk.StringVar()
password = ttk.Entry(frame, textvariable=username)
password.grid(column=1, row=1, **options)
password.focus()
# convert button


def checkLogin():
    try:
        user.checkLogin(username.get(), password.get())
    except ValueError as error:
        showerror(title='Error', message=error)


convert_button = ttk.Button(frame, text='Login')
convert_button.grid(column=2, row=1, sticky='W', **options)
convert_button.configure(command=checkLogin)

# add padding to the frame and show it
frame.grid(padx=10, pady=10)


# start the app
root.mainloop()