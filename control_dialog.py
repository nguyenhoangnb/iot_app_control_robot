from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QDialog, QVBoxLayout, QLabel, QSlider, QPushButton, QHBoxLayout
from control_handle import Control_ui
import paho.mqtt.client as mqtt
import json
import sqlite3
from sub import StateDatabase
import math

class ControlDialog(QDialog):
    def __init__(self, mqtt_client, parent=None):
        super().__init__(parent)
        self.mqtt_client = mqtt_client
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Velocity Control")
        layout = QVBoxLayout()

        # Linear velocity slider
        self.linear_label = QLabel("Linear Velocity: 0.0")
        self.linear_slider = QSlider(QtCore.Qt.Horizontal)
        self.linear_slider.setRange(-100, 100)
        self.linear_slider.setValue(0)
        self.linear_slider.valueChanged.connect(self.update_linear_velocity)

        # Angular velocity slider
        self.angular_label = QLabel("Angular Velocity: 0.0")
        self.angular_slider = QSlider(QtCore.Qt.Horizontal)
        self.angular_slider.setRange(-180, 180)
        self.angular_slider.setValue(0)
        self.angular_slider.valueChanged.connect(self.update_angular_velocity)

        # Direction buttons
        button_layout = QHBoxLayout()

        self.forward_button = QPushButton("Forward")
        self.forward_button.clicked.connect(self.move_forward)
        button_layout.addWidget(self.forward_button)

        self.left_button = QPushButton("Left")
        self.left_button.clicked.connect(self.turn_left)
        button_layout.addWidget(self.left_button)

        self.right_button = QPushButton("Right")
        self.right_button.clicked.connect(self.turn_right)
        button_layout.addWidget(self.right_button)

        self.backward_button = QPushButton("Backward")
        self.backward_button.clicked.connect(self.move_backward)
        button_layout.addWidget(self.backward_button)

        # Send velocity button
        self.send_velocity_button = QPushButton("Send Velocity")
        self.send_velocity_button.clicked.connect(self.send_velocity)

        # Layout arrangement
        layout.addWidget(self.linear_label)
        layout.addWidget(self.linear_slider)
        layout.addWidget(self.angular_label)
        layout.addWidget(self.angular_slider)
        layout.addLayout(button_layout)
        layout.addWidget(self.send_velocity_button)

        self.setLayout(layout)

    def update_linear_velocity(self):
        value = self.linear_slider.value() 
        self.linear_label.setText(f"Linear Velocity: {value:.1f}")

    def update_angular_velocity(self):
        value = self.angular_slider.value() 
        self.angular_label.setText(f"Angular Velocity: {value:.1f}")

    def send_velocity(self):
        linear_velocity = self.linear_slider.value() * 0.2823 / 100.0
        angular_velocity = self.angular_slider.value() * math.pi/ 180.0

        data = {
            "linear_velocity": linear_velocity,
            "angular_velocity": angular_velocity
        }

        try:
            self.mqtt_client.publish("robot/control", json.dumps(data))
            print(f"Sent: {data}")
        except Exception as e:
            print(f"Error sending velocity: {e}")

    def move_forward(self):
        data = {
            "linear_velocity": 0.2823,
            "angular_velocity": 0.0
        }
        self.publish_direction(data)

    def move_backward(self):
        data = {
            "linear_velocity": -0.2823,
            "angular_velocity": 0.0
        }
        self.publish_direction(data)

    def turn_left(self):
        data = {
            "linear_velocity": 0.0,
            "angular_velocity": math.pi/2
        }
        self.publish_direction(data)

    def turn_right(self):
        data = {
            "linear_velocity": 0.0,
            "angular_velocity": -math.pi/2
        }
        self.publish_direction(data)

    def publish_direction(self, data):
        try:
            self.mqtt_client.publish("robot/control", json.dumps(data))
            print(f"Sent: {data}")
        except Exception as e:
            print(f"Error sending direction: {e}")