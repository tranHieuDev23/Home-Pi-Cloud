import json
from datetime import datetime
from threading import Thread
from paho.mqtt.client import Client
from models.status_log import StatusLog
from daos.device_dao import DeviceDAO
from daos.status_log_dao import StatusLogDAO


class StatusListener:
    def __init__(self, mqtt_host, mqtt_port, mqtt_username, mqtt_password):
        self.__device_dao = DeviceDAO()
        self.__log_dao = StatusLogDAO()
        self.__mqtt_client = Client()
        self.__mqtt_client.on_subscribe = self.on_subscribe
        self.__mqtt_client.on_message = self.on_message
        self.__mqtt_client.connect(mqtt_host, mqtt_port)
        mqtt_thread = Thread(target=self.__mqtt_client.loop_forever)
        mqtt_thread.daemon = True
        mqtt_thread.start()

    def subscribe(self, topic):
        print(topic)
        self.__mqtt_client.subscribe(topic, qos=2)

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print("Subscribed with granted QoS: %s" % str(granted_qos))

    def on_message(self, client, userdata, message):
        timestamp = round(datetime.now().timestamp() * 1000)
        message_json = json.loads(message.payload.decode('utf-8'))
        if ('deviceId' not in message_json or 'fieldName' not in message_json or 'fieldValue' not in message_json):
            return
        device_id = message_json['deviceId']
        device = self.__device_dao.get(device_id)
        if (device_id is None):
            return
        field_name = message_json['fieldName']
        field_value = message_json['fieldValue']
        status_log = StatusLog(
            None, device.id, timestamp, field_name, field_value)
        self.__log_dao.save(status_log)
