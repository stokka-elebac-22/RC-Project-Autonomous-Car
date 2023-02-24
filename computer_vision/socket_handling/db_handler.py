import sqlite3

from abstract_storage import abstract_storage

class db_handler(abstract_storage):
    
    def __init__(self, db_name):
        self.db_name = db_name 
        self.create_project_tables()
        
    def add_log(self, pos, sensor_type, value, timestamp=0):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        if timestamp == 0:
            sqlite_insert_with_param  = "INSERT INTO sensor \
                (position, sensor_type, value) VALUES(?, ?, ?);"
            data_tuple = (pos, sensor_type, value)
        else:
            sqlite_insert_with_param  = "INSERT INTO sensor \
                (position, sensor_type, value, timestamp) VALUES(?, ?, ?, ?);"
            data_tuple = (pos, sensor_type, value, timestamp)
        cur.execute(sqlite_insert_with_param, data_tuple)
        conn.commit()

    def create_project_tables(self):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS sensor( \
            ID INTEGER PRIMARY KEY, \
            position INT, \
            sensor_type INT, \
            value int, \
            Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP )")
        conn.commit
    
    def get_sensor_data(self, pos, sensor_type):
        conn = sqlite3.connect(self.db_name)        
        cur = conn.cursor()
        cur.execute("SELECT timestamp, value FROM sensor \
            WHERE position=? and sensor_type=?", (pos, sensor_type))
        rows = cur.fetchall()
        return rows
    
    def get_recent_sensor_data(self):
        conn = sqlite3.connect(self.db_name, uri=True)
        cur = conn.cursor()
        cur.execute("SELECT position, sensor_type, value, timestamp FROM sensor \
            GROUP BY position, sensor_type ORDER BY MAX(timestamp)", ())
        rows = cur.fetchall()
        return rows
        # SELECT DISTINCT position, sensor_type FROM sensor \

if __name__ == "__main__":
    database = db_handler(":memory:")
    # database = db_handler("db_file.db")
    for x in range(100):
        database.add_log(1,0,x, 0)
    for row in database.get_recent_sensor_data():
        print(row)        
    for row in database.get_sensor_data(1,0):
        print(row)

