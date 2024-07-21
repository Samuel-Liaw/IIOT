from datetime import datetime
from opcua import Server
import time
import random

# Setup our server
server = Server()
server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

# Setup our namespace
name = "OPCUA_SIMULATION_SERVER"
NameSpaceIdx = server.register_namespace(name)

# Create a new object complying to OPCUA convention to represent our simulated device
MyObj = server.nodes.objects.add_object(NameSpaceIdx, "MyObject")

# Add some variables to this object
temp_var = MyObj.add_variable(NameSpaceIdx, "Temperature", 0.0)
humidity_var = MyObj.add_variable(NameSpaceIdx, "Humidity", 0.0)
time_var = MyObj.add_variable(NameSpaceIdx, "Time", "")

# Set the variables to be writable by clients
temp_var.set_writable()
humidity_var.set_writable()
time_var.set_writable()

# Start the server
server.start()
print("OPC UA Server started at opc.tcp://0.0.0.0:4840/freeopcua/server/")
print(MyObj.nodeid)
try:
    while True:
        # Simulate sensor data
        temp_value = random.uniform(50.0, 80.0)
        humidity_value = random.uniform(30.0, 50.0)
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Update the values
        temp_var.set_value(temp_value)
        humidity_var.set_value(humidity_value)
        time_var.set_value(current_time)

        print(f"Device: {MyObj},\n"
              f"Temperature: {temp_var, temp_value}, \n"
              f"Humidity: {humidity_var, humidity_value}, \n"
              f"Current time: {time_var, current_time}")
        print("")

        # Sleep for a second before the next update
        time.sleep(1)

finally:
    # Close the server when exiting
    server.stop()
    print("OPC UA Server stopped")
