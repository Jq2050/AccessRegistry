#Keeping a record of people accesing a building
import sqlite3
from datetime import datetime

#Creating a data base
database = "prueba.db"
conn = sqlite3.connect(database)
#A cursor let's me executeSQL commands in the BDD
cur = conn.cursor()
#Create a data base only if it does not exist
cur.execute('''CREATE TABLE IF NOT EXISTS people (first_name TEXT NOT NULL, last_name TEXT NOT NULL,
            cedula TEXT PRIMARY KEY NOT NULL, in_date TEXT NOT NULL,
            in_time TEXT NOT NULL, out_date TEXT NOT NULL, out_time TEXT NOT NULL)''')

#Inserting a new record
def InsertRow():
    data = []  # Initialize an empty (vector) list to store the data
    name = input("Enter your name: ") #need to validate data
    LastName = input("Enter your last name: ") #need to validate data
    ID = int(input("Enter your ID: ")) #change to char
    # Fecha y hora actual
    current_datetime = datetime.now()
    # Separar fecha y hora
    current_date = current_datetime.date().strftime('%Y-%m-%d')
    current_time = current_datetime.time().strftime('%H:%M:%S')
    # Create a new time object with seconds as an integer, I dont need it because now it is a string
    #current_time_integer = current_time.replace(microsecond=0)
    # Out date
    out_date = None
    # Out time
    out_time = None
    # Create a tuple with the provided data in the list
    Ingreso = (name,LastName,ID,current_date,current_time,out_date,out_time)
    data.append(Ingreso)
    #instruccion = f"INSERT INTO people VALUES ('{name}','{LastName}',{ID},'{current_date}','{current_time_integer}','{out_date}','{out_time}')"
    #cur.execute(instruccion)
    instruccion = "INSERT INTO people (first_name, last_name,cedula, in_date, in_time, out_date, out_time) VALUES (?, ?, ?, ?, ?, ?, ?);"
 #   cur.execute(instruccion, (name,LastName,ID,current_date,current_time_integer,out_date,out_time))
    cur.execute(instruccion, (Ingreso))
    conn.commit()

#Query to get all records
def ReadTable():
    cur.execute("SELECT * FROM people")
#    print(cur.fetchall())
    rows = cur.fetchall()
    for row in rows:
        print(row)

#Query to get people who is still inside the building
def ReadOutEmpty():
    cur.execute("SELECT * FROM people WHERE out_time IS NULL")
    print(cur.fetchall())

#Record people's get out time
def InsertOut():
    current_datetime = datetime.now()
    out_date = current_datetime.date().strftime('%Y-%m-%d')
    out_time = current_datetime.time().strftime('%H:%M:%S')   
    LastName = input("Apellido de quien va a salir: ")
    instruccion = "UPDATE people SET out_date = ?, out_time = ? WHERE Last_Name = ? AND out_date IS NULL;"
    cur.execute(instruccion, (out_date, out_time, LastName))

#Our main menu
def main_menu():
    while True:
        print("Main Menu")
        print("1. Ingresar visitante")
        print("2. Consultar BDD")
        print("3. Quien no sale?")
        print("4. Registrar salida")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            InsertRow()
        elif choice == '2':
            ReadTable()
        elif choice == '3':
            ReadOutEmpty()
        elif choice == '4':
            InsertOut()
        elif choice == '5':
            print("Exiting...")
            cur.close()
            conn.close()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()