import sqlite3, csv

conn = sqlite3.connect('users.db') 
cur = conn.cursor()

cur.execute("CREATE TABLE Users (Username, Password, First_Name, Middle_Initial, Last_Name, Gender, Birthdate, Role, Email, Phone, Address, City, State, Zipcode);") # use your column names here

with open('users.csv','r') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['Username'], i['Password'], i['First_Name'], i['Middle_Initial'], i['Last_Name'], i['Gender'], i['Birthdate'], i['Role'], i['Email'], i['Phone'], i['Address'], i['City'], i['State'], i['Zipcode']) for i in dr]

cur.executemany("INSERT INTO Users (Username, Password, First_Name, Middle_Initial, Last_Name, Gender, Birthdate, Role, Email, Phone, Address, City, State, Zipcode) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
conn.commit()
conn.close()