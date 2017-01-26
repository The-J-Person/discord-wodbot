#!/usr/bin/python3
import tkinter as tk #UI
import apiaccess
from keyring import ObsidianKey,ObsidianSecret

api = None

def login_window():
    window = tk.Toplevel(root)
    window.title("R20BN-Tools")
    
    url = api.get_auth_url()
    
    tk.Label(window, text="Go to this URL:").grid(row=0,column=0)
    urlEntry = tk.Entry(window, width = 70)
    urlEntry.insert(tk.INSERT, url)
    urlEntry.grid(row=1,column=0)
    
    tk.Label(window, text="And copy the PIN here:").grid(row=2,column=0)
    PinEntry = tk.Entry(window)
    PinEntry.grid(row=3,column=0)
    
    login = tk.Button(window,text="Login")
    login["command"] = lambda: attempt_login(window,PinEntry.get())
    login.grid(row=4,column=0)
    
    window.protocol('WM_DELETE_WINDOW', root.destroy)
    
def attempt_login(window,pin):
    api.verify(pin) #Note to self: Check for errors? Presently not checking.
    welcome(window)
        
def welcome(old_window):
    old_window.destroy()
    window = tk.Toplevel(root)
    response = api.get_user_data()
    n = 0
    campaigns = None
    for k in response.keys():
        if k == 'campaigns':
            campaigns = response[k]
            continue
        tk.Label(window, text=k).grid(row=n,column=0)
        tk.Label(window, text=str(response[k])).grid(row=n,column=1)
        n=n+1
    responseText = tk.Text(window)
    responseText.insert(tk.INSERT, response)
    responseText.grid(row=n,column=0)
    n=n+1
    for game in campaigns:
        for k in game.keys():
            tk.Label(window, text=k).grid(row=n,column=0)
            tk.Label(window, text=str(game[k])).grid(row=n,column=1)
            n=n+1
    window.protocol('WM_DELETE_WINDOW', root.destroy)
    
###

if ObsidianKey is not None and ObsidianSecret is not None:
    api = apiaccess.ObsidianAPI(ObsidianKey,ObsidianSecret)    

root = tk.Tk()
root.title("R20BN Tools")
root.withdraw() # to minimize it, since we're just using Toplevels on top of it
tk.Label(text="Closing this window ends the program").pack()
login_window()

root.mainloop()