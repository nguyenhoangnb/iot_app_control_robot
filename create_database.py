import sqlite3


def initialize_database():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect("states_manual.db")
    cursor = conn.cursor()

    # Create tables for each state
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS state_1 (
        state TEXT,
        time INTEGER,
        time_out INTEGER,
        led_1_status TEXT,
        led_1_time INTEGER,
        led_1_timeout INTEGER,
        led_2_status TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS state_2 (
        state TEXT,
        time INTEGER,
        time_out INTEGER,
        led_1_status TEXT,
        led_1_time INTEGER,
        led_1_timeout INTEGER,
        led_2_status TEXT,
        led_2_time INTEGER,
        led_2_timeout INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS state_3 (
        state TEXT,
        time INTEGER,
        time_out INTEGER,
        led_1_status TEXT,
        led_2_status TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS state_4 (
        state TEXT,
        time INTEGER,
        time_out INTEGER,
        led_2_status TEXT,
        led_2_time INTEGER,
        led_2_timeout INTEGER
    )
    """)

    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("Database initialized and tables created successfully.")


def insert_sample_data():
    conn = sqlite3.connect("states_manual.db")
    cursor = conn.cursor()

    # Insert data into state_1
    cursor.execute("""
    INSERT INTO state_1 VALUES (
        'state_1', 40000, 0, 'on', 10000, 0, 'on'
    )
    """)

    # Insert data into state_2
    cursor.execute("""
    INSERT INTO state_2 VALUES (
        'state_2', 45000, 0, 'on', 3000, 0, 'on', 6000, 0
    )
    """)

    # Insert data into state_3
    cursor.execute("""
    INSERT INTO state_3 VALUES (
        'state_3', 50000, 0, 'off', 'on'
    )
    """)

    # Insert data into state_4
    cursor.execute("""
    INSERT INTO state_4 VALUES (
        'state_4', 35000, 0, 'on', 5000, 0
    )
    """)

    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("Sample data inserted successfully.")


def get_state_data(state_table):
    """
    Fetch the first row of data from the specified table.
    """
    conn = sqlite3.connect("states_manual.db")
    cursor = conn.cursor()

    # Retrieve data from the specified table
    cursor.execute(f"SELECT * FROM {state_table}")
    data = cursor.fetchone()

    conn.close()
    if data:
        print(f"Data from '{state_table}':", data)
    else:
        print(f"No data found in '{state_table}'")
    return data


def send_state_1():
    """
    Fetch and send data for state_1
    """
    state_data = get_state_data("state_1")
    if state_data:
        mapped_data = {
            "state_now": {
                "state": state_data[0],
                "time": state_data[1]
            },
            "led_1": {
                "status": state_data[3],
                "time": state_data[4],
                "timeOut": state_data[5]
            },
            "led_2": {
                "status": state_data[6],
                "time": state_data[7],
                "timeOut": state_data[8]
            }
        }
        publish_command(mapped_data)


def send_state_2():
    """
    Fetch and send data for state_2
    """
    state_data = get_state_data("state_2")
    if state_data:
        mapped_data = {
            "state_now": {
                "state": state_data[0],
                "time": state_data[1]
            },
            "led_1": {
                "status": state_data[3],
                "time": state_data[4],
                "timeOut": state_data[5]
            },
            "led_2": {
                "status": state_data[6],
                "time": state_data[7],
                "timeOut": state_data[8]
            }
        }
        publish_command(mapped_data)


def send_state_3():
    """
    Fetch and send data for state_3
    """
    state_data = get_state_data("state_3")
    if state_data:
        mapped_data = {
            "state_now": {
                "state": state_data[0],
                "time": state_data[1]
            },
            "led_1": {
                "status": state_data[3]
            },
            "led_2": {
                "status": state_data[4]
            }
        }
        publish_command(mapped_data)


def send_state_4():
    """
    Fetch and send data for state_4
    """
    state_data = get_state_data("state_4")
    if state_data:
        mapped_data = {
            "state_now": {
                "state": state_data[0],
                "time": state_data[1]
            },
            "led_2": {
                "status": state_data[3],
                "time": state_data[4],
                "timeOut": state_data[5]
            }
        }
        publish_command(mapped_data)


def publish_command(state_data):
    """
    Simulate a command publication by printing the data.
    """
    print("Publishing state data:", state_data)


# Main execution to initialize database, insert data, and simulate operations
if __name__ == "__main__":
    initialize_database()
    insert_sample_data()

   
