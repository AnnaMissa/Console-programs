'''
File handling with Python 2.7
Program checks files in directory "IN".
File name has the format: [user name][processing method][file ID].txt
Processing method must be "ZIP" or "UTF".
If user name exists in database and file has correct format/method,
program processes the file and adds it to directory "OUT".
The result of each operation is saved in history (in database).
'''


import sqlite3
import os
from datetime import datetime
from zipfile import ZipFile


class Database:
    def __init__(self, namebase):
        self.namebase = namebase

    def connect(self):
        con = sqlite3.connect(self.namebase)
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name VARCHAR(20))")
        con.commit()
        cur.execute("CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_name VARCHAR(20), "
                    "process VARCHAR(20), file_name VARCHAR(20), date VARCHAR(20), status VARCHAR(20))")
        con.commit()
        return con, cur

    def disconnect(self, con):
        con.close()

    def create_user(self, name, con, cur):
        cur.execute("INSERT INTO user (name) VALUES(?)", (name, ))
        con.commit()
        print "User create"

    def delete_user(self, name, con, cur):
        cur.execute("DELETE FROM user WHERE name=?", (name, ))
        con.commit()
        print "User delete"

    def search(self, cur, user):
        cur.execute("SELECT name FROM user WHERE name=?", (user,))
        if len(cur.fetchall()) != 0:
            return True
        else:
            return False

    def add_history(self, user, proc, file_name, status, con, cur):
        date = datetime.strftime(datetime.now(), "%Y.%m.%d")
        item = (user, proc, file_name, date, status)
        cur.execute("INSERT INTO history (user_name, process, file_name, date, status) "
                    "VALUES(?,?,?,?,?)", item)
        con.commit()

    def show_history(self, cur):
        cur.execute("SELECT * FROM history")
        print "History:"
        for row in cur.fetchall():
            print "ID: {:<3} USER: {:7} PROCESS: {:12} FILE NAME: {:15} DATE: {:12}" \
                  "STATUS: {:20}".format(row[0], row[1], row[2], row[3], row[4], row[5])

    def clear_history(self, cur, con):
        cur.execute("DELETE FROM history")
        con.commit()
        print "History cleared"


class Files:
    def __init__(self, title):
        self.title = title

    def delete_file(self):
        os.remove(path + "IN" + "\\" + self.title)

    def zip_file(self):
        z = ZipFile(path + "OUT" + "\\" + self.title[:-4] + ".zip", 'w')
        z.write(os.path.join(path + "IN", self.title))
        z.close()

    def utf_file(self):
        f = open(path + "IN" + "\\" + self.title, "r")
        text = f.read().decode("cp1251")
        text = text.encode("utf8")
        file = open(path + "OUT" + "\\" + self.title, "w")
        file.write(text)
        file.close()
        f.close()

    def check(self, database, con, cur):
        if self.title.find("ZIP") != -1:
            user = self.title[:self.title.find("ZIP")]
            proc = "ZIP"
        elif self.title.find("UTF") != -1:
            user = self.title[:self.title.find("UTF")]
            proc = "UTF"
        else: #error in mode
            database.add_history("admin", "error method", self.title, "not executed, delete file", con, cur)
            return False
        if database.search(cur, user):
            database.add_history(user, proc, self.title, "done", con, cur) #must be after procces !!!
            return proc
        else: #error user
            database.add_history("admin", "error user", self.title, "not executed, delete file", con, cur)
            return False


class Work:
    def dialog(self):
        try:
            op = 0
            op = input("\nEnter the number of the action:"
                       "\nStart work - 1"
                       "\nCreate user - 2"
                       "\nDelete user - 3"
                       "\nShow history - 4"
                       "\nClear all history - 5"
                       "\nQuit - 6"
                       "\n>>> ")
        except NameError:
            print "Error. Need to enter the number."
        else:
            if not 0 < op < 7:
                print "Error. The number must be from 1 to 6"
        return op

    def action(self, op, database, con, cur):
        if op == 1:
            for el in os.listdir(path + "IN"):
                obj = Files(el)
                proc = obj.check(database, con, cur)
                if proc == "ZIP":
                    obj.zip_file()
                elif proc == "UTF":
                    obj.utf_file()
                obj.delete_file()
            print "Done!"
        elif op == 2:
            uname = raw_input("Enter the user name to create:"
                              "\n>>> ")
            database.create_user(uname, con, cur)
        elif op == 3:
            uname = raw_input("Enter the user name to delete:"
                              "\n>>> ")
            database.delete_user(uname, con, cur)
        elif op == 4:
            database.show_history(cur)
        elif op == 5:
            database.clear_history(cur, con)


path = os.path.relpath("D:\GitHub\Console-programs\File_handling") + "\\"
a = Work()
database = Database("change_history.db")
con, cur = database.connect()
while True:
    op = a.dialog()
    if op == 6:
        print "Good bye!"
        break
    elif 0 < op <6:
        a.action(op, database, con, cur)
    y = raw_input("\nYou want to continue?"
                  "\nIf so, enter Y:"
                  "\n>>> ")
    if not (y == "Y" or y == "y"):
        print "Good bye!"
        break
database.disconnect(con)