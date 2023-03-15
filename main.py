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
#from tkinter.ttk import *

# set as tuple? 
user_password = {
    "admin": "admin",
    "jsung": "jsung",
    "a": "a"
}

root = Tk()
root.title("Medical Store Management System")
root.geometry("300x200")
#root.configure(background='black')
user = ""

prescriptionColumns = ["Name", "Type", "Quantity", "Cost", "Description", "Expiry Date", "Location", "Manufacturer"]

def create_login():
    frame = Frame(root)
    frame.place(x=30, y=30)

    
    # Generate patient login widgets
    titleLabel = Label(frame, text="Sign In")
    userLabel = Label(frame, text="Username:")#, background="#6fa8dc")
    userEntry = Entry(frame, width=15)#, background="#6fa8dc")
    passwordLabel = Label(frame, text="Password:")
    passwordEntry = Entry(frame, width=15, show="*")
    rememberCheck = Checkbutton(frame, text="Remember Me")
    signButton = Button(frame, text="SIGN IN", command=lambda: login_check(userEntry.get(), passwordEntry.get(), frame))
    newAccountLabel = Label(frame, text="New here?")
    newAccountButton = Button(frame, text="CREATE ACCOUNT", command=lambda: create_account())

    # Display login widgets
    titleLabel.grid(row=0, column=0, columnspan=2)
    userLabel.grid(row=1, column=0)
    userEntry.grid(row=1, column=1)
    passwordLabel.grid(row=2, column=0)
    passwordEntry.grid(row=2, column=1)
    rememberCheck.grid(row=3, column=0)
    signButton.grid(row=3, column=1)
    newAccountLabel.grid(row=4, column=0, columnspan=2)
    newAccountButton.grid(row=5, column=0, columnspan=2)

def open_dashboard(username):
    root.geometry("800x400")
    frame = Frame(root)
    frame.place(x=0, y=0)
    userLabel = Label(frame, text=f"Welcome, {username}!", font=("Arial", 10))
    logoffButton = Button(frame, text="Logout", font=("Arial", 10))

    dashboardLabel = Label(frame, text=f"Medical Store Dashboard", font=("Arial", 20))

    orderLabel = Label(frame, text="Existing Prescriptions ", font=("Arial", 15))
    searchPrescriptionsButton = Button(frame, width=25, text="Search Prescriptions ", command=lambda: login_check(userEntry.get(), passwordEntry.get(), frame))
    AddPrescriptionButton = Button(frame, width=25, text="Add New Prescription", command=lambda: add_prescriptions(frame))
    deletePrescriptionButton = Button(frame, width=25, text="Delete Existing Prescription", command=lambda: login_check(userEntry.get(), passwordEntry.get(), frame))

    inventoryLabel = Label(frame, text="Current Inventory", font=("Arial", 15))
    searchInventoryButton = Button(frame, width=25, text="Search Inventory", command=lambda: login_check(userEntry.get(), passwordEntry.get(), frame))
    AddInventoryButton = Button(frame, width=25, text="Add New Inventory", command=lambda: login_check(userEntry.get() , passwordEntry.get(), frame))
    deleteInventoryButton = Button(frame, width=25, text="Delete Existing Inventory", command=lambda: login_check(userEntry.get(), passwordEntry.get(), frame))
    
    patientLabel = Label(frame, text="Current Patients", font=("Arial", 15))
    searchPatientsButton = Button(frame, width=25, text="Search Patients", command=lambda: login_check(userEntry.get(), passwordEntry.get(), frame))
    AddPatientButton = Button(frame, width=25, text="Add New Patient", command=lambda: login_check(userEntry.get(), passwordEntry.get(), frame))
    deletePatientButton = Button(frame, width=25, text="Delete Existing Patient", command=lambda: login_check(userEntry.get(), passwordEntry.get(), frame))


    # Display dashboard widgets
    userLabel.grid(row=0, column=4)
    logoffButton.grid(row=0, column=5)

    dashboardLabel.grid(row=1, column=0, columnspan=3)
    
    orderLabel.grid(row=5, column=0)
    searchPrescriptionsButton.grid(row=6, column=0)
    AddPrescriptionButton.grid(row=7, column=0)
    deletePrescriptionButton.grid(row=8, column=0)
    
    inventoryLabel.grid(row=5, column=1)
    searchInventoryButton.grid(row=6, column=1)
    AddInventoryButton.grid(row=7, column=1)
    deleteInventoryButton.grid(row=8, column=1)
    
    patientLabel.grid(row=5, column=2)
    searchPatientsButton.grid(row=6, column=2)
    AddPatientButton.grid(row=7, column=2)
    deletePatientButton.grid(row=8, column=2)

def login_check(username, password, frame):
    if (username, password) in user_password.items():
        frame.destroy()
        open_dashboard(username)
    else:
        errorLabel = Label(frame, text="Username and/or password not correct. Please try again.")
        errorLabel.grid(row=6, column=0, columnspan=2)
    return

def create_account():
    return

def add_prescriptions(frame):
    global prescriptionColumns

    clear_frame(frame)

    new_entry = []

    Label(frame, text="Enter new prescription information below:", font=("Arial", 15)).grid(row=0, column=0, columnspan=2)

    for i in range(len(prescriptionColumns)):
        addLabel = Label(frame, text=f"{prescriptionColumns[i]}:", width=15)
        addEntry = Entry(frame)

        addLabel.grid(row=i+1, column=0)
        addEntry.grid(row=i+1, column=1)

        new_entry.append(addEntry)

    clearButton = Button(frame, width=15, text="Clear", command=lambda: clear_Labels(frame))
    submitButton = Button(frame, width=15, text="Submit", command=lambda: submit_Labels(new_entry, frame))

    clearButton.grid(row=len(prescriptionColumns)+3, column=0)
    submitButton.grid(row=len(prescriptionColumns)+3, column=1)

    Label(frame, text='-' * 250).grid(row=len(prescriptionColumns)+4, column=0, columnspan=len(prescriptionColumns))

    for i in range(len(prescriptionColumns)):
        displayLabel = Label(frame, text=f"{prescriptionColumns[i]}:", width=15)
        displayListbox = Listbox(frame)

        displayLabel.grid(row=len(prescriptionColumns)+5, column=i)
        displayListbox.grid(row=len(prescriptionColumns)+6, column=i)

    return

def clear_Labels(frame):
    return

def submit_Labels(new_entry, frame):
    return

def clear_frame(frame):
   for widgets in frame.winfo_children():
      widgets.destroy()

create_login()

root.mainloop()