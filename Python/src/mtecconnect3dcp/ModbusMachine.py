


# Standard library imports
import math
import time
from threading import Timer

# Third-party imports
import serial

# Typing
from typing import Optional, Callable, Any

class ModbusMachine:
    """
    Base class for Modbus machine communication.

    Args:
        port (str): Serial port to use (e.g., 'COM3').
        frequency_inverter_id (str): ID of the frequency inverter (default '01').
        baudrate (int): Serial baudrate (default 19200).
        log (bool): Enable logging (default False).
    """
    def __init__(self, frequency_inverter_id: str = "01", baudrate: int = 19200, log: bool = False):
        self._frequency_inverter_id = frequency_inverter_id
        self._baudrate = baudrate
        self._log = log
        self._connected = False
        self._serial: Optional[serial.Serial] = None
        self._keepalive_timer: Optional[Timer] = None
        self._keepalive_interval = 0.25  # seconds
        self._timeout = 0.2  # seconds
        self._keepalive_command = "03FD000001"
        self._keepalive_callback: Optional[Callable[[Any], None]] = None

    def connect(self, port: str):
        """
        Connects to the Modbus machine using the provided serial port.

        Args:
            port (str): Serial port to use.
        """
        self._port = port
        if not self._port:
            raise ValueError("No serial port provided.")
        self._serial = serial.Serial(
            port=self._port,
            baudrate=self._baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.EIGHTBITS
        )
        self._connected = True
        self._log(f"Connected to {self._port}")

    def disconnect(self):
        """
        Disconnects from the Modbus machine.
        """
        if self._serial and self._serial.is_open:
            self._serial.close()
        self._connected = False
        self._log("Disconnected.")

    def read(self, command: str) -> Any:
        """
        Reads a value from the Modbus machine.

        Args:
            command (str): The Modbus command to read.

        Returns:
            Any: The value read from the machine.
        """
        return self._send_command("03" + command, 1)

    def write(self, command: str, value: int) -> Any:
        """
        Writes a value to the Modbus machine.

        Args:
            command (str): The Modbus command to write.
            value (int): The value to write.

        Returns:
            Any: The response from the machine.
        """
        return self._send_command("06" + command, value)

    def _send_command(self, parameter: str, value: int) -> Any:
        data = self._frequency_inverter_id + parameter + self._int2hex(value, 4)
        return self._send_hex_command(data)

    def _send_hex_command(self, data: str) -> Any:
        crc = self._calc_crc(data)
        command = data + crc
        return self._send_and_receive(command)

    def _send_and_receive(self, command: str) -> Any:
        if not self._connected or not self._serial:
            raise RuntimeError("Not connected to Modbus machine.")
        self._log(f"Sending: {command}")
        self._serial.write(bytes.fromhex(command))
        res = self._wait_for_response()
        if res is None:
            self._log("No valid response received. - Retries once.")
            self._serial.write(bytes.fromhex(command))
            res = self._wait_for_response()
        if res is None:
            self._log("No valid response received after retry.")
        return res


    def _wait_for_response(self) -> Any:
        ONE_SECOND = 1_000_000_000
        timeout = time.time_ns() + (self._timeout * ONE_SECOND)
        while True:
            if self._serial.inWaiting() >= 2:
                break
            if time.time_ns() > timeout:
                self._log("Timeout waiting for response header.")
                self._serial.read(self._serial.inWaiting())
                return None
        message_fcID = int.from_bytes(self._serial.read(1), "little")
        message_type = int.from_bytes(self._serial.read(1), "little")
        command = self._int2hex(message_fcID, 2) + self._int2hex(message_type, 2)

        if message_type == 3:  # Type: read
            message_length = int.from_bytes(self._serial.read(1), "little")
            command += self._int2hex(message_length, 2)
            complete_data_length = message_length + 2  # data + CRC
        elif message_type == 6:  # Type: send
            complete_data_length = 6  # param(2) + value(2) + CRC(2)
        else:
            complete_data_length = 2  # CRC only

        while True:
            if self._serial.inWaiting() >= complete_data_length:
                break
            if time.time_ns() > timeout:
                self._log("Timeout waiting for response body.")
                self._serial.read(self._serial.inWaiting())
                return None

        is_error = False
        if message_type == 3:
            message_value = 0
            for _ in range(message_length):
                message_value = (message_value << 8) + int.from_bytes(self._serial.read(1), "little")
                command += self._int2hex(message_value & 0xFF, 2)
        elif message_type == 6:
            param = self._int2hex(int.from_bytes(self._serial.read(1), "little"), 2) + self._int2hex(int.from_bytes(self._serial.read(1), "little"), 2)
            command += param
            value0 = int.from_bytes(self._serial.read(1), "little")
            value1 = int.from_bytes(self._serial.read(1), "little")
            message_value = value0 * 256 + value1
            command += self._int2hex(message_value, 4)
        elif message_type == 0x86:
            message_value = int.from_bytes(self._serial.read(1), "little")
            command += self._int2hex(message_value, 2)
            is_error = True
        else:
            message_value = None

        crc = self._int2hex(int.from_bytes(self._serial.read(1), "little"), 2) + self._int2hex(int.from_bytes(self._serial.read(1), "little"), 2)
        if self._calc_crc(command) != crc:
            is_error = True
            self._log("CRC error.")
        if is_error:
            self._log("Error in Modbus response.")
            return None
        return message_value

    def keepalive(self, callback: Optional[Callable[[Any], None]] = None, interval: float = 0.25):
        """
        Starts a keepalive loop sending a command at a regular interval.

        Args:
            callback (Callable): Function to call with the response.
            interval (float): Interval in seconds.
        """
        self._keepalive_callback = callback
        self._keepalive_interval = interval
        self._keepalive_loop()

    def _keepalive_loop(self):
        if not self._connected:
            return
        value = self._send_hex_command(self._frequency_inverter_id + self._keepalive_command)
        if self._keepalive_callback:
            self._keepalive_callback(value)
        self._keepalive_timer = Timer(self._keepalive_interval, self._keepalive_loop)
        self._keepalive_timer.start()

    def stop_keepalive(self):
        """
        Stops the keepalive loop.
        """
        if self._keepalive_timer:
            self._keepalive_timer.cancel()
            self._keepalive_timer = None

    def _int2hex(self, value: int, length: int) -> str:
        s = hex(value)[2:]
        while len(s) < length:
            s = "0" + s
        return s.upper()

    def _calc_crc(self, command: str) -> str:
        buffer = bytearray.fromhex(command)
        crc = 0xFFFF
        for pos in range(len(buffer)):
            crc ^= buffer[pos]
            for _ in range(8):
                if (crc & 0x0001) != 0:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        return self._int2hex((crc % 256) * 256 + math.floor(crc / 256), 4)

    def _log(self, content: str):
        if self._log:
            print(content)