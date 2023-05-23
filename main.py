import sqlite3
import tkinter
import os
from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *
from tkcalendar import DateEntry
from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator
from InvoiceGenerator.pdf import SimpleInvoice
from datetime import date

root = Tk()

#root.configure(background='black')
user = ""
databaseMed = "prescription.db"
databasePatient = "prescription.db"
databasePres = "prescription.db"
tableNameMed = "Prescription_Drugs"
tableNamePatient = "Patients"
tableNameUsers = "Users"
tableNamePres = "pres"
username = ""


inventoryColumns = ["Product_Number", "Non_Proprietary_Name", "Manufacturer", "Dosage", "Unit", "Category_Description", "Price",  "Quantity"]
prescriptionColumns = ["Patient_Id", "First_Name", "Last_Name", "Age", "Medicine_Id", "Medicine_Name", "Dosage", "Unit", "Quantity"]
patientColumns = ["First_Name", "Middle_Initial", "Last_Name", "Gender", "Age", "Email", "Phone","Patient_id"]


try:
    medical_storage_db = sqlite3.connect(databaseMed)
    cursor_med = medical_storage_db.cursor()
except sqlite3.Error as error:
    print("Error while connecting to medical storage sqlite database", error)

try:
    patients_db = sqlite3.connect(databasePatient)
    cursor_patient = patients_db.cursor()
    patients_db.set_trace_callback(print)
except sqlite3.Error as error:
    print("Error while connecting to patients sqlite database", error)

try:
    pres_db = sqlite3.connect(databasePres)
    cursor_pres = pres_db.cursor()
except sqlite3.Error as error:
    print("Error while connecting to prescription sqlite database", error)


user_password = (cursor_pres.execute('select Username, Password from Users').fetchall())

def create_login():
    root.title("Medical Store Management System")
    root.geometry("400x200")

    
    frame = Frame(root)
    frame.place(x=30, y=30)

    # Generate patient login widgets
    titleLabel = Label(frame, text="Sign In",font="Arial,15")
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
    userLabel.grid(row=1, column=0,padx=5,pady=5)
    userEntry.grid(row=1, column=1,padx=5,pady=5)
    passwordLabel.grid(row=2, column=0,padx=5,pady=5)
    passwordEntry.grid(row=2, column=1,padx=5,pady=5)
    rememberCheck.grid(row=3, column=0,padx=5,pady=5)
    signButton.grid(row=3, column=1,padx=5,pady=5)
    newAccountLabel.grid(row=4, column=0, columnspan=2)
    newAccountButton.grid(row=5, column=0, columnspan=2)

def open_dashboard(username):
    root.geometry("1800x700")
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
    deletePatientButton = Button(frame, width=25, text="Edit/Delete Existing Patient", command=lambda: Display_patients(frame,tableNamePatient,cursor_pres,0))
    generateInvoiceButton = Button(frame, width=25, text="Generate Invoice", command=lambda: get_invoice(frame, tableNamePres, prescriptionColumns, cursor_pres,tableNameMed))



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
    generateInvoiceButton.grid(row=9, column=2, columnspan=3)

def get_invoice(frame, tableName, columns, cursor,tableNameMed):
    clear_frame(frame)
    patientId = StringVar(frame)
    patientId.set("Patient_Id")
    addLabel1 = Label(frame, text="Patient ID:")
    addLabel1.grid(row=1, column=0)
    dropDown1 = OptionMenu(frame, patientId, *get_patient_ids(cursor))
    dropDown1.grid(row=1, column=1)
    generateInvoiceButton = Button(frame, width=25, text="Generate Invoice", command=lambda: generate_invoice(frame, tableNamePres, prescriptionColumns, cursor_pres,patientId,tableNameMed))
   
    generateInvoiceButton.grid(row=2, column=1)
    homeButton = Button(frame, width=15, text="Home Menu", command=lambda: home_Menu(frame))
    homeButton.grid(row=4, column=1)


def generate_invoice(frame, tableName, columns, cursor,patientId,tableNameMed):

    print(patientId.get())
    try:
        query = f"SELECT Patients.Patient_id,Patients.First_name, Patients.Last_name,Prescription_Drugs.Non_Proprietary_Name,pres.Quantity,Prescription_Drugs.Price,Prescription_Drugs.Quantity,Prescription_Drugs.Product_Number FROM pres LEFT JOIN Patients ON pres.Patient_id = Patients.Patient_id LEFT JOIN Prescription_Drugs ON pres.Drug_id = Prescription_Drugs.Product_Number WHERE Patients.Patient_id = {patientId.get()}"
        rows = cursor.execute(query).fetchall()
        print(rows)
        print(f"No of records - {len(rows)}")
        if (len(rows) == 0):
            raise Exception("Sorry, no numbers below zero")
        else:
            os.environ["INVOICE_LANG"] = "en"
            client = Client(rows[0][1] + " " + rows[0][2])
            provider = Provider('MCA', bank_account='2600420569', bank_code='2010')
            creator = Creator('CIS_008_Group3')
            invoice = Invoice(client, provider, creator)
            invoice.currency = u'\u0024'
            invoice.currency_locale = 'en_US.UTF-8'
            invoice.number = patientId.get()
            invoice.use_tax = True
            #invoice.title = f"Invoice for {patientId.get()}"
            invoice.date = date.today()

            for i in range(len(rows)):
                print(i)
                avilable_quantity = rows[i][6]
                requested_quantity = rows[i][4]
                print(f"Check-1 {avilable_quantity} {requested_quantity}")
                if (requested_quantity <= avilable_quantity):
                    print(f"Updating for {rows[i]}")
                    price = float(rows[i][5].split("$")[1])
                    print(rows[i][4],price,rows[i][3],'10.04')
                    dstring = rows[i][3].strip()          
                    invoice.add_item(Item(rows[i][4],price, description=dstring,tax='10.04'))

                else:
                    raise IndexError
            

            pdf = SimpleInvoice(invoice)
            pdf.gen(f"invoice-{rows[0][0]}.pdf", generate_qr_code=True)
            tkinter.messagebox.showinfo(title ='Invoice', message=f'Invocie of {rows[0][1] + " " + rows[0][2]} generated successfully') 

            update_database(cursor,rows,tableNameMed)
            print("The END")

              
    except IndexError as err:
        tkinter.messagebox.showwarning(title ='Invoice Warning',message=f'Running out of Stock -{rows[i][3]} ')
    except Exception as err:
        print("An error occurred:", err)
        print(len(rows))
        tkinter.messagebox.showwarning(title = "Invoice Warning",message='Record not found') 

def update_database(cursor,rows,tableNameMed):
    print(f"in update functin {cursor}{rows}{tableNameMed}")
    for i in range(len(rows)):
        avilable_quantity = rows[i][6]
        requested_quantity = rows[i][4]
        print(f"Check-1 {avilable_quantity} {requested_quantity}")
        remaing_quantity = avilable_quantity - requested_quantity
        query = f"UPDATE {tableNameMed} SET Quantity = {remaing_quantity} WHERE Product_Number = '{rows[i][7]}'"
        print(f"The query is - {query}")
        cursor.execute(query)
        pres_db.commit()

    

def login_check(username, password, frame):
    if (username, password) in user_password:
        frame.destroy()
        open_dashboard(username)
    else:
        #errorLabel = Label(frame, text="Username and/or password not correct. Please try again.")
        tkinter.messagebox.showwarning(title='Login Warning', message="Username and/or password not correct. Please try again.")
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
    rolelabel = Label(frame, text='Role*')
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
def save_data(username,password,firstname,m_name,lastname,gender,bday,role,addr,zipcode,city,state,phone,email,window):
    # error if required field is empty
    if username.get()== "" or password.get() == "" or firstname.get() == "" or lastname.get()== "" or role.get()== "":
        messagebox.showerror('Error',"Please enter required field")
        return
    # for getting data
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
    # user table interfaces into db
    insert_query = ''' INSERT INTO Users (Username,Password,First_name,Middle_Initial,Last_name,Gender,Birthdate,Role,Address,Zipcode,City,State,Phone,Email) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
    data_insert_tuple = (Username,Password,First_name,Middle_Initial,Last_name,Gender,Birthdate,Role,Address,Zipcode,City,State,Phone,Email)
    cursor_pres.execute(insert_query,data_insert_tuple)
    pres_db.commit()
    window.quit()
def close(rt):
    rt.quit()

def Display_patients(rt, TableName, cursor, start):
    clear_frame(rt)
    
    if(start < 0):
        start = 0
    next_number = start + 15

    Label(rt,text='Edit/Delete Patients Record',font=('Arial',15)).grid(row=0,column=0,columnspan=6,padx=10,pady=10)
    query = f'SELECT Patient_id, First_Name, Middle_Initial, Last_Name, Gender, Age, Email, Phone FROM {TableName} ORDER BY Patient_id Asc LIMIT {str(start)}, 15'
    rows = cursor.execute(query).fetchall()
    #print(f"Legth of records - {rows}")
    r_set=cursor.execute(f"SELECT count(*) as no from {TableName}")
    data_row=r_set.fetchone()
    no_rec=data_row[0] # Total number of rows in table
    #print(no_rec)

    #print(f"Next number - {next_number}")
    # to display columns name of patients table
    Label(rt, text='Patient_id').grid(row=1, column=0, padx=10, pady=10)
    Label(rt, text='First_Name').grid(row=1, column=1, padx=10, pady=10)
    Label(rt, text='Middle_Name').grid(row=1, column=2, padx=10, pady=10)
    Label(rt, text='Last_Name').grid(row=1, column=3, padx=10, pady=10)
    Label(rt, text='Gender').grid(row=1, column=4, padx=10, pady=10)
    Label(rt, text='Age').grid(row=1, column=5, padx=10, pady=10)
    Label(rt, text='Email').grid(row=1, column=6, padx=10, pady=10)
    Label(rt, text='Phone').grid(row=1, column=7, padx=10, pady=10)


    r = 2
    for row in rows:
        for j in range(len(row)):
            z = tkinter.Entry(rt)
            z.grid(row=r,column=j)
            z.insert(END,row[j])
        #print("Rownum 1: :" + str(r))
        edit = tkinter.Button(rt, width=15, text='Edit', command=lambda d=row[0], row_num=r: Edit(d,str(row_num), rt, TableName, cursor, start))
        edit.grid(row=r,column=j+2)
        del1 = tkinter.Button(rt, text='X', command= lambda d=row[0]: patient_del(d,rt,TableName,cursor,start))
        del1.grid(row=r,column=j+1)
        r += 1

    if start > 0:
        prevButton = Button(rt, width=15, text="<<Prev", command=lambda: Display_patients(rt, TableName, cursor, (start - 15)))
        prevButton.grid(row=17,column=0,sticky='e',pady=10)
    
    homeButton = Button(rt, width=15, text="Home Menu", command=lambda: home_Menu(rt))
    homeButton.grid(row=17,column=4,sticky='e',padx=10,pady=10)

    nextButton = Button(rt, width=15, text="Next>>", command=lambda: Display_patients(rt, TableName, cursor, (start + 15)))
    nextButton.grid(row=17,column=9,sticky='e',padx=10)
    if(no_rec <= next_number): 
        nextButton["state"]="disabled" # disable next button
    else:
        nextButton["state"]="active"

    #text_scroll.config(command=canvas.yview)


def patient_del(t,win,tb_name,cur, start):
    var = messagebox.askyesnocancel("Delete?","Delete Patient_id:" + str(t),default='no')
    if var:
        query = "DELETE FROM Patients WHERE Patient_id = ?"
        data = (str(t),)
        conn = cur.execute(query,data)
        messagebox.showerror('Deleted?','Number of row deleted :'+ str(conn.rowcount))
        pres_db.commit()
    # to refresh table
    Display_patients(win,tb_name,cur,start)
    return
def Edit(t,row_num, window,tablename,cursor, start):
    
    #Display_patients(window,tablename,cursor)
    print(f"SELECT Patient_id, First_Name, Middle_Initial, Last_Name, Gender, Age, Email, Phone FROM {tablename}  where Patient_id = ?",(t,))
    r = cursor.execute(f"SELECT Patient_id, First_Name, Middle_Initial, Last_Name, Gender, Age, Email, Phone FROM {tablename}  where Patient_id = ?",(str(t),))
    s = r.fetchone()
    str_First_Name = StringVar(window)
    str_Middle_Name = StringVar(window)
    str_Last_Name = StringVar(window)
    str_Gender = StringVar(window)
    str_Age = StringVar(window)
    str_Email = StringVar(window)
    str_Phone = StringVar(window)
    str_Patient_id = StringVar(window)
    

    # to store data

    str_Patient_id.set(s[0])
    str_First_Name.set(s[1])
    str_Middle_Name.set(s[2])
    str_Last_Name.set(s[3])
    str_Gender.set(s[4])
    str_Age.set(s[5])
    str_Email.set(s[6])
    str_Phone.set(s[7])

    #print("str_First_Name" + s[0])
    #print("str_Phone" + s[6])
    Entry(window,textvariable=str_Patient_id).grid(row=row_num,column=0)
    Entry(window,textvariable=str_First_Name).grid(row=row_num,column=1)
    Entry(window,textvariable=str_Middle_Name).grid(row=row_num,column=2)
    Entry(window,textvariable=str_Last_Name).grid(row=row_num,column=3)
    Entry(window,textvariable=str_Gender).grid(row=row_num,column=4)
    Entry(window,textvariable=str_Age).grid(row=row_num,column=5)
    Entry(window,textvariable=str_Email).grid(row=row_num,column=6)
    Entry(window,textvariable=str_Phone).grid(row=row_num,column=7)
   
    K=Button(window,text='Update', command= lambda : my_update())
    K.grid(row=row_num,column=9)

    
    def my_update():
        query = f"UPDATE Patients SET First_Name = ?,Middle_Initial = ?,Last_Name =?,Gender=?,Age=?,Email=?,Phone=? WHERE Patient_id = ?"
        data = (str_First_Name.get(), str_Middle_Name.get(), str_Last_Name.get(), str_Gender.get(), str_Age.get(), str_Email.get(), str_Phone.get(),t)
        print("Query : " + query)
        print(data)

        cursor.execute(query, data)
        pres_db.commit()
        Display_patients(window,tablename,cursor,start)
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
    print(f"Check for tableName {tableName}")

    cursor.execute(f"INSERT INTO {tableName} VALUES (?, ?, ?, ?, ?, ?, ?, ?)", entryItems)
    #database.commit()
    if tableName == "Patients":
        patients_db.commit()
    elif tableName == "Prescription_Drugs":
        medical_storage_db.commit()

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
    print(entryItems)
    query= f"SELECT Drug_id FROM pres WHERE Patient_id = {int(entryItems[0])}"
    current_product_ids =  [item[0] for item in cursor.execute(query).fetchall()]
    #print(dir(current_product_ids))
    #print(f"Current products - {current_product_ids}")
    if current_product_ids:
        #print("Products presetn")
        if entryItems[1] in current_product_ids:
            query=f"select Quantity FROM pres WHERE Drug_id= '{entryItems[1]}'"
            current_quantity = [item[0] for item in cursor.execute(query).fetchall()]
            #print(current_quantity[0])
            new_quantity = current_quantity[0] + int(entryItems[2])
            #print(f"New quantity {new_quantity}")
            query = f"UPDATE {tableName} SET Quantity = {new_quantity} WHERE Drug_id = '{entryItems[1]}'"
            cursor.execute(query)
        else:
            cursor.execute(f"INSERT INTO {tableName} (Patient_id,Drug_id,Quantity) VALUES (?, ?, ?)", entryItems)
    else:
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

create_login()

root.mainloop()
