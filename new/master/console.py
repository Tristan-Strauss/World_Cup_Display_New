import serial
import time

class SlaveController:
    def __init__(self, port="/dev/serial0", baud=9600):
        self.ser = serial.Serial(port, baud)
        time.sleep(2)
        print("[+] Serial Initialized")

    def send(self, command):
        self.ser.write(f"{command}\n".encode())
        print(f"[>] Sent to slave: {command}")
