import sqlite3
from sqlite3.dbapi2 import Error

class db:
    def __init__(self):
        try:
            self.con = sqlite3.connect('/db/comp.db')
            self.cur = self.con.cursor()
        except Error as e:
            print(e)

    def create_table(self):
        try:
            self.cur.execute('''CREATE TABLE lists (name text, list text, UNIQUE(name) ON CONFLICT REPLACE)''')
        except:
            pass

    def insert(self, name, body):
        # try:
        print(name, body)
        self.cur.execute("INSERT INTO lists VALUES (?, ?)", (name, body))
        self.con.commit()
        self.cur.close()
        print("Insert successfull")
        # except:
        #     print("Failed to insert")

    def delete(self, name):
        self.cur.execute("DELETE FROM lists WHERE name=(?)", (name,))
        self.con.commit()
        self.cur.close()
        print("Delete successfull")

    def select_complist(self):
        # try:
        complist = []
        for list in self.cur.execute("SELECT name FROM lists").fetchall():
            complist.append(list[0])
            print(list)
        self.cur.close()
        return complist
        # except Error as e:
        #     print(e)

    def select_list(self, name):
        # try:
        result= self.cur.execute("SELECT list FROM lists WHERE name=(?)", (name,)).fetchall()
        self.cur.close()

        return result[0][0]
        # except:
        #     print("Failed to select a list")