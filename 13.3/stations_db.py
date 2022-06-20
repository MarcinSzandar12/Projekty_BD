from sqlalchemy import create_engine, MetaData, Integer, Float, String, Date, Table, Column
import csv
import sqlite3

engine = create_engine('sqlite:///database.db', echo=True)

meta = MetaData()

stations = Table(
   'stations', meta,
   Column('station', String, primary_key=True),
   Column('latitude', Float),
   Column('longitude', Float),
   Column('elevation', Float),
   Column('name', String),
   Column('country', String),
   Column('state', String),
)

stations_measure = Table(
    'stations_measure', meta,
    Column('station', String, primary_key=True),
    Column('date', Date),
    Column('precip', Float),
    Column('tobs', Integer),
)

meta.create_all(engine)

conn = sqlite3.connect("database.db")
cur = conn.cursor()

csv_file_1 = open('clean_stations.csv')
csv_file_2 = open('clean_measure.csv')
rows_1 = csv.reader(csv_file_1)
rows_2 = csv.reader(csv_file_2)

cur.executemany("INSERT INTO stations VALUES (?, ?, ?, ?, ?, ?, ?)", rows_1)
cur.executemany("INSERT OR IGNORE INTO stations_measure VALUES (?, ?, ?, ?)", rows_2)

print(conn.execute("SELECT * FROM stations_measure LIMIT 5").fetchall())