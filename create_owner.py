import sqlite3


connection = sqlite3.connect("../sqlite.db")
cursor     = connection.cursor()
filename   = r"C:\Users\JasonGarcia24\FINTECH\workspace\fantasy-five\data\aave.sqlite"

file    =  open(filename, "r")
sql_str = file.read()
cursor.executescript(sql_str)

breakpoint()
for row in cursor.execute("SELECT * FROM bitcoin"):\
    print(row)


