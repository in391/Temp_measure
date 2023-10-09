import main_read
import time
from AWS import aws_iot_core_connect

bus = main_read.bus_start()
main_read.collect_start(bus)
time.sleep(1)

timestamp = time.time()
clientId = 1
gas = 0
temp_comp = main_read.collect_temp(bus)
hum_comp = main_read.collect_humid(bus, temp_comp)

message_topic = "pp/temp/add"
message_dict = {
    "Timestamp": timestamp,
    "Client": clientId,
    "Gas": gas,
    "Humid": temp_comp,
    "Temp": hum_comp
}

try:
    client = aws_iot_core_connect.client_create_and_connect()
    aws_iot_core_connect.client_publish_message(client, message_topic, message_dict)
    aws_iot_core_connect.client_stop(client)
except Exception as e:
    print(e)