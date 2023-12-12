import smbus
import time
import main_read

bus = smbus.SMBus(1)
address = 0x77
reg_add = 0x74
operate_data = 0b01000001

add_adc_msb = 0x22
add_adc_lsb = 0x23
add_adc_xlsb= 0x24

add_part_t1_msb = 0xEA
add_part_t1_lsb = 0xE9

add_part_t2_msb = 0x8B
add_part_t2_lsb = 0x8A

add_part_t3 = 0x8C

bus.write_byte_data(address, reg_add, operate_data)
time.sleep(1)

adc = bus.read_byte_data(address, add_adc_msb)
adc = adc << 8
adc += bus.read_byte_data(address, add_adc_lsb)
adc = adc << 4
adc += bus.read_byte_data(address, add_adc_xlsb) >> 4

par_t1 = bus.read_byte_data(address, add_part_t1_msb)
par_t1 = par_t1 << 8
par_t1 += bus.read_byte_data(address, add_part_t1_lsb)

par_t2 = bus.read_byte_data(address, add_part_t2_msb)
par_t2 = par_t2 << 8
par_t2 += bus.read_byte_data(address, add_part_t2_lsb)

par_t3 = bus.read_byte_data(address, add_part_t3)

#print(adc, par_t1, par_t2, par_t3)
#print(hex(adc), hex(par_t1), hex(par_t2), hex(par_t3))

var1 = ((float(adc)/16384.0) - (float(par_t1) / 1024.0)) * float(par_t2)
var2 = (((float(adc) / 131072.0) - (float(par_t1) / 8192.0))*((float(adc)/131072.0) - (float(par_t1)/8192.0)))*(float(par_t3) * 16.0)
t_fine = var1 + var2
temp_comp = t_fine / 5120.0

#print(temp_comp)

var1 = (int(adc) >> 3) - (int(par_t1) << 1);
var2 = (var1*int(par_t2)) >> 11;
var3 = ((((var1 >> 1)*(var1 >> 1)) >> 12) * (int(par_t3) << 4)) >> 14;
t_fine = var2 + var3;
temp_comp = ((t_fine * 5) + 128) >> 8;

print(temp_comp)
hum_comp = main_read.collect_humid(bus, temp_comp)
print(hum_comp)