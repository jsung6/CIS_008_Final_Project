"""
Medical Store Management System - CIS 008 Final Project

Medical Store Management System for small enterprises based on Python. UI created to provide electronic billing documentation, database access, and stock maintenance with valued customer assistance.
These attributes have now been employed to calcualte consumer discounts, daily revenues, and procedures to avoid possible income loss.

- GUI?
- Login/Logout
- Dedicated feature for stock maintenance
- Feature to access the database
- Various options to generate bills and handle cash
"""

from tkinter import *

# set as tuple? 
user_password = {
    "admin": "admin",
    "jsung": "jsung"
}

root = Tk()
root.title("Medical Store Management System")
root.geometry("1200x500")




def create_login():
    frame = Frame(root)
    frame.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=0.5, anchor="c")
    
    # Generate login widgets
    titleLabel = Label(frame, text="Sign In")
    userLabel = Label(frame, text="Username:")
    userEntry = Entry(frame, width=15, borderwidth=3)
    passwordLabel = Label(frame, text="Password:")
    passwordEntry = Entry(frame, width=15, borderwidth=3, show="*")
    rememberCheck = Checkbutton(frame, text="Remember Me")
    signButton = Button(frame, text="SIGN IN", command=lambda: login_check(userEntry.get(), passwordEntry.get(), frame))

    # Display login widgets
    titleLabel.grid(row=0, column=0, columnspan=2)
    userLabel.grid(row=1, column=0)
    userEntry.grid(row=1, column=1)
    passwordLabel.grid(row=2, column=0)
    passwordEntry.grid(row=2, column=1)
    rememberCheck.grid(row=3, column=0)
    signButton.grid(row=3, column=1)

def create_dashboard():
    frame = Frame(root)
    frame.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=0.5, anchor="c")
    titleLabel = Label(frame, text="Welcome")

    # Display login widgets
    titleLabel.grid(row=0, column=0, columnspan=2)

def login_check(username, password, frame):
    if (username, password) in user_password.items():
        clear_frame(frame)
        create_dashboard()
    else:
        errorLabel = Label(frame, text="Username and/or password not correct. Please try again.")
        errorLabel.grid(row=4, column=0, columnspan=2)
    return


def clear_frame(frame):
    for widgets in frame.winfo_children():
        widgets.destroy()
    frame.destroy()

create_login()

root.mainloop()