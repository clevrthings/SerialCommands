import serial
from threading import Thread, Event, Lock
import time
import logging
from .find_port import find_device_port

class SerialCommands:
    def __init__(self, port: str = "AUTO", baud_rate: int = 9600, default_command_prefix: str = "command", value_separator: str = ":", log_level: int = logging.INFO, log_name: str = "SerialCommands"):
        if port == "AUTO":
            self._port = find_device_port(log_level=log_level)
        else:
            self._port = port
        self._baud_rate = baud_rate
        self._serial = None
        self._stop_event = Event()
        self._default_command_prefix = default_command_prefix
        self._value_separator = value_separator
        self._command_callbacks = {}
        self._value_callbacks = {}
        self._lock = Lock()
        self._listen_thread = None
        self.log_level = log_level
        self.log_name = log_name
        
        logging.basicConfig(level=self.log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(log_name)
        self.logger.info(f"Initialized SerialCommands with port={self._port}, baud_rate={self._baud_rate}")

    def _connect(self):
        with self._lock:
            try:
                self._serial = serial.Serial(self._port, self._baud_rate, timeout=1)
                self.logger.info(f"Connected to {self._port} at {self._baud_rate} baud.")
            except serial.SerialException as e:
                self.logger.error(f"Error connecting to {self._port}: {e}")
                self._serial = None

    def close_connection(self):
        with self._lock:
            if self._serial:
                if self._serial.is_open:
                    self._serial.close()
                    self.logger.info(f"Closed connection to {self._port}")
                self._serial = None

    def set_command_callback(self, command, callback, *args, **kwargs):
        if 'args' in kwargs:
            args = kwargs.pop('args')
        self._command_callbacks[command] = (callback, args, kwargs)
        self.logger.debug(f"Set command callback for command={command}")

    def set_value_callback(self, value, callback, *args, **kwargs):
        if 'args' in kwargs:
            args = kwargs.pop('args')
        self._value_callbacks[value] = (callback, args, kwargs)
        self.logger.debug(f"Set value callback for value={value}")

    def _check_for_command_callback(self, data):
        if data in self._command_callbacks:
            callback, args, kwargs = self._command_callbacks[data]
            callback(*args, **kwargs)
            self.logger.debug(f"Executed command callback for data={data}")
            return True
        return False

    def _check_for_value_callback(self, data):
        command, sep, message = data.partition(self._value_separator)
        if sep and command in self._value_callbacks:
            callback, args, kwargs = self._value_callbacks[command]
            callback(message.strip(), *args, **kwargs)
            self.logger.debug(f"Executed value callback for command={command} with message={message.strip()}")
            return True
        return False

    def listen(self):
        while not self._stop_event.is_set():
            with self._lock:
                if self._serial and self._serial.is_open:
                    try:
                        if self._serial.in_waiting > 0:
                            data = self._serial.readline().decode('utf-8').strip()
                            if data:
                                self.logger.info(f"Received: {data}")
                                if not self._check_for_command_callback(data):
                                    self._check_for_value_callback(data)
                    except serial.SerialException as e:
                        self.logger.error(f"Serial exception: {e}")
                        break
                    except OSError as e:
                        self.logger.error(f"OS error: {e}")
                        break
                else:
                    time.sleep(0.1)
                    continue

    def send_message(self, message: str):
        with self._lock:
            if self._serial and self._serial.is_open:
                try:
                    self._serial.write(message.encode('utf-8'))
                    self.logger.info(f"Sent: {message}")
                except serial.SerialException as e:
                    self.logger.error(f"Error sending command: {e}")

    def send_command(self, command: str, custom_command_prefix: str = ""):
        if custom_command_prefix != "":
            self.send_message(f"{custom_command_prefix}: {command}")
        else:
            self.send_message(f"{self._default_command_prefix}: {command}")

    def _start_listening(self):
        self._listen_thread = Thread(target=self.listen)
        self._listen_thread.start()
        self.logger.info("Listening for data...")

    def start(self):
        self._connect()
        self._start_listening()

    def stop(self):
        self._stop_event.set()
        if self._listen_thread:
            self._listen_thread.join()
        self.close_connection()
        self.logger.info("Stopped listening.")

    def reopen_connection(self):
        self.close_connection()
        time.sleep(0.1)
        self._connect()
