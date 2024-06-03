# SerialCommands
A Python module for seamless serial communication with devices like an Arduino or ESP, offering both non-blocking and blocking interfaces with customizable command and value callbacks.

[GitHub](https://github.com/clevrthings/SerialCommands), [PyPi](https://pypi.org/project/ct-serialcommands/)

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install SerialCommands.

```bash
pip install pyserial
pip install ct-serialcommands
```

## Simple usage
```python
from ct_serialcommands import SerialCommands

def command_callback():
    print("This is a command callback")

def value_callback(value):
    print(f"This is a value callback with value: {value}")

arduino = SerialCommands()
arduino.set_command_callback("test_command", command_callback)
arduino.set_value_callback("value", value_callback) # Returns everything after the value_separator to the callback function. 
                                                    # Ex: value_separator = ":". If the incoming message = "value: 11", "11" will be passed to the callback function.

arduino.send_command("test") # Adds a prefix to the command. Ex: command: test
arduino.send_message("hallo")
```

## Overview
`ct_serialcommands` is a robust Python module designed to facilitate seamless communication with serial devices. It offers both non-blocking and blocking interfaces, allowing developers to easily send and receive commands and values through a serial interface. The module includes features such as automatic device port detection, customizable baud rates, and support for setting command and value callbacks. Additionally, it provides comprehensive logging capabilities to aid in debugging and monitoring serial communications. Whether you're developing for embedded systems, IoT devices, or any application requiring serial communication, `ct_serialcommands` simplifies the process and enhances reliability.


## Features
- Automatically find and connect to the device port.
- Set custom baud rates.
- Define command and value callbacks.
- Send commands and messages.
- Logging support for debugging and monitoring.

## Example usage:
```python
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
        pass
except KeyboardInterrupt:
    print("Program terminated.")
finally:
    arduino.stop()
```

# Contributing
Contributions are welcome! Please open an issue or submit a pull request on GitHub.
You can also suggest a new sensor by opening an issue. 

# Support my work
If you like my work you can always [buy me a coffee!](https://buymeacoffee.com/clevrthings)
