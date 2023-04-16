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

import sqlite3
from tkinter import *
#from tkinter.ttk import *

# set as tuple? 
user_password = {
    "admin": "admin",
    "jsung": "jsung",
    "": ""
}

root = Tk()
root.title("Medical Store Management System")
root.geometry("300x200")
#root.configure(background='black')
user = ""

database = "medical_storage_20.db"
tableName = "Prescription_Drugs"
username = ""

prescriptionColumns = ["Product_Number", "Proprietary_Name", "Non_Proprietary_Name", "Dosage_Form", "Delivery", "Manufacturer", "Substance_Name", "Dosage", "Unit", "Category_Description", "Price",  "Quantity"]

try:
    medical_storage_db = sqlite3.connect(database)
    cursor = medical_storage_db.cursor()
except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)


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
    searchPrescriptionsButton = Button(frame, width=25, text="Search Prescriptions ", command=lambda: search_prescriptions(frame, ["all"]))
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

def search_prescriptions(frame, databaseList):
    clear_frame(frame)

    newEntry = []

    searchLabel = Label(frame, text="Search entire database:")
    searchEntry = Entry(frame)
    filterLabel = Label(frame, text="Filter database by category:")
    filterEntry = Entry(frame)

    newEntry.append(searchEntry)
    newEntry.append(filterEntry)

    variable = StringVar(frame)
    #variable.set(prescriptionColumns[0])

    dropDown = OptionMenu(frame, variable, *prescriptionColumns)

    searchLabel.grid(row=0, column=0)
    searchEntry.grid(row=1, column=0)
    filterLabel.grid(row=2, column=0)
    filterEntry.grid(row=3, column=0)
    dropDown.grid(row=3, column=1)

    clearButton = Button(frame, width=15, text="Clear Filters", command=lambda: clear_Labels(newEntry, frame))
    searchButton = Button(frame, width=15, text="Search", command=lambda: search_Database([searchEntry.get(), filterEntry.get(), variable.get()], frame))
    homeButton = Button(frame, width=15, text="Home Menu", command=lambda: home_Menu(frame))
    
    clearButton.grid(row=4, column=0)
    searchButton.grid(row=4, column=1)
    homeButton.grid(row=4, column=2)

    display_Inventory(frame, get_Inventory_List(databaseList))

    return


def add_prescriptions(frame):
    clear_frame(frame)

    newEntry = []

    Label(frame, text="Enter new prescription information below:", font=("Arial", 15)).grid(row=0, column=0, columnspan=2)    

    for i in range(len(prescriptionColumns)):
        addLabel = Label(frame, text=f"{prescriptionColumns[i]}:", width=15)
        addEntry = Entry(frame)

        addLabel.grid(row=i+1, column=0)
        addEntry.grid(row=i+1, column=1)

        newEntry.append(addEntry)

    clearButton = Button(frame, width=15, text="Clear", command=lambda: clear_Labels(newEntry, frame))
    submitButton = Button(frame, width=15, text="Submit", command=lambda: submit_Labels(newEntry, frame))
    homeButton = Button(frame, width=15, text="Home Menu", command=lambda: home_Menu(frame))

    clearButton.grid(row=len(prescriptionColumns)+3, column=0)
    submitButton.grid(row=len(prescriptionColumns)+3, column=1)
    homeButton.grid(row=len(prescriptionColumns)+3, column=2)

    Label(frame, text='-' * 250).grid(row=len(prescriptionColumns)+4, column=0, columnspan=len(prescriptionColumns))
    
    display_Inventory(frame, get_Inventory_List(["all"]))

    return

def display_Inventory(frame, databaseList):
    for i in range(len(prescriptionColumns)):
        displayLabel = Label(frame, text=f"{prescriptionColumns[i]}:")
        displayListbox = Listbox(frame)

        displayLabel.grid(row=len(prescriptionColumns)+5, column=i)
        displayListbox.grid(row=len(prescriptionColumns)+6, column=i)

        for item in databaseList:
            displayListbox.insert(i, item[i])
    return

def get_Inventory_List(queryList):
    query = f"SELECT * FROM {tableName} ORDER BY Proprietary_Name DESC"
    #if len(queryList) != 1 and queryList[0] != "all":
    #    if queryList != "":

        
    cursor.execute(query)
    return cursor.fetchall()

def search_Database(queryList, frame):
    for query in queryList:
        print(query)
    return

def home_Menu(frame):
    clear_frame(frame)
    open_dashboard(username)
    return


def clear_Labels(newEntry, frame):
    for entry in newEntry:
        entry.delete(0, END)
    return

def submit_Labels(newEntry, frame):
    entryItems = []
    for entry in newEntry:
        entryItems.append(entry.get())

    cursor.execute(f"INSERT INTO {tableName} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", entryItems)
    medical_storage_db.commit()
    
    clear_Labels(newEntry, frame)
    return

def clear_frame(frame):
   for widgets in frame.winfo_children():
      widgets.destroy()

create_login()

root.mainloop()