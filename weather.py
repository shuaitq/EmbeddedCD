import Adafruit_DHT
import sqlite3
from apscheduler.schedulers.blocking import BlockingScheduler
import time
import sys
import math
def job():
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
    print(humidity, temperature)
    if humidity <= 100 and humidity >= 5 and temperature >= 5:
        cursor.execute('insert into weather (humidity, temperature) values (?, ?)', (humidity, temperature))
    cursor.close()
    conn.commit()
    conn.close()

def run():
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'cron', second = '*/10')
    scheduler.start()

def show():
    cursor.execute('select * from weather')
    for row in cursor:
        print(row)

def create():
    cursor.execute('''create table weather (id integer primary key autoincrement not null,
                                            time timestamp default current_timestamp not null,
                                            humidity float not null,
                                            temperature float not null)''')
    conn.commit()

if len(sys.argv) == 1:
    run()
else:
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    if sys.argv[1] == 'show':
        show()
    elif sys.argv[1] == 'create':
        create()
    else:
        print('Error!')
    cursor.close()
    conn.commit()
    conn.close()
