import serial.tools.list_ports
import logging

device_list = ['Arduino', 'USB-SERIAL CH340', 'CP2102', 'FTDI', 'USB JTAG']

def find_device_port(log_level: int = logging.INFO, log_name: str = "FindDevicePort"):

    logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(log_name)
    
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        logger.debug(f"Found port: {port}")
        if any(device in port.description for device in device_list):
            logger.debug(f"Returning device port: {port.device}")
            return port.device
    return None