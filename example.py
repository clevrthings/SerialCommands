from ct_serialcommands import SerialCommands
import time
import logging


# Create a command callback function
def command_callback(arg1, arg2):
    print(f"Command callback with arg1: {arg1}, arg2: {arg2}")
    
# Create a value callback function
def value_callback(value, arg1, arg2):
    print(f"Value callback with arg1: {arg1}, arg2: {arg2} and value: {value}")


# Set the port name of the connected device. (Optional. Default = "AUTO") (When set to AUTO, make sure only one device is connected. It will use the first port that is found.)
# port = "/dev/cu.usbmodem21211101"
port = "AUTO"

# Set the baud rate. (Optional. Default = 9600)
baud_rate = 9600

# Set the default command prefix when sending a command. (Optional. Default = "command") (Ex.: command: test)
default_command_prefix = "command"

# Set the separator for a received value. Ex.: 'value1: 30'. (Optional. Default = ":")
value_separator = ":"

# Set the logging level. (Optional. Default = logging.INFO)
log_level = logging.INFO

# Set the logger name. (Optional. Default = "SerialCommands")
log_name = "SerialCommands"

# Initialise the class
arduino = SerialCommands(port=port, baud_rate=baud_rate, default_command_prefix=default_command_prefix, value_separator=value_separator, log_level=log_level, log_name=log_name)


# Set a command callback. Option 1
arduino.set_command_callback("command1", command_callback, "test 1", "test 2")

# Set a command callback. Option 2
arduino.set_command_callback(command="command1", callback=command_callback, args=["test 1", "test 2"])

# Set a command callback. Option 3
arduino.set_command_callback(command="command1", callback=command_callback, arg1="test 1", arg2="test 2")

# Set a value callback
arduino.set_value_callback(value="value", callback=value_callback, arg1="test 1", arg2="test 2")


# Start listening for commands
arduino.start()

try:
    while True:
        # arduino.listen()
        time.sleep(15)  # import time
        arduino.close_connection()
        time.sleep(40)  # import time
        arduino.reopen_connection()
        time.sleep(20)  # import time
        pass
except KeyboardInterrupt:
    print("Program terminated.")
finally:
    arduino.stop()