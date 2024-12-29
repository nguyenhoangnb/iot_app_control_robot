from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QDialog, QVBoxLayout, QLabel, QSlider, QPushButton, QHBoxLayout
from control_handle import Control_ui
import paho.mqtt.client as mqtt
import json
import sqlite3
from sub import StateDatabase


class main_control(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_window = QMainWindow()
        self.main_handle = Control_ui(self.main_window)
        self.main_window.show()
        self.conn = sqlite3.connect("states.db")
        self.cursor = self.conn.cursor()

        # MQTT Client Setup
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_message = self.on_message
        self.db = StateDatabase()

        self.stop_check = False
        self.check_auto = False
        self.current_state = ""
        self.topic_auto = "automatic"
        self.broker_address = "192.168.43.111"
        self.port = 1883  # Default MQTT port
        try:
            self.mqtt_client.connect(self.broker_address, self.port)
            self.mqtt_client.subscribe("handleTopic")
            self.mqtt_client.subscribe("check_auto")
            self.mqtt_client.subscribe("currentStateTopic")
        except Exception as e:
            print(f"Error connecting to MQTT broker: {e}")
        self.mqtt_client.loop_start()

        # Connect buttons to their respective methods
        self.main_handle.state_1.clicked.connect(self.send_state_1)
        self.main_handle.state_2.clicked.connect(self.send_state_2)
        self.main_handle.state_3.clicked.connect(self.send_state_3)
        self.main_handle.state_4.clicked.connect(self.send_state_4)

        self.main_handle.resume_button.clicked.connect(self.send_continue)
        self.main_handle.stop_button.clicked.connect(self.send_stop)
        self.main_handle.control_v.hide()
    def on_message(self, client, userdata, msg):
        """
        Callback for incoming messages from the MQTT topic.
        Parses the payload and inserts data into the database.
        """
        print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")
        data = ''
        try:
            # Parse JSON payload
            data = json.loads(msg.payload.decode())
        except json.JSONDecodeError as e:
            data = msg.payload.decode()
            

        if msg.topic == "handleTopic":
            # Handle the state_data topic
            print(data)
            state_now = data.get("state_now")
            led_1 = data.get("led_1")
            led_2 = data.get("led_2")

            if not state_now:
                print("State_now field is missing from the message payload.")
                return

            state = state_now.get("state")
            self.current_state = state
            if not state:
                print("State field inside state_now is missing.")
                return

            print("Parsed state_now data:", state_now)
            print("Parsed led_1 data:", led_1)
            print("Parsed led_2 data:", led_2)

            # Save state_now and other data to the database
            self.db.update_data(state, state_now, led_1, led_2)

        elif msg.topic == "check_auto":
            check = msg.payload.decode().strip()  # The payload is just a string ("0" or "1")
            print(f"check_auto received with value: {check}")

            if check == "1":
                # Action for enabling auto mode
                message_to_publish = "Auto mode is now active"
                print(f"Publishing message to topic {self.topic_auto}: {self.current_state}")
                self.send_continue()
                self.current_state = ""

            else:
                print(f"Invalid check value received: {check}. Expected '0' or '1'.")
        elif msg.topic == "currentStateTopic":
            self.main_handle.lbl_state_now.setText(data)

    def send_continue(self):
        self.stop_check = False
        if self.current_state == "state_1":
            self.send_state_1()
        elif self.current_state == "state_2":
            self.send_state_2()
        elif self.current_state == "state_3":
            self.send_state_3()
        elif self.current_state == "state_4":
            self.send_state_4()
        self.update_timeouts(self.current_state)

    def send_stop(self):
        self.stop_check = True
        message = "stop"
        topic = "stop"
        try:
            self.mqtt_client.publish(topic, message)
            print(f"Published: {message} to topic: {topic}")
        except Exception as e:
            print(f"Error publishing to topic {topic}: {e}")

    def send_state_1(self):
        state_dict = self.get_state_data("state_1")
        state_data = {
            "state_now": {
                "state": state_dict[0],
                "time": state_dict[1],
                "timeOut": state_dict[2]
            },
            "led_1": {
                "status": state_dict[3],
                "time": state_dict[4],  # Time in milliseconds
                "timeOut": state_dict[5]
            },
            "led_2": {
                "status": state_dict[6],
            }
        }
        if self.stop_check:
            state_data["state_now"]["timeOut"] = 0
            state_data["led_1"]["timeOut"] = 0
            state_data["led_2"]["timeOut"] = 0
        self.publish_command(state_data)

    def send_state_2(self):
        state_dict = self.get_state_data("state_2")
        state_data = {
            "state_now": {
                "state": state_dict[0],
                "time": state_dict[1],
                "timeOut": state_dict[2]
            },
            "led_1": {
                "status": state_dict[3],
                "time": state_dict[4],  # Time in milliseconds
                "timeOut": state_dict[5]
            },
            "led_2": {
                "status": state_dict[6],
                "time": state_dict[7],  # Time in seconds
                "timeOut": state_dict[8]
            }
        }
        if self.stop_check:
            state_data["state_now"]["timeOut"] = 0
            state_data["led_1"]["timeOut"] = 0
            state_data["led_2"]["timeOut"] = 0
        self.publish_command(state_data)

    def send_state_3(self):
        state_dict = self.get_state_data("state_3")
        state_data = {
            "state_now": {
                "state": state_dict[0],
                "time": state_dict[1],
                "timeOut": state_dict[2]
            },
            "led_1": {
                "status": state_dict[3],
            },
            "led_2": {
                "status": state_dict[4],
            }
        }
        self.publish_command(state_data)

    def send_state_4(self):
        state_dict = self.get_state_data("state_4")
        state_data = {
            "state_now": {
                "state": state_dict[0],
                "time": state_dict[1],
                "timeOut": state_dict[2]
            },
            "led_2": {
                "status": state_dict[3],
                "time": state_dict[4],  # Time in seconds
                "timeOut": state_dict[5]
            }
        }
        if self.stop_check:
            state_data["state_now"]["timeOut"] = 0
            state_data["led_2"]["timeOut"] = 0
        self.publish_command(state_data)

    def get_state_data(self, state_table):
        conn = sqlite3.connect("states.db")
        cursor = conn.cursor()

        # Retrieve data from the specified table
        cursor.execute(f"SELECT * FROM {state_table}")
        data = cursor.fetchone()

        conn.close()
        return data


    def update_timeouts(self, state_table):
        """
        Reset timeouts and update statuses for the given state table.
        """
        conn = sqlite3.connect("states.db")
        cursor = conn.cursor()
        # print(state_table)
        try:
            # Validate the table name to prevent SQL injection
            valid_tables = {"state_1", "state_2", "state_3", "state_4"}
            if state_table not in valid_tables:
                raise ValueError(f"Invalid table name: {state_table}")

            # Get column names of the table
            cursor.execute(f"PRAGMA table_info('{state_table}')")
            columns = [column[1] for column in cursor.fetchall()]

            # Prepare the updates based on the state table
            updates = []
            if state_table == "state_1":
                updates.append("led_1_status = 'on'")
                updates.append("led_2_status = 'on'")
            elif state_table == "state_2":
                updates.append("led_1_status = 'off'")
                updates.append("led_2_status = 'on'")
            elif state_table == "state_3":
                updates.append("led_1_status = 'off'")
                updates.append("led_2_status = 'on'")
            elif state_table == "state_4":
                updates.append("led_2_status = 'on'")

            # Add timeout resets if the columns exist
            if "time_out" in columns:
                updates.append("time_out = 0")
            if "led_1_timeout" in columns:
                updates.append("led_1_timeout = 0")
            if "led_2_timeout" in columns:
                updates.append("led_2_timeout = 0")

            # If there are updates, execute the query
            if updates:
                update_query = f"UPDATE {state_table} SET {', '.join(updates)}"
                cursor.execute(update_query)
                conn.commit()

        except sqlite3.Error as e:
            print(f"SQLite error updating timeouts in {state_table}: {e}")
        except ValueError as ve:
            print(f"Validation error: {ve}")
        except Exception as e:
            print(f"General error updating timeouts in {state_table}: {e}")
        finally:
            conn.close()

    def publish_command(self, state_data):
        try:
            message = json.dumps(state_data)
            self.mqtt_client.publish(self.topic_auto, message)
            print(f"Published: {message} to topic: {self.topic_auto}")
        except Exception as e:
            print(f"Error publishing to topic {self.topic_auto}: {e}")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = main_control()
    sys.exit(app.exec_())
