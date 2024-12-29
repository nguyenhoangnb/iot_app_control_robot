import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt
import paho.mqtt.client as mqtt

# MQTT Broker Configuration
BROKER = "192.168.1.114"
PORT = 1883
TOPIC_LIGHT = "home/light"
TOPIC_FAN = "home/fan"
TOPIC_LIGHT_STATUS = "home/light/status"
TOPIC_FAN_STATUS = "home/fan/status"

# Create MQTT Client and Connect
def connect_mqtt(userdata):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            client.subscribe([(TOPIC_LIGHT_STATUS, 0), (TOPIC_FAN_STATUS, 0)])
        else:
            print(f"Failed to connect, return code {rc}")
    
    def on_message(client, userdata, msg):
        topic = msg.topic
        message = msg.payload.decode()
        print(f"Received message '{message}' on topic '{topic}'")
        
        if topic == TOPIC_LIGHT_STATUS:
            userdata.update_light_status(message)
        elif topic == TOPIC_FAN_STATUS:
            userdata.update_fan_status(message)

    client = mqtt.Client('Qt6DeviceController')
    client.on_connect = on_connect
    client.on_message = on_message
    client.user_data_set(userdata)  # Set userdata to the DeviceControlApp instance
    client.connect(BROKER, PORT)
    client.loop_start()  # Start loop in background
    return client

# Send command to device
def send_command(client, topic, command):
    if client.is_connected():
        client.publish(topic, command)
        print(f"Command '{command}' sent to topic '{topic}'")
    else:
        print("MQTT client is not connected")

# PyQt6 GUI Application Class
class DeviceControlApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.mqtt_client = connect_mqtt(self)  # Pass self to allow callbacks to update UI
        self.status_fan_pre = "ON"

    def initUI(self):
        self.setWindowTitle("Device Control via MQTT")
        self.setGeometry(100, 100, 300, 400)
        layout = QVBoxLayout()

        # Light Control
        self.label_light = QLabel("Light status: Off", self)
        self.label_light.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_light)
        self.btn_light_on = QPushButton("Turn Light On", self)
        self.btn_light_on.clicked.connect(self.turn_on_light)
        layout.addWidget(self.btn_light_on)
        self.btn_light_off = QPushButton("Turn Light Off", self)
        self.btn_light_off.clicked.connect(self.turn_off_light)
        layout.addWidget(self.btn_light_off)

        # Fan Control
        self.label_fan = QLabel("Fan status: Off", self)
        self.label_fan.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_fan)
        self.btn_fan_on = QPushButton("Turn Fan On", self)
        self.btn_fan_on.clicked.connect(self.turn_on_fan)
        layout.addWidget(self.btn_fan_on)
        self.btn_fan_off = QPushButton("Turn Fan Off", self)
        self.btn_fan_off.clicked.connect(self.turn_off_fan)
        layout.addWidget(self.btn_fan_off)

        # Stop and Resume Buttons
        self.btn_stop = QPushButton("Stop System", self)
        self.btn_stop.clicked.connect(self.stop_system)
        layout.addWidget(self.btn_stop)
        
        self.btn_resume = QPushButton("Resume System", self)
        self.btn_resume.clicked.connect(self.resume_system)
        layout.addWidget(self.btn_resume)

        # Set layout
        self.setLayout(layout)

    # Light Control Functions
    def turn_on_light(self):
        send_command(self.mqtt_client, TOPIC_LIGHT, "ON")

    def turn_off_light(self):
        send_command(self.mqtt_client, TOPIC_LIGHT, "OFF")

    # Fan Control Functions
    def turn_on_fan(self):
        send_command(self.mqtt_client, TOPIC_FAN, "ON")

    def turn_off_fan(self):
        send_command(self.mqtt_client, TOPIC_FAN, "OFF")

    # System Control Functions
    def stop_system(self):
        send_command(self.mqtt_client, TOPIC_LIGHT, "OFF")
        send_command(self.mqtt_client, TOPIC_FAN, "OFF")
        print("System stopped: All devices turned off.")

    def resume_system(self):
        print("System resumed: Devices can now be controlled individually.")

    # Update GUI Labels for Real-Time Status
    def update_light_status(self, status):
        self.label_light.setText(f"Light status: {status.capitalize()}")

    def update_fan_status(self, status):
        self.label_fan.setText(f"Fan status: {status.capitalize()}")

# Run Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DeviceControlApp()
    window.show()
    sys.exit(app.exec())
