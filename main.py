import sqlite3
import tkinter
from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *
from tkcalendar import DateEntry
#from tkinter.ttk import *

root = Tk()

#root.configure(background='black')
user = ""

databaseMed = "medical_storage_1000.db"
databasePatient = "patients.db"
databaseUser = "users.db"
databasePres = "prescription.db"
tableNameMed = "Prescription_Drugs"
tableNamePatient = "Patients"
tableNameUsers = "Users"
tableNamePres = "pres"
username = ""

inventoryColumns = ["Product_Number", "Non_Proprietary_Name", "Manufacturer", "Dosage", "Unit", "Category_Description", "Price",  "Quantity"]
prescriptionColumns = ["Patient_Id", "First_Name", "Last_Name", "Age", "Medicine_Id", "Medicine_Name", "Dosage", "Unit", "Quantity"]
patientColumns = ["First_Name", "Middle_Initial", "Last_Name", "Gender", "Age", "Email", "Phone"]

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

try:
    pres_db = sqlite3.connect(databasePres)
    cursor_pres = pres_db.cursor()
except sqlite3.Error as error:
    print("Error while connecting to prescription sqlite database", error)

user_password = (cursor_user.execute('select Username, Password from Users').fetchall())

def create_login():
    root.title("Medical Store Management System")
    root.geometry("300x200")
    
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
    userLabel = Label(frame, text=f"Welcome, {username}!")
    logoffButton = Button(frame, text="Logout", command=lambda: logout(frame))

    dashboardLabel = Label(frame, text=f"Medical Store Dashboard")

    orderLabel = Label(frame, text="Existing Prescriptions ")
    searchPrescriptionsButton = Button(frame, width=25, text="Search Prescriptions ", command=lambda: search_prescription(frame, ["all"], tableNamePres, prescriptionColumns, cursor_pres))
    addPrescriptionButton = Button(frame, width=25, text="Add New Prescription", command=lambda: add_prescription(frame, tableNamePres, prescriptionColumns, pres_db, cursor_pres))
    #deletePrescriptionButton = Button(frame, width=25, text="Edit Existing Prescription", command=lambda: login_check(userEntry.get(), passwordEntry.get(), frame))
    
    inventoryLabel = Label(frame, text="Current Inventory")
    searchInventoryButton = Button(frame, width=25, text="Search Inventory", command=lambda: search_database(frame, ["all"], tableNameMed, inventoryColumns, cursor_med))
    addInventoryButton = Button(frame, width=25, text="Add New Inventory", command=lambda: add_to_database(frame, tableNameMed, inventoryColumns, databaseMed, cursor_med))
    #deleteInventoryButton = Button(frame, width=25, text="Edit/Delete Existing Inventory", command=lambda: login_check(userEntry.get(), passwordEntry.get(), frame))
    
    patientLabel = Label(frame, text="Current Patients")
    searchPatientsButton = Button(frame, width=25, text="Search Patients", command=lambda: search_database(frame, ["all"], tableNamePatient, patientColumns, cursor_patient))
    addPatientButton = Button(frame, width=25, text="Add New Patient", command=lambda: add_to_database(frame, tableNamePatient, patientColumns, databasePatient, cursor_patient))
    deletePatientButton = Button(frame, width=25, text="Edit/Delete Existing Patient", command=lambda: display_patients(frame,tableNamePatient,cursor_patient))

    # Display dashboard widgets
    userLabel.grid(row=0, column=4)
    logoffButton.grid(row=0, column=5)

    dashboardLabel.grid(row=1, column=0, columnspan=5)
    
    orderLabel.grid(row=5, column=0)
    searchPrescriptionsButton.grid(row=6, column=0)
    addPrescriptionButton.grid(row=7, column=0)
    #deletePrescriptionButton.grid(row=8, column=0)
    
    inventoryLabel.grid(row=5, column=1)
    searchInventoryButton.grid(row=6, column=1)
    addInventoryButton.grid(row=7, column=1)
    #deleteInventoryButton.grid(row=8, column=1)
    
    patientLabel.grid(row=5, column=2, columnspan=3)
    searchPatientsButton.grid(row=6, column=2, columnspan=3)
    addPatientButton.grid(row=7, column=2, columnspan=3)
    deletePatientButton.grid(row=8, column=2, columnspan=3)

def login_check(username, password, frame):
    if (username, password) in user_password:
        frame.destroy()
        open_dashboard(username)
    else:
        tkinter.messagebox.showwarning(title='Login Warning', message="Username and/or password not correct. Please try again.")
        #errorLabel = Label(frame, text="Username and/or password not correct. Please try again.")
        #errorLabel.grid(row=6, column=0, columnspan=2)
    return

def create_account(frame):
    frame.destroy()
    root.geometry("600x400")
    frame = Frame(root)
    frame.pack()
    headerLabel = Label(frame, text="Create A New Medical Storage Management System Account")
    usernameLabel = Label(frame, text="Username*")
    usernameEntry = Entry(frame)
    passwordLabel = Label(frame, text="Password*")
    passwordEntry = Entry(frame,show='*')
    firstNameLabel = Label(frame, text="First Name*")
    firstNameEntry = Entry(frame)
    middleInitialLabel = Label(frame, text="Middle Initial")
    middleInitialEntry = Entry(frame)
    lastNameLabel = Label(frame, text="Last Name*")
    lastEntry = Entry(frame)
    genderLabel = Label(frame, text="Gender")
    genderEntry = Combobox(frame,values=['Male','Female'], width=17)
    birthdateLabel = Label(frame, text="Birthdate")
    birthdateEntry = DateEntry(frame,selectmode='day', width=17)
    roleLabel = Label(frame, text='Role*')
    roleEntry = Combobox(frame,values=['Admin','Manager','HR'],width=17)
    addressLabel = Label(frame, text="Address")
    addressEntry = Entry(frame)
    zipcodeLabel = Label(frame, text="Zip Code")
    zipcodeEntry = Entry(frame)
    cityLabel = Label(frame, text="City")
    cityEntry = Entry(frame)
    stateLabel = Label(frame, text="State")
    stateEntry = Entry(frame)
    emailLabel = Label(frame, text="Email")
    emailEntry = Entry(frame,width=20)
    phoneLabel = Label(frame, text="Phone")
    phoneEntry = Entry(frame)

    headerLabel.grid(row=0, column=0, columnspan=3)
    usernameLabel.grid(row=1, column=0)
    usernameEntry.grid(row=1,column=1)
    passwordLabel.grid(row=1, column=2)
    passwordEntry.grid(row=1,column=3,padx=10,pady=10)
    firstNameLabel.grid(row=2, column=0)
    firstNameEntry.grid(row=2,column=1)
    middleInitialLabel.grid(row=2, column=2)
    middleInitialEntry.grid(row=2,column=3,padx=10,pady=10)
    lastNameLabel.grid(row=3, column=0)
    lastEntry.grid(row=3,column=1)
    genderLabel.grid(row=3, column=2)
    genderEntry.grid(row=3,column=3,padx=10,pady=10)
    birthdateLabel.grid(row=4,column=0)
    birthdateEntry.grid(row=4,column=1)
    roleLabel.grid(row=4, column= 2)
    roleEntry.grid(row=4, column=3,padx=10,pady=10)
    addressLabel.grid(row=5,column=0)
    addressEntry.grid(row=5,column=1)
    zipcodeLabel.grid(row=5,column=2)
    zipcodeEntry.grid(row=5,column=3,padx=10,pady=10)
    cityLabel.grid(row=6,column=0)
    cityEntry.grid(row=6,column=1)
    stateLabel.grid(row=6,column=2)
    stateEntry.grid(row=6,column=3,padx=10,pady=10)
    phoneLabel.grid(row=7,column=0)
    phoneEntry.grid(row=7,column=1)
    emailLabel.grid(row=7,column=2,padx=10,pady=10)
    emailEntry.grid(row=7,column=3,padx=10,pady=10)

    save_entry = tkinter.Button(frame, text="Save", command=lambda : save_data(usernameEntry,passwordEntry, firstNameEntry ,middleInitialEntry,lastEntry,genderEntry,birthdateEntry,roleEntry,addressEntry,zipcodeEntry,cityEntry,stateEntry,phoneEntry,emailEntry,frame))
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

    userLabel = Label(frame, text=f"Welcome, {username}!")
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

    userLabel = Label(frame, text=f"Welcome, {username}!")
    logoffButton = Button(frame, text="Logout", command=lambda: logout(frame))

    Label(frame, text="Enter New Prescription Information below:").grid(row=0, column=0, columnspan=2)    

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

    if tableName == "pres":
        query = """SELECT Patients.First_name, Patients.Last_name, Patients.Age,Prescription_Drugs.Non_Proprietary_Name,
                    Prescription_Drugs.Dosage, Prescription_Drugs.Unit, pres.Quantity
                FROM Patients, Prescription_Drugs
                JOIN pres ON Patients.Patient_id = pres.Patient_id AND Prescription_Drugs.Drug_id = pres.Drug_id"""
 
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
    database.commit()
    clear_Labels(newEntry)
    add_to_database(frame, tableName, columns, database, cursor)
    
    return

def clear_frame(frame):
   for widgets in frame.winfo_children():
      widgets.destroy()

def search_prescription(frame, databaseList, tableName, columns, cursor):
    clear_frame(frame)

    newEntry = []

    userLabel = Label(frame, text=f"Welcome, {username}!")
    logoffButton = Button(frame, text="Logout", command=lambda: logout(frame))

    search_name_label = Label(frame, text="Search by patient name:")# old name: searchEntryLabel
    search_name = Entry(frame) # searchEntry
    search_medicine_label = Label(frame, text="Search by medicine name:") # filterEntryLabel
    search_medicine = Entry(frame) # filterEntry

    newEntry.append(search_name)
    newEntry.append(search_medicine)

    variable = StringVar(frame)
    variable.set(columns[0])

    #dropDown = OptionMenu(frame, variable, *columns)

    search_name_label.grid(row=0, column=0)
    search_name.grid(row=1, column=0)
    search_medicine_label.grid(row=2, column=0)
    search_medicine.grid(row=3, column=0)
    userLabel.grid(row=0, column=4)
    logoffButton.grid(row=0, column=5)
    #dropDown.grid(row=3, column=1)

    clearButton = Button(frame, width=15, text="Clear Filters", command=lambda: clear_Labels(newEntry))
    searchButton = Button(frame, width=15, text="Search",
                          command=lambda: search_prescription(frame, [search_name.get(), search_medicine.get()],
                                                        tableName, columns, cursor))
    homeButton = Button(frame, width=15, text="Home Menu", command=lambda: home_Menu(frame))

    clearButton.grid(row=4, column=0)
    searchButton.grid(row=4, column=1)
    homeButton.grid(row=4, column=2)

    displayList = display_Inventory(frame, get_prescription_list(databaseList, columns, cursor), columns)

    displayList.grid(row=5, column=0, columnspan=len(columns))

    return

def get_prescription_list(queryList, columns, cursor):
    query = """SELECT Patients.Patient_id, Patients.First_name, Patients.Last_name, Patients.Age, Prescription_Drugs.Product_Number,
                    Prescription_Drugs.Non_Proprietary_Name, Prescription_Drugs.Dosage, Prescription_Drugs.Unit, pres.Quantity
                FROM Patients, Prescription_Drugs
                JOIN pres ON Patients.Patient_id = pres.Patient_id AND Prescription_Drugs.Product_Number = pres.Drug_id"""

    if len(queryList) == 2:
        patientName = queryList[0]
        medicineName = queryList[1]

        if patientName != "" and medicineName !="":
            query += f" WHERE Patients.First_name LIKE '%{patientName}%' " \
                     f" OR Patients.Last_name LIKE '%{patientName}%'" \
                     f" AND Prescription_Drugs.Non_Proprietary_Name LIKE '%{medicineName}%'"
        elif patientName != "":
            query += f" WHERE Patients.First_name LIKE '%{patientName}%' OR Patients.Last_name LIKE '%{patientName}%'"
        elif medicineName != "":
            query += f" WHERE Prescription_Drugs.Non_Proprietary_Name LIKE '%{medicineName}%'"

        else:
            win = Tk()
            win.geometry("250x50")
            win.title("Invalid Search")
            Label(win, text="Invalid search! Please try again.").pack()

    cursor.execute(query)

    return cursor.fetchall()

def get_patient_ids(cursor):
    query = f"SELECT Patient_id Patients FROM Patients"
    cursor.execute(query)
    return [item[0] for item in cursor.fetchall()]

def get_patient_name(patientId, cursor):
    query = f"SELECT First_name, Last_name FROM Patients WHERE Patient_id = {patientId}"
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0] + " " + result[1]

def get_drug_ids(cursor):
    query = f"SELECT Product_Number FROM Prescription_Drugs"
    cursor.execute(query)
    return [item[0] for item in cursor.fetchall()]

def get_drug_name(drugId, cursor):
    query = f"SELECT Non_Proprietary_Name FROM Prescription_Drugs WHERE Product_Number = '{drugId}'"
    cursor.execute(query)
    result = cursor.fetchone()
    return result

def insert_prescription(newEntry, frame, tableName, columns, database, cursor):
    entryItems = []
    for entry in newEntry:
        entryItems.append(entry.get())
    cursor.execute(f"INSERT INTO {tableName} (Patient_id,Drug_id,Quantity) VALUES (?, ?, ?)", entryItems)
    database.commit()
    add_prescription(frame, tableName, columns, database, cursor)
    return
def add_prescription(frame, tableName, columns, database, cursor):
    clear_frame(frame)

    userLabel = Label(frame, text=f"Welcome, {username}!")
    logoffButton = Button(frame, text="Logout", command=lambda: logout(frame))

    Label(frame, text="Enter new prescription information below:").grid(row=0, column=0, columnspan=2)

    patientId = StringVar(frame)
    patientId.set("Patient_Id")
    addLabel1 = Label(frame, text="Patient ID:")
    addLabel1.grid(row=1, column=0)
    dropDown1 = OptionMenu(frame, patientId, *get_patient_ids(cursor))
    dropDown1.grid(row=1, column=1)
    patientOut = StringVar(frame)
    patientOut.set("Patient Name")
    patientName = Label(frame, textvariable=patientOut)
    patientName.grid(row=1, column=2)
    def updatePatient(*args):
        patientOut.set(get_patient_name(patientId.get(), cursor))
    patientId.trace('w', updatePatient)

    drugId = StringVar(frame)
    drugId.set("Medicine_Id")
    addLabel2 = Label(frame, text="Medicine ID:")
    addLabel2.grid(row=2, column=0)
    dropDown2 = OptionMenu(frame, drugId, *get_drug_ids(cursor))
    dropDown2.grid(row=2, column=1)
    drugOut = StringVar(frame)
    drugOut.set("Medicine Name")
    drugName = Label(frame, textvariable=drugOut)
    drugName.grid(row=2, column=2)
    def updateDrug(*args):
        drugOut.set(get_drug_name(drugId.get(), cursor))
    drugId.trace('w', updateDrug)

    quantity = Label(frame, text="Quantity:")
    quantityEntry = Entry(frame)
    quantity.grid(row=3, column=0)
    quantityEntry.grid(row=3, column=1)

    userLabel.grid(row=0, column=2)
    logoffButton.grid(row=0, column=3)

    newPrescription = [patientId, drugId, quantityEntry]

    clearButton = Button(frame, width=15, text="Clear", command=lambda: clear_Labels([quantityEntry]))
    submitButton = Button(frame, width=15, text="Submit",
                          command=lambda: insert_prescription(newPrescription, frame, tableName, columns, database, cursor))
    homeButton = Button(frame, width=15, text="Home Menu", command=lambda: home_Menu(frame))

    clearButton.grid(row=len(columns) + 3, column=0)
    submitButton.grid(row=len(columns) + 3, column=1)
    homeButton.grid(row=len(columns) + 3, column=2)

    Label(frame, text='-' * 250).grid(row=len(columns) + 4, column=0, columnspan=len(columns))

    displayList = display_Inventory(frame, get_prescription_list(["all"], columns, cursor), columns)

    displayList.grid(row=len(columns) + 5, column=0, columnspan=4)

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

def display_patients(rt,TableName,cursor):
    clear_frame(rt)
    tkinter.Label(rt,text='Edit/Delete Patients Record').grid(row=0,column=0,columnspan=6,padx=10,pady=10)
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
    display_patients(win,tb_name,cur)
    return


create_login()

root.mainloop()