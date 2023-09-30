import Data_read
import csv
import time, datetime

bus = Data_read.bus_start()
date = datetime.datetime.today()
minute = date.minute

while True:
	date = datetime.datetime.today()
	if minute is not date.minute:
		Data_read.collect_start(bus)
		time.sleep(1)
		temp_comp = Data_read.collect_temp(bus)
		hum_comp = Data_read.collect_humid(bus, temp_comp)
		date = datetime.datetime.today()
		minute = date.minute
		with open('data/data_temp_humid_2.csv', 'a') as file:
			writer = csv.writer(file)
			writer.writerow([time.time(), temp_comp/100, hum_comp/10000])
		#print(temp_comp/100)
		#print(hum_comp/10000)
	time.sleep(10)
