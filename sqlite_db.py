import sqlite3, csv

conn = sqlite3.connect('medical_storage_1000.db') 
cur = conn.cursor()

cur.execute("CREATE TABLE Prescription_Drugs (Product_Number, Non_Proprietary_Name, Manufacturer, Dosage, Unit, Category_Description, Price, Quantity);") # use your column names here

with open('product_1000.csv','r') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['Product_Number'], i['Non_Proprietary_Name'], i['Manufacturer'], i['Dosage'], i['Unit'], i['Category_Description'], i['Price'], i['Quantity']) for i in dr]

cur.executemany("INSERT INTO Prescription_Drugs (Product_Number, Non_Proprietary_Name, Manufacturer, Dosage, Unit, Category_Description, Price, Quantity) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)
conn.commit()
conn.close()