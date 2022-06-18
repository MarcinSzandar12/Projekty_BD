from sqlalchemy import create_engine, MetaData, Integer, Float, String, Date, Table, Column
from convert import csv_to_json

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

data = csv_to_json("C:\Users\SzandY\Desktop\Kodilla\Projekty_BD\13.3\clean_stations.csv", "clean_stations.json")

conn = engine.connect()

result = conn.execute("SELECT * FROM stations LIMIT 5").fetchall()

for row in result:
    print(row)