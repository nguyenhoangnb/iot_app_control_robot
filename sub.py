import sqlite3
import json
import paho.mqtt.client as mqtt

class StateDatabase:
    def __init__(self, db_name="states.db"):
        self.db_name = db_name

    def print_db_table(self, table_name):
        """
        Fetch and print the data from a specified database table.
        """
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        try:
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            print(f"Data in table '{table_name}':")
            for row in rows:
                print(row)
        except Exception as e:
            print(f"Error querying database table {table_name}: {e}")
        finally:
            connection.close()

    def update_data(self, state, state_now , led_1, led_2):
        """
        Update data in the appropriate table based on the state value.
        """
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        try:
            if state == "state_1":
                cursor.execute("""
                    UPDATE state_1
                    SET 
                        time_out = ?, 
                        led_1_status = ?, 
                        led_1_timeout = ?, 
                        led_2_status = ?
                """, (
                    state_now.get("timeOut", 0),
                    led_1.get("status", ""),
                    led_1.get("timeOut", 0),
                    led_2.get("status", ""),
                ))
                print("Updated state_1 table.")
                self.print_db_table("state_1")

            elif state == "state_2":
                cursor.execute("""
                    UPDATE state_2
                    SET 
                        time_out = ?, 
                        led_1_status = ?, 
                        led_1_timeout = ?, 
                        led_2_status = ?, 
                        led_2_timeout = ?
                """, (
                    state_now.get("timeOut", 0),
                    led_1.get("status", ""),
                    led_1.get("timeout", 0),
                    led_2.get("status", ""),
                    led_2.get("timeout", 0),
                ))
                print("Updated state_2 table.")
                self.print_db_table("state_2")

            elif state == "state_3":
                cursor.execute("""
                    UPDATE state_3
                    SET 
                        time_out = ?, 
                        led_1_status = ?, 
                        led_2_status = ?
                """, (
                    state_now.get("timeOut", 0),
                    led_1.get("status", ""),
                    led_2.get("status", ""),
                ))
                print("Updated state_3 table.")
                self.print_db_table("state_3")

            elif state == "state_4":
                cursor.execute("""
                    UPDATE state_4
                    SET 
                        time_out = ?, 
                        led_2_status = ?, 
                        led_2_timeout = ?
                """, (
                    state_now.get("time_out", 0),
                    led_2.get("status", ""),
                    led_2.get("timeout", 0),
                ))
                print("Updated state_4 table.")
                self.print_db_table("state_4")

            connection.commit()

        except Exception as e:
            print(f"Failed to update data in database: {e}")
        finally:
            connection.close()


class MQTTClient:
    def __init__(self, broker_ip="192.168.1.114", broker_port=1883, topic="state_data"):
        self.broker_ip = broker_ip
        self.broker_port = broker_port
        self.topic = topic
        self.db = StateDatabase()
        self.client = mqtt.Client()

    def on_message(self, client, userdata, msg):
        """
        Callback for incoming messages from the MQTT topic.
        Parses the payload and inserts data into the database.
        """
        print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")

        try:
            # Parse JSON payload
            data = json.loads(msg.payload.decode())
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return

        # Determine which database table to interact with
        state = data.get("state")
        if not state:
            print("State field is missing from the message payload.")
            return

        self.db.insert_data(state, data)

    def mqtt_client_setup(self):
        """
        Set up MQTT client and start listening for messages.
        """
        # Assign callback
        self.client.on_message = self.on_message

        # Connect to MQTT broker
        try:
            self.client.connect(self.broker_ip, self.broker_port, 60)
            self.client.subscribe(self.topic)
            print(f"Connected to MQTT broker and subscribed to '{self.topic}'")
        except Exception as e:
            print(f"Could not connect to MQTT broker: {e}")
            return

        # Start message loop
        self.client.loop_start()
        print(f"Listening for messages on '{self.topic}' topic...")

        try:
            while True:
                pass  # Keep script running
        except KeyboardInterrupt:
            print("Stopping subscriber...")
        finally:
            self.client.loop_stop()
            self.client.disconnect()
            print("Disconnected from the MQTT broker.")

if __name__ == "__main__":
    mqtt_client = MQTTClient()
    mqtt_client.mqtt_client_setup()
