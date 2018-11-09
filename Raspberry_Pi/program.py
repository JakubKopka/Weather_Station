import MySQLdb
import datetime
from datetime import datetime
import bme280
import sys
import time

now = datetime.now()
last_minute = 0
while True:
    if last_minute != now.minute and now.minute%3==0:
        print now.minute
        last_minute = now.minute
        try:
            db = MySQLdb.connect(host="",  # your host, usually localhost
                                user="",  # your username
                                passwd="",  # your password
                                db="")  # name of the data base
            cur = db.cursor()
            temperature, pressure, humidity = bme280.readBME280All()
            data = datetime.now().strftime("%Y-%m-%d %H:%M")
            cur.execute("INSERT INTO stacjapogodowa_odczyty"
                           "(data_odczytu, temperatura, wilgotnosc, cisnienie) "
                           "VALUES (%s, %s,%s, %s)",
                           (data, temperature, humidity, pressure))
            db.commit()
        except Exception as ex:
            print("Blad! ", ex)
            cur.close()
            db.close()
        last_minute = now.minute
    now = datetime.now()


