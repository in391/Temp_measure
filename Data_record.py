import Data_read
import csv
import time

bus = Data_read.bus_start()
Data_read.collect_start(bus)
time.sleep(1)

temp_comp = Data_read.collect_temp(bus)
hum_comp = Data_read.collect_humid(bus, temp_comp)
with open('data/data_temp_humid_3.csv', 'a') as file:
	writer = csv.writer(file)
	writer.writerow([time.time(), temp_comp/100, hum_comp/10000])
