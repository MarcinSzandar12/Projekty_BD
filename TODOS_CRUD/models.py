import json
import sqlite3
from sqlite3 import Error

class TodosSQLite:
    def __init__(self):
        try:
            with open("todos.json", "r") as f:
                self.todos = json.load(f)
        except FileNotFoundError:
            self.todos = []

    def all(self):
        return self.todos     

    def create_connection(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)

        return conn

    def create_connection_in_memory():
        conn = None
        try:
            conn = sqlite3.connect(":memory:")
            print(f"Connected, sqlite version: {sqlite3.version}")
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def save_all(self):
        with open("todos.json", "w") as f:
            json.dump(self.todos, f)

    def add_task(self, conn, zadanie):
        sql = '''INSERT INTO tasks(Zadanie_id, tytuł, opis, status)
             VALUES(?,?,?,?)'''
        cur = conn.cursor()
        cur.execute(sql, zadanie)
        conn.commit()
        self.save_all()        

    def select_all(conn, table):
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table}")
        rows = cur.fetchall()
        return rows

    def select_where(conn, table, **query):
        cur = conn.cursor()
        qs = []
        values = ()
        for k, v in query.items():
            qs.append(f"{k}=?")
            values += (v,)
        q = " AND ".join(qs)
        cur.execute(f"SELECT * FROM {table} WHERE {q}", values)
        rows = cur.fetchall()
        return rows

    def update(self, conn, table, id, **kwargs):
        parameters = [f"{k} = ?" for k in kwargs]
        parameters = ", ".join(parameters)
        values = tuple(v for v in kwargs.values())
        values += (id, )

        sql = f''' UPDATE {table}
             SET {parameters}
             WHERE id = ?'''
        try:
            cur = conn.cursor()
            cur.execute(sql, values)
            conn.commit()
            self.save_all()
            print("OK")
        except sqlite3.OperationalError as e:
            print(e)
        
    def delete_where(self, conn, table, **kwargs):
        qs = []
        values = tuple()
        for k, v in kwargs.items():
            qs.append(f"{k}=?")
            values += (v,)
        q = " AND ".join(qs)

        sql = f'DELETE FROM {table} WHERE {q}'
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        self.save_all()
        print("Deleted")
        

todos = TodosSQLite()