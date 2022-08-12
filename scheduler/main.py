from datetime import datetime
import psutil
import schedule
import time

from database import Database
from defaults import SQL_IMPORT_FILE, SQL_DATABASE

database = Database(SQL_DATABASE)
database.import_tables(SQL_IMPORT_FILE)

def get_disk_info():
    data = list(psutil.disk_usage('/'))
    data[0] = data[0] / (2**30)
    data[1] = data[1] / (2**30)
    data[2] = data[2] / (2**30)
    data.append(datetime.now())
    data = tuple(data)
    database.insert_data(table='disk', data=data)

schedule.every(3).seconds.do(get_disk_info)

while True:
    schedule.run_pending()
    time.sleep(1)