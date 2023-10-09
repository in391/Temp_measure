# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awscrt import mqtt5
from awsiot import mqtt5_client_builder 
from uuid import uuid4
import threading
from concurrent.futures import Future
import json

TIMEOUT = 10
message_topic = "sdk/test/python"
message_dict = {
    "Timestamp": 712389215,
    "Client": 2,
    "Gas": 123.213,
    "Humid": 345.12,
    "Temp": 123.123
}
message_string = message_dict
received_count = 0
received_all_event = threading.Event()
future_stopped = Future()
future_connection_success = Future()

# Callback when any publish is received
def on_publish_received(publish_packet_data):
    publish_packet = publish_packet_data.publish_packet
    assert isinstance(publish_packet, mqtt5.PublishPacket)
    print("Received message from topic'{}':{}".format(publish_packet.topic, publish_packet.payload))
    # global received_count
    # received_count += 1
    # if received_count == 10:
    #     received_all_event.set()
    received_all_event.set()

# Callback for the lifecycle event Stopped
def on_lifecycle_stopped(lifecycle_stopped_data: mqtt5.LifecycleStoppedData):
    print("Lifecycle Stopped")
    global future_stopped
    future_stopped.set_result(lifecycle_stopped_data)

# Callback for the lifecycle event Connection Success
def on_lifecycle_connection_success(lifecycle_connect_success_data: mqtt5.LifecycleConnectSuccessData):
    print("Lifecycle Connection Success")
    global future_connection_success
    future_connection_success.set_result(lifecycle_connect_success_data)


# Callback for the lifecycle event Connection Failure
def on_lifecycle_connection_failure(lifecycle_connection_failure: mqtt5.LifecycleConnectFailureData):
    print("Lifecycle Connection Failure")
    print("Connection failed with exception:{}".format(lifecycle_connection_failure.exception))

aws_endpoint = "anpb1w2ol50zo-ats.iot.ap-northeast-1.amazonaws.com"
aws_port = 8883
aws_client_id = "home-surface-jsdfiod"
# X.509 based certificate file
certificate_file_path = "C:/Users/Surface/Documents/Project/awsiot/connect_device_package/home-surface.cert.pem"
# PKCS#1 or PKCS#8 PEM encoded private key file
private_key_filePath = "C:/Users/Surface/Documents/Project/awsiot/connect_device_package/home-surface.private.key"

client = mqtt5_client_builder.mtls_from_path(
    endpoint=aws_endpoint,
    port=aws_port,
    cert_filepath=certificate_file_path,
    pri_key_filepath=private_key_filePath,
    http_proxy_options=None,
    on_publish_received=on_publish_received,
    on_lifecycle_stopped=on_lifecycle_stopped,
    on_lifecycle_connection_success=on_lifecycle_connection_success,
    on_lifecycle_connection_failure=on_lifecycle_connection_failure,
    client_id=aws_client_id)

print("MQTT5 Client Created")
client.start()
lifecycle_connect_success_data = future_connection_success.result(TIMEOUT)
connack_packet = lifecycle_connect_success_data.connack_packet
negotiated_settings = lifecycle_connect_success_data.negotiated_settings

publish_future = client.publish(mqtt5.PublishPacket(
    topic=message_topic,
    payload=json.dumps(message_string),
    qos=mqtt5.QoS.AT_LEAST_ONCE
))

publish_completion_data = publish_future.result(TIMEOUT)
print("PubAck received with {}".format(repr(publish_completion_data.puback.reason_code)))

print("Stopping Client")
client.stop()

future_stopped.result(TIMEOUT)
print("Client Stopped!")