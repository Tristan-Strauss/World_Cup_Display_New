import serial
import time
import RPi.GPIO as GPIO

ser = serial.Serial('/dev/serial0', 9600)
time.sleep(2)

print("[DEBUG] Serial Connection established")

# GPIO config
GPIO.setmode(GPIO.BOARD) # Uses physical pin numbers. 1 = 3v3, 2 = 5v...
GPIO.setwarnings(False)

# Set up all the GPIO pins
GPIO.setup(3, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
# GPIO.setup(27, GPIO.OUT)
# GPIO.setup(28, GPIO.OUT)
GPIO.setup(29, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(32, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)
GPIO.setup(40, GPIO.OUT)

# Set all GPIO pins to low
GPIO.output(3, GPIO.LOW)
GPIO.output(5, GPIO.LOW)
GPIO.output(7, GPIO.LOW)
GPIO.output(11, GPIO.LOW)
GPIO.output(12, GPIO.LOW)
GPIO.output(13, GPIO.LOW)
GPIO.output(15, GPIO.LOW)
GPIO.output(16, GPIO.LOW)
GPIO.output(18, GPIO.LOW)
GPIO.output(19, GPIO.LOW)
GPIO.output(21, GPIO.LOW)
GPIO.output(22, GPIO.LOW)
GPIO.output(23, GPIO.LOW)
GPIO.output(24, GPIO.LOW)
GPIO.output(26, GPIO.LOW)
# GPIO.output(27, GPIO.LOW)
# GPIO.output(28, GPIO.LOW)
GPIO.output(29, GPIO.LOW)
GPIO.output(31, GPIO.LOW)
GPIO.output(32, GPIO.LOW)
GPIO.output(33, GPIO.LOW)
GPIO.output(35, GPIO.LOW)
GPIO.output(36, GPIO.LOW)
GPIO.output(37, GPIO.LOW)
GPIO.output(38, GPIO.LOW)
GPIO.output(40, GPIO.LOW)

print("[DEBUG] GPIO Pins configured and set LOW")

year_pin_dict = {
    "2034": 3,
    "2038": 5,
    "2042": 7,
    "2046": 11,
    "2050": 12,
    "2054": 13,
    "2058": 15,
    "2062": 16,
    "2066": 18,
    "2070": 19,
    "2074": 21,
    "2078": 22,
    "2082": 23,
    "2086": 24,
    "2090": 26,
    "2094": 27,
    "2098": 28,
    "2102": 29,
    "2106": 31,
    "2110": 32,
    "2114": 33,
    "2118": 35,
    "2122": 36,
    "2126": 37,
    "2130": 38,
    "2134": 40
}

def check_if_year_local(year):
    if year in year_pin_dict:
        print(f"[DEBUG] Year {year} is local")
        return True
    print(f"[DEBUG] Year {year} is not local")
    return False

def get_pin_from_year(year):
    return year_pin_dict[year]

def set_pin_low(pin):
    GPIO.output(pin, GPIO.LOW)
    print(f"[DEBUG] Set GPIO pin {pin} LOW")

def set_pin_high(pin):
    GPIO.output(pin, GPIO.HIGH)
    print(f"[DEBUG] Set GPIO pin {pin} HIGH")

def parse_command(command):
    command = command.split("_")
    year = command[0]
    state = command[1]
    if check_if_year_local(year):
        pin = get_pin_from_year(year)
        if state == "ON":
            set_pin_high(pin)
        elif state == "OFF":
            set_pin_low(pin)


print("[DEBUG] Waiting for commands from master...")
while True:
    if ser.in_waiting > 0:
        command = ser.readline().decode().strip()
        print(f"[DEBUG] Received command from master: {command}")
        parse_command(command)
        