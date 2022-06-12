import sqlite3
from sqlite3 import Error

class TodosSQLite:
    def __init__(self, db_file):
        self.db_file = db_file     

    def all(self):
        with self.create_connection() as conn:
            return self.select_all(conn, "tasks")   

    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
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

    def add_task(self, zadanie):
        sql = '''INSERT INTO tasks(task_id, title, description, status)
             VALUES(?,?,?,?)'''
        with self.create_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql, zadanie)
            conn.commit()       

    def select_all(self, conn, table):
        with self.create_connection() as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM {table}")
            rows = cur.fetchall()
            return rows

    def select_where(self, table, **query):
        with self.create_connection() as conn:
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

    def update(self, table, id, **kwargs):
        parameters = [f"{k} = ?" for k in kwargs]
        parameters = ", ".join(parameters)
        values = tuple(v for v in kwargs.values())
        values += (id, )

        sql = f''' UPDATE {table}
             SET {parameters}
             WHERE id = ?'''
        with self.create_connection() as conn:
            try:
                cur = conn.cursor()
                cur.execute(sql, values)
                conn.commit()
                print("OK")
            except sqlite3.OperationalError as e:
                print(e)
        
    def delete_where(self, table, **kwargs):
        qs = []
        values = tuple()
        for k, v in kwargs.items():
            qs.append(f"{k}=?")
            values += (v,)
        q = " AND ".join(qs)

        sql = f'DELETE FROM {table} WHERE {q}'
        with self.create_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql, values)
            conn.commit()
            print("Deleted")
        

todos = TodosSQLite("todos.db")