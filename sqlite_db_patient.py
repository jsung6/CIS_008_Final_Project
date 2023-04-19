import sqlite3, csv

conn = sqlite3.connect('patients.db') 
cur = conn.cursor()

cur.execute("CREATE TABLE Patients (First_Name, Middle_Initial, Last_Name, Gender, Age, Email, Phone, Prescriptions);") # use your column names here

with open('patients.csv','r') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['First_Name'], i['Middle_Initial'], i['Last_Name'], i['Gender'], i['Age'], i['Email'], i['Phone'], i['Prescriptions']) for i in dr]

cur.executemany("INSERT INTO Patients (First_Name, Middle_Initial, Last_Name, Gender, Age, Email, Phone, Prescriptions) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)
conn.commit()
conn.close()