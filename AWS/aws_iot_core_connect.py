# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awscrt import mqtt5
from awsiot import mqtt5_client_builder 
from uuid import uuid4
import threading
from concurrent.futures import Future
import json

#Configuration Section
TIMEOUT = 10
AWS_ENDPOINT = "anpb1w2ol50zo-ats.iot.ap-northeast-1.amazonaws.com"
AWS_PORT = 8883
AWS_CLIENT_ID = "home-raspberry-pi-3bp"
# X.509 based certificate file
CERT_FILE_PATH = "~/.key/home-raspberry-pi-3bp.cert.pem"
# PKCS#1 or PKCS#8 PEM encoded private key file
PRI_KEY_FILE_PATH = "~/.key/home-raspberry-pi-3bp.private.key"


received_all_event = threading.Event()
future_stopped = Future()
future_connection_success = Future()

# Callback when any publish is received
def on_publish_received(publish_packet_data):
    publish_packet = publish_packet_data.publish_packet
    assert isinstance(publish_packet, mqtt5.PublishPacket)
    print("Received message from topic'{}':{}".format(publish_packet.topic, publish_packet.payload))
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

# Create Client
def client_create_and_connect():
    client = mqtt5_client_builder.mtls_from_path(
        endpoint=AWS_ENDPOINT,
        port=AWS_PORT,
        cert_filepath=CERT_FILE_PATH,
        pri_key_filepath=PRI_KEY_FILE_PATH,
        http_proxy_options=None,
        on_publish_received=on_publish_received,
        on_lifecycle_stopped=on_lifecycle_stopped,
        on_lifecycle_connection_success=on_lifecycle_connection_success,
        on_lifecycle_connection_failure=on_lifecycle_connection_failure,
        client_id=AWS_CLIENT_ID)
    
    client.start()
    lifecycle_connect_success_data = future_connection_success.result(TIMEOUT)
    # connack_packet = lifecycle_connect_success_data.connack_packet
    # negotiated_settings = lifecycle_connect_success_data.negotiated_settings
    print("Client is Created")
    
    return client

# Publish Message
def client_publish_message(client, message_topic, message_string):
    publish_future = client.publish(mqtt5.PublishPacket(
        topic=message_topic,
        payload=json.dumps(message_string),
        qos=mqtt5.QoS.AT_LEAST_ONCE
    ))
    publish_completion_data = publish_future.result(TIMEOUT)
    return publish_completion_data

# Terminate Client
def client_stop(client):
    print("Stopping Client")
    client.stop()

    future_stopped.result(TIMEOUT)
    print("Client Stopped!")

    return