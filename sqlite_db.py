import sqlite3, csv

conn = sqlite3.connect('medical_storage_20.db') 
cur = conn.cursor()

cur.execute("CREATE TABLE t (Product_Number, Proprietary_Name, Non_Proprietary_Name, Dosage_Form, Delivery, Manufacturer, Substance_Name, Dosage, Unit, Category_Description, Price, Quantity);") # use your column names here

with open('product_20.csv','r') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['Product_Number'], i['Proprietary_Name'], i['Non_Proprietary_Name'], i['Dosage_Form'], i['Delivery'], i['Manufacturer'], i['Substance_Name'], i['Dosage'], i['Unit'], i['Category_Description'], i['Price'], i['Quantity']) for i in dr]

cur.executemany("INSERT INTO t (Product_Number, Proprietary_Name, Non_Proprietary_Name, Dosage_Form, Delivery, Manufacturer, Substance_Name, Dosage, Unit, Category_Description, Price, Quantity) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
conn.commit()
conn.close()