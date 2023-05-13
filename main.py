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
import tkinter
from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *
from tkcalendar import DateEntry

databaseMed = "medical_storage_1000.db"
databasePatient = "patients.db"
databaseUser = "users.db"
tableNameMed = "Prescription_Drugs"
tableNamePatient = "Patients"
tableNameUsers = "Users"
username = ""

root = Tk()
#prescriptionColumns = ["Product_Number", "Non_Proprietary_Name", "Dosage_Form", "Manufacturer", "Dosage", "Unit", "Category_Description", "Price",  "Quantity"]
prescriptionColumns = ["Product_Number", "Non_Proprietary_Name", "Manufacturer", "Dosage", "Unit", "Category_Description", "Price",  "Quantity"]
patientColumns = ["First_Name", "Middle_Initial", "Last_Name", "Gender", "Age", "Email", "Phone", "Prescriptions"]

try:
    medical_storage_db = sqlite3.connect(databaseMed)
    cursor_med = medical_storage_db.cursor()
except sqlite3.Error as error:
    print("Error while connecting to medical storage sqlite database", error)

try:
    patients_db = sqlite3.connect(databasePatient)
    cursor_patient = patients_db.cursor()
except sqlite3.Error as error:
    print("Error while connecting to patients sqlite database", error)

try:
    user_db = sqlite3.connect(databaseUser)
    cursor_user = user_db.cursor()
except sqlite3.Error as error:
    print("Error while connecting to user sqlite database", error)

# to get data from user database
user_password = (cursor_user.execute('select Username, Password from Users').fetchall())

def create_login():
    root.title("Medical Store Management System")
    root.geometry("400x200")
    
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
    newAccountButton = Button(frame, text="CREATE ACCOUNT", command=lambda: create_account(frame))

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
    root.geometry("1200x500")
    frame = Frame(root)
    frame.pack()
    userLabel = Label(frame, text=f"Welcome, {username}!", font=("Arial", 15))
    logoffButton = Button(frame, text="Logout",command=lambda: logout(frame))


    dashboardLabel = Label(frame, text=f"Medical Store Dashboard", font=("Arial", 50))

    orderLabel = Label(frame, text="Existing Prescriptions ", font=("Arial", 20))
    searchPrescriptionsButton = Button(frame, width=25, text="Search Prescriptions ", command=lambda: login_check(userEntry.get() , passwordEntry.get(), frame))
    addPrescriptionButton = Button(frame, width=25, text="Add New Prescription", command=lambda: login_check(userEntry.get() , passwordEntry.get(), frame))
    deletePrescriptionButton = Button(frame, width=25, text="Edit/Delete Existing Prescription", command=lambda: login_check(userEntry.get(), passwordEntry.get(), frame))

    inventoryLabel = Label(frame, text="Current Inventory", font=("Arial", 20))
    searchInventoryButton = Button(frame, width=25, text="Search Inventory", command=lambda: search_database(frame, ["all"], tableNameMed, prescriptionColumns, cursor_med))
    addInventoryButton = Button(frame, width=25, text="Add New Inventory", command=lambda: add_to_database(frame, tableNameMed, prescriptionColumns, databaseMed, cursor_med))
    deleteInventoryButton = Button(frame, width=25, text="Edit/Delete Existing Inventory", command=lambda: login_check(userEntry.get(), passwordEntry.get(), frame))
    
    patientLabel = Label(frame, text="Current Patients", font=("Arial", 20))
    searchPatientsButton = Button(frame, width=25, text="Search Patients", command=lambda: search_database(frame, ["all"], tableNamePatient, patientColumns, cursor_patient))
    addPatientButton = Button(frame, width=25, text="Add New Patient", command=lambda: add_to_database(frame, tableNamePatient, patientColumns, databasePatient, cursor_patient))
    deletePatientButton = Button(frame, width=25, text="Edit/Delete Existing Patient", command=lambda: Display_patients(frame,tableNamePatient,cursor_patient))

    # Display dashboard widgets
    userLabel.grid(row=0, column=4)
    logoffButton.grid(row=0, column=5)

    dashboardLabel.grid(row=1, column=0, columnspan=5)
    
    orderLabel.grid(row=5, column=0)
    searchPrescriptionsButton.grid(row=6, column=0)
    addPrescriptionButton.grid(row=7, column=0)
    deletePrescriptionButton.grid(row=8, column=0)
    
    inventoryLabel.grid(row=5, column=1)
    searchInventoryButton.grid(row=6, column=1)
    addInventoryButton.grid(row=7, column=1)
    deleteInventoryButton.grid(row=8, column=1)
    
    patientLabel.grid(row=5, column=2, columnspan=3)
    searchPatientsButton.grid(row=6, column=2, columnspan=3)
    addPatientButton.grid(row=7, column=2, columnspan=3)
    deletePatientButton.grid(row=8, column=2, columnspan=3)

def login_check(username, password, frame):
    if (username, password) in user_password:
        frame.destroy()
        open_dashboard(username)
    else:
        #errorLabel = Label(frame, text="Username and/or password not correct. Please try again.")
        errorLabal = tkinter.messagebox.showwarning(title='Login Warning', message="Username and/or password not correct. Please try again.")
        #errorLabel.grid(row=6, column=0, columnspan=2)
    return

def create_account(frame):
    frame.destroy()
    root.geometry("600x400")
    frame = Frame(root)
    frame.pack()
    headerLabel = Label(frame, text="Create A New Medical Storage Management System Account")
    usernameLabel = Label(frame, text="Username*")
    username_entry = Entry(frame)
    passwordLabel = Label(frame, text="Password*")
    password_entry = Entry(frame,show='*')
    firstNameLabel = Label(frame, text="First Name*")
    firstName_entry = Entry(frame)
    middleInitialLabel = Label(frame, text="Middle Initial")
    middleInitil_entry = Entry(frame)
    lastNameLabel = Label(frame, text="Last Name*")
    last_entry = Entry(frame)
    genderLabel = Label(frame, text="Gender")
    gender_entry = Combobox(frame,values=['Male','Female'], width=17)
    birthdateLabel = Label(frame, text="Birthdate")
    birthdate_entry = DateEntry(frame,selectmode='day', width=17)
    rolelabel = Label(frame, text='Role')
    role_entry = Combobox(frame,values=['Admin','Manager','HR'],width=17)
    addressLabel = Label(frame, text="Address")
    address_entry = Entry(frame)
    zipcodeLabel = Label(frame, text="Zip Code")
    zipcode_entry = Entry(frame)
    cityLabel = Label(frame, text="City")
    city_entry = Entry(frame)
    stateLabel = Label(frame, text="State")
    state_entry = Entry(frame)
    phoneLabel = Label(frame, text="Phone")
    phone_entry = Entry(frame)
    emailLabel = Label(frame, text="Email")
    email_entry = Entry(frame,width=20)

    headerLabel.grid(row=0, column=0, columnspan=3)
    usernameLabel.grid(row=1, column=0)
    username_entry.grid(row=1,column=1)
    passwordLabel.grid(row=1, column=2)
    password_entry.grid(row=1,column=3,padx=10,pady=10)
    firstNameLabel.grid(row=2, column=0)
    firstName_entry.grid(row=2,column=1)
    middleInitialLabel.grid(row=2, column=2)
    middleInitil_entry.grid(row=2,column=3,padx=10,pady=10)
    lastNameLabel.grid(row=3, column=0)
    last_entry.grid(row=3,column=1)
    genderLabel.grid(row=3, column=2)
    gender_entry.grid(row=3,column=3,padx=10,pady=10)
    birthdateLabel.grid(row=4,column=0)
    birthdate_entry.grid(row=4,column=1)
    rolelabel.grid(row=4, column= 2)
    role_entry.grid(row=4, column=3,padx=10,pady=10)
    addressLabel.grid(row=5,column=0)
    address_entry.grid(row=5,column=1)
    zipcodeLabel.grid(row=5,column=2)
    zipcode_entry.grid(row=5,column=3,padx=10,pady=10)
    cityLabel.grid(row=6,column=0)
    city_entry.grid(row=6,column=1)
    stateLabel.grid(row=6,column=2)
    state_entry.grid(row=6,column=3,padx=10,pady=10)
    phoneLabel.grid(row=7,column=0)
    phone_entry.grid(row=7,column=1)
    emailLabel.grid(row=7,column=2,padx=10,pady=10)
    email_entry.grid(row=7,column=3,padx=10,pady=10)

    save_entry = tkinter.Button(frame, text="Save", command=lambda : save_data(username_entry,password_entry, firstName_entry ,middleInitil_entry,last_entry,gender_entry,birthdate_entry,role_entry,address_entry,zipcode_entry,city_entry,state_entry,phone_entry,email_entry,frame))
    save_entry.grid(row=8, column=0,sticky='news', padx=10, pady=10)
    delete_entry = tkinter.Button(frame, text='Close', command=lambda : close(frame))
    delete_entry.grid(row=8, column=2, padx=10, pady=10, sticky='news')
    return

def logout(frame):
    frame.destroy()
    create_login()
    return

def search_database(frame, databaseList, tableName, columns, cursor):
    clear_frame(frame)

    newEntry = []

    userLabel = Label(frame, text=f"Welcome, {username}!", font=("Arial", 15))
    logoffButton = Button(frame, text="Logout", command=lambda: logout(frame))

    searchLabel = Label(frame, text="Search entire database:")
    searchEntry = Entry(frame)
    filterLabel = Label(frame, text="Filter database by category:")
    filterEntry = Entry(frame)

    newEntry.append(searchEntry)
    newEntry.append(filterEntry)

    variable = StringVar(frame)
    variable.set(columns[0])

    dropDown = OptionMenu(frame, variable, *columns)

    searchLabel.grid(row=0, column=0)
    searchEntry.grid(row=1, column=0)
    filterLabel.grid(row=2, column=0)
    filterEntry.grid(row=3, column=0)
    userLabel.grid(row=0, column=4)
    logoffButton.grid(row=0, column=5)
    dropDown.grid(row=3, column=1)

    clearButton = Button(frame, width=15, text="Clear Filters", command=lambda: clear_Labels(newEntry))
    searchButton = Button(frame, width=15, text="Search", command=lambda: search_database(frame, [searchEntry.get(), filterEntry.get(), variable.get()], tableName, columns, cursor))
    homeButton = Button(frame, width=15, text="Home Menu", command=lambda: home_Menu(frame))
    
    clearButton.grid(row=4, column=0)
    searchButton.grid(row=4, column=1)
    homeButton.grid(row=4, column=2)

    displayList = display_Inventory(frame, get_Inventory_List(databaseList, tableName, columns, cursor), columns)

    displayList.grid(row=5, column=0, columnspan=len(columns))

    return


def add_to_database(frame, tableName, columns, database, cursor):
    clear_frame(frame)

    newEntry = []

    userLabel = Label(frame, text=f"Welcome, {username}!", font=("Arial", 15))
    logoffButton = Button(frame, text="Logout", command=lambda: logout(frame))

    Label(frame, text="Enter New Prescription Information below:", font=("Arial", 15)).grid(row=0, column=0, columnspan=2)

    for i in range(len(columns)):
        addLabel = Label(frame, text=f"{columns[i]}:")
        addEntry = Entry(frame)

        addLabel.grid(row=i+1, column=0)
        addEntry.grid(row=i+1, column=1)

        newEntry.append(addEntry)

    userLabel.grid(row=0, column=2)
    logoffButton.grid(row=0, column=3)

    clearButton = Button(frame, width=15, text="Clear", command=lambda: clear_Labels(newEntry))
    submitButton = Button(frame, width=15, text="Submit", command=lambda: submit_Labels(newEntry, frame, tableName, columns, database, cursor))
    homeButton = Button(frame, width=15, text="Home Menu", command=lambda: home_Menu(frame))

    clearButton.grid(row=len(columns)+3, column=0)
    submitButton.grid(row=len(columns)+3, column=1)
    homeButton.grid(row=len(columns)+3, column=2)

    Label(frame, text='-' * 250).grid(row=len(columns)+4, column=0, columnspan=len(columns))
    
    displayList = display_Inventory(frame, get_Inventory_List(["all"], tableName, columns, cursor), columns)

    displayList.grid(row=len(columns)+5, column=0, columnspan=4)

    return
def save_data(username,password,firstname,m_name,lastname,gender,bday,role,addr,zipcode,city,state,phone,email,window):
    Username = username.get()
    Password = password.get()
    First_name = firstname.get()
    Middle_Initial= m_name.get()
    Last_name = lastname.get()
    Gender = gender.get()
    Birthdate = bday.get()
    Role = role.get()
    Address = addr.get()
    Zipcode = zipcode.get()
    City = city.get()
    State = state.get()
    Phone = phone.get()
    Email = email.get()
    # user db interface
    insert_query = ''' INSERT INTO Users (Username,Password,First_name,Middle_Initial,Last_name,Gender,Birthdate,Role,Address,Zipcode,City,State,Phone,Email) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
    data_insert_tuple = (Username,Password,First_name,Middle_Initial,Last_name,Gender,Birthdate,Role,Address,Zipcode,City,State,Phone,Email)
    cursor_user.execute(insert_query,data_insert_tuple)
    user_db.commit()
    window.quit()
def close(rt):
    rt.quit()

def Display_patients(rt,TableName,cursor):
    clear_frame(rt)
    tkinter.Label(rt,text='Edit/Delete Patients Record',font=('Arial',15)).grid(row=0,column=0,columnspan=6,padx=10,pady=10)
    query = f'SELECT * FROM {TableName} ORDER BY First_Name Asc LIMIT 15'
    rows = cursor.execute(query).fetchall()
    # to display columns name of patients table
    k = tkinter.Label(rt, text='First_Name')
    k.grid(row=1, column=0, padx=10, pady=10)
    l = tkinter.Label(rt, text='Middle_Name')
    l.grid(row=1, column=1, padx=10, pady=10)
    l = tkinter.Label(rt, text='Last_Name')
    l.grid(row=1, column=2, padx=10, pady=10)
    m = tkinter.Label(rt, text='Gender')
    m.grid(row=1, column=3, padx=10, pady=10)
    m = tkinter.Label(rt, text='Age')
    m.grid(row=1, column=4, padx=10, pady=10)
    n = tkinter.Label(rt, text='Email')
    n.grid(row=1, column=5, padx=10, pady=10)
    m = tkinter.Label(rt, text='Phone')
    m.grid(row=1, column=6, padx=10, pady=10)
    m = tkinter.Label(rt, text='Prescription')
    m.grid(row=1, column=7, padx=10, pady=10)

    r = 1
    for row in rows:
        for j in range(len(row)):
            z = tkinter.Entry(rt)
            z.grid(row=r,column=j)
            z.insert(END,row[j])

        del1 = tkinter.Button(rt, text='X', command= lambda d=row[0]: patient_del(d,rt,TableName,cursor))
        del1.grid(row=r,column=j+1)
        r += 1
    homeButton = Button(rt, width=15, text="Home Menu", command=lambda: home_Menu(rt))
    homeButton.grid(row=17,column=1,columnspan=6,sticky='e',padx=10,pady=10)
    edit = Button(rt,width=15,text='Edit', command= None)
    edit.grid(row=17,column=0,columnspan=6,sticky='w',padx=10,pady=10)


def patient_del(t,win,tb_name,cur):
    var = messagebox.askyesnocancel("Delete?","Delete First_Name:" + t,default='no')
    if var:
        query = "DELETE FROM Patients WHERE First_Name = ?"
        data = (t,)
        conn = cursor_patient.execute(query,data)
        messagebox.showerror('Deleted?','Number of row deleted :'+ str(conn.rowcount))
        patients_db.commit()
    # to refresh table
    Display_patients(win,tb_name,cur)
    return

def display_Inventory(frame, databaseList, columns):
    frame1 = Frame(frame)

    text_scroll = Scrollbar(frame1)
    text_scroll.grid(row=len(columns)+6, column=len(columns), sticky=NS)

    listboxWidgets = []
    for i in range(len(columns)):
        listboxWidth = 20
        if columns[i] == "Dosage" or columns[i] == "Quantity" or columns[i] == "Age" or columns[i] == "Middle_Initial":
            listboxWidth = 6
        elif columns[i] == "Unit" or columns[i] == "Price" or columns[i] == "Gender":
            listboxWidth = 8
        elif columns[i] == "Product_Number" or columns[i] == "First_Name" or columns[i] == "Last_Name" or columns[i] == "Phone":
            listboxWidth = 12
        elif columns[i] == "Category_Description" or columns[i] == "Prescriptions":
            listboxWidth = 40
        displayLabel = Label(frame1, text=f"{columns[i]}:")
        displayListbox = Listbox(frame1, bd=4, width=listboxWidth, yscrollcommand=text_scroll.set)

        displayLabel.grid(row=len(columns)+5, column=i)
        displayListbox.grid(row=len(columns)+6, column=i)

        listboxWidgets.append(displayListbox)

        for item in databaseList:
            displayListbox.insert(END, item[i])

    def multiple_yview(*args):
        for listboxWidget in listboxWidgets:
            listboxWidget.yview(*args)

    text_scroll.config(command=multiple_yview)    
    return frame1

def get_Inventory_List(queryList, tableName, columns, cursor):
    query = f"SELECT * FROM {tableName} ORDER BY Non_Proprietary_Name ASC"

    if tableName == "Patients":
        query = f"SELECT * FROM {tableName} ORDER BY Last_Name ASC"
 
    if len(queryList) == 3:
        searchAllKeyword = queryList[0]
        filterKeyword = queryList[1]
        filterCategory = queryList[2]
        
        if searchAllKeyword != "":
            query = f"SELECT * FROM {tableName} WHERE "
            for i in range(len(columns) - 1):
                query += f"{columns[i]} LIKE '%{searchAllKeyword}%' OR "
            query += f"{columns[-1]} LIKE '%{searchAllKeyword}%'"
        elif filterKeyword != "" and filterCategory != "":
            query = f"SELECT * FROM {tableName} WHERE {filterCategory} LIKE '%{filterKeyword}%'"
        else:
            win = Tk()
            win.geometry("250x50")
            win.title("Invalid Search")
            Label(win, text="Invalid search! Please try again.").pack()

    cursor.execute(query)
    
    return cursor.fetchall()

def home_Menu(frame):
    clear_frame(frame)
    frame.destroy()
    open_dashboard(username)
    return

def clear_Labels(newEntry):
    for entry in newEntry:
        entry.delete(0, END)
    return

def submit_Labels(newEntry, frame, tableName, columns, database, cursor):
    entryItems = []
    for entry in newEntry:
        entryItems.append(entry.get())

    cursor.execute(f"INSERT INTO {tableName} VALUES (?, ?, ?, ?, ?, ?, ?, ?)", entryItems)
    #database.commit()
    clear_Labels(newEntry)
    add_to_database(frame, tableName, columns, database, cursor)
    
    return

def clear_frame(frame):
   for widgets in frame.winfo_children():

      widgets.destroy()

create_login()

root.mainloop()