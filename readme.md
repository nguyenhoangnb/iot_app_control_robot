# PyQt5 MQTT Control System

This is a Python-based control system using **PyQt5** for the graphical user interface (GUI) and **MQTT** for communication. The system allows users to control devices via the GUI, with states and control commands sent over MQTT. Data is stored and managed in an **SQLite** database.

## Features

- **MQTT Communication**: Connects to an MQTT broker to send and receive data regarding the current state of devices.
- **PyQt5 GUI**: A simple and intuitive interface for interacting with devices.
- **SQLite Database**: Stores state data locally for manual control and updates dynamically based on incoming MQTT messages.
- **Control Dialog**: A dialog for controlling velocity and other parameters.
- **State Control**: The system can control various devices in 4 different states.

## Requirements

- Python >=3.8
- PyQt5
- paho-mqtt
- sqlite3 (Included in the Python standard library)

### Install Dependencies

To install the required Python packages, use the following command:

```bash
pip install -r requirements.txt
```
## Installation
1. Clone the Repository
bash
Copy code
git clone https://github.com/nguyenhoangnb/iot_app_control_robot.git
    ```bash
    cd iot_app_control_robot
    ```
2. Install the Dependencies
  
    ```bash
    pip install -r requirements.txt
    ```
3. Run the Application \
Run the Control State App
This script manages the device states via the GUI and communicates with the MQTT broker.

    ```bash
    python control_state.py
    ```
    Run the Set State Automatic App
This script manages automatic state transitions based on MQTT messages. It can control devices in an automated manner.

    ```bash
    python set_automatic.py
    ```
## Usage
Control States:
Click one of the state buttons (State 1, State 2, State 3, or State 4) in the GUI to send corresponding state data over MQTT.

Stop and Resume:

The Stop button will stop the current state and operation.
The Resume button will continue the operation from the last selected state.
Control Dialog:
Clicking the Control button opens a dialog to control additional parameters, such as velocity or other settings.

## MQTT Topics
- **`handleTopic`**: Used to send state data including current state and LED statuses.
- **`check_auto`**: Used to check whether auto mode is enabled (value "1") or disabled (value "0").
- **`currentStateTopic`**: Sends the current state data to update the GUI.
- **`automatic`**: Used for publishing automatic mode status (whether auto mode is active or not).
- **`stop`**: Used to stop the current operation.
## Acknowledgements<br>
PyQt5: The graphical user interface was built using PyQt5, enabling easy design and interaction with the system.
paho-mqtt: Used for communication between the control system and the connected devices via MQTT. It enables message publishing and subscribing to topics.
SQLite3: Used for lightweight, local database management to store and retrieve state data.
Special Thanks: To the contributors and developers of PyQt5, paho-mqtt, and SQLite for their contributions to the project's functionality and scalability.
