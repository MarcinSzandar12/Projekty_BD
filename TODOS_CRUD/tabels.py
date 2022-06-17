from sqlite3 import Error
from models import todos

def execute_sql(conn, sql):
   """ Execute sql
   :param conn: Connection object
   :param sql: a SQL script
   :return:
   """
   try:
       c = conn.cursor()
       c.execute(sql)
   except Error as e:
       print(e)

if __name__ == "__main__":
    
   create_tasks_sql = """
   -- task table
   CREATE TABLE IF NOT EXISTS tasks (
      task_id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
      title VARCHAR(250) NOT NULL,
      description TEXT,
      status VARCHAR(15) NOT NULL
   );
   """

   db_file = "todos.db"

   conn = todos.create_connection()
   if conn is not None:
       execute_sql(conn, create_tasks_sql)
       conn.close()

