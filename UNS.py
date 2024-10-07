import platform
import socket
import getpass
import paho.mqtt.client as mqtt
import json

ROOT_TOPIC = "uns/jpn/xxx/xxx/xxx"


def generate_descripive_namespace():
    descriptive_info = {
        "name": "xxx",
        "role": "Tech Analyst",
        "Username": getpass.getuser(),
        "system": platform.system(),
        "release": platform.release(),
        "hostname": socket.gethostname(),
        "ip_address": socket.gethostbyname((socket.gethostname())),
        "location": "xxx,xxx"
    }
    return descriptive_info


def generate_functional_namespace():
    functional_info = {
        "process": "example_process",
        "status": "running",
        "timestamp": "2024-10-05T11:03:00Z"
    }
    return functional_info


def generate_informative_namespace():
    informative_info = {
        "message": "System running smoothly",
        "alerts": [],
        "uptime": "24 hours"
    }
    return informative_info


def publish_namespace(client, namespace, topic_suffix):
    namespace_json = json.dumps(namespace)
    full_topic = f"{ROOT_TOPIC}/{topic_suffix}"
    client.publish(full_topic, namespace_json)
    print(f"Published to {full_topic}:{namespace_json}")


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected {mqtt_broker} with result code {rc}")
        client.subscribe(f"{ROOT_TOPIC}/#")

        publish_namespace(client, descripive_namespace, "descriptive")
        publish_namespace(client, functional_namespace, "functional")
        publish_namespace(client, informative_namespace, "informative")
    else:
        print(f"Bad connection returned code={rc}")


def on_message(client, userdata, msg):
    print(f"Received message from {msg.topic}:{msg.payload.decode()}")


if __name__ == "__main__":
    descripive_namespace = generate_descripive_namespace()
    functional_namespace = generate_functional_namespace()
    informative_namespace = generate_informative_namespace()

    print(f"Generated Descriptive Namespace:{descripive_namespace}")
    print(f"Generated Functional Namespace:{functional_namespace}")
    print(f"Generated Informative Namespace:{informative_namespace}")

    # mqtt_broker = "144.202.65.194"
    mqtt_broker = "mqtt.eclipseprojects.io"
    mqtt_port = 1883

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(mqtt_broker, mqtt_port, 60)

    client.loop_forever()
