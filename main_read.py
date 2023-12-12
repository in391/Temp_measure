import smbus
import time

address = 0x77

def bus_start():
	return smbus.SMBus(1)

def collect_start(bus):
	reg_add = 0x74
	operate_data = 0b01000001

	bus.write_byte_data(address, reg_add, operate_data)
	time.sleep(1)
	return bus

def collect_temp(bus):
	#Temp Collection
	add_adc_msb = 0x22
	add_adc_lsb = 0x23
	add_adc_xlsb= 0x24
	add_part_t1_msb = 0xEA
	add_part_t1_lsb = 0xE9
	add_part_t2_msb = 0x8B
	add_part_t2_lsb = 0x8A
	add_part_t3 = 0x8C

	temp_adc = bus.read_byte_data(address, add_adc_msb)
	temp_adc = temp_adc << 8
	temp_adc += bus.read_byte_data(address, add_adc_lsb)
	temp_adc = temp_adc << 4
	temp_adc += bus.read_byte_data(address, add_adc_xlsb) >> 4

	par_t1 = bus.read_byte_data(address, add_part_t1_msb)
	par_t1 = par_t1 << 8
	par_t1 += bus.read_byte_data(address, add_part_t1_lsb)
	par_t2 = bus.read_byte_data(address, add_part_t2_msb)
	par_t2 = par_t2 << 8
	par_t2 += bus.read_byte_data(address, add_part_t2_lsb)
	par_t3 = bus.read_byte_data(address, add_part_t3)
	
	#Temp Calculation
	var1 = (int(temp_adc) >> 3) - (int(par_t1) << 1)
	var2 = (var1*int(par_t2)) >> 11
	var3 = ((((var1 >> 1)*(var1 >> 1)) >> 12) * (int(par_t3) << 4)) >> 14
	t_fine = var2 + var3
	temp_comp = ((t_fine * 5) + 128) >> 8
	
	return temp_comp

def collect_humid(bus, temp_comp):
	#Humid Collection
	hum_adc_msb = 0x25
	hum_adc_lsb = 0x26
	hum_par_h1_msb = 0xE3
	hum_par_h1_lsb = 0xE2
	hum_par_h2_msb = 0xE1
	hum_par_h2_lsb = 0xE2
	hum_par_h3 = 0xE4
	hum_par_h4 = 0xE5
	hum_par_h5 = 0xE6
	hum_par_h6 = 0xE7
	hum_par_h7 = 0xE8

	hum_adc = bus.read_byte_data(address, hum_adc_msb)
	hum_adc = hum_adc << 8
	hum_adc += bus.read_byte_data(address, hum_adc_lsb)

	par_h1 = bus.read_byte_data(address, hum_par_h1_msb)
	par_h1 = par_h1 << 4
	par_h1 += bus.read_byte_data(address, hum_par_h1_lsb) >> 4
	par_h2 = bus.read_byte_data(address, hum_par_h2_msb)
	par_h2 = par_h2 << 4
	par_h2 += bus.read_byte_data(address, hum_par_h2_lsb) >> 4
	par_h3 = bus.read_byte_data(address, hum_par_h3)
	par_h4 = bus.read_byte_data(address, hum_par_h4)
	par_h5 = bus.read_byte_data(address, hum_par_h5)
	par_h6 = bus.read_byte_data(address, hum_par_h6)
	par_h7 = bus.read_byte_data(address, hum_par_h7)
	
	#Humid Calculation
	temp_comp = int(temp_comp)
	var1 = int(hum_adc) - int(int(par_h1) << 4) - (int(temp_comp * int(par_h3) / 100) >> 1)
	var2 = int(par_h2) * int(((temp_comp * int(par_h4)) / 100) + ((int(temp_comp * ((temp_comp * int(par_h5)) / 100)) >> 6) / 100 + (1 << 14))) >> 10
	var3 = var1 * var2
	var4 = int((int(par_h6) << 7) + (temp_comp * int(par_h7) / 100)) >> 4
	var5 = int((var3 >> 14) * (var3 >> 14)) >> 10
	var6 = int(var4 * var5) >> 1
	hum_comp = int(var3 + var6) >> 12
	hum_comp = int((int(var3 + var6) >> 10) * 1000) >> 12

	return hum_comp
