import serial
import time

class ArduinoController:
    def __init__(self, port='COM3', baudrate=9600):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)  # Allow time to connect
        self.base_x = 96
        self.base_y = 78

    def send_angle(self, theta_x, theta_y):
        servo1 = max(0, min(180, int(theta_x) + self.base_x))
        servo2 = max(0, min(180, int(theta_y) + self.base_y))
        self.ser.write(f"{servo1},{servo2}\n".encode())
