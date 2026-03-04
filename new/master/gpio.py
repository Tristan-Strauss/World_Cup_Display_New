import RPi.GPIO as GPIO

master_year_pin_dict = {
    "1930": 7,
    "1934": 11,
    "1938": 12,
    "1942": 13,
    "1946": 15,
    "1950": 16,
    "1954": 18,
    "1958": 19,
    "1962": 21,
    "1966": 22,
    "1970": 23,
    "1974": 24,
    "1978": 26,
    "1982": 29,
    "1986": 31,
    "1990": 32,
    "1994": 33,
    "1998": 35,
    "2002": 36,
    "2006": 37,
    "2010": 38,
    "2014": 40
}

slave_year_pin_dict = {
    "2018": 7,
    "2022": 11,
    "2026": 12,
    "2030": 13,
    "2034": 15,
    "2038": 16,
    "2042": 18,
    "2046": 19,
    "2050": 21,
    "2054": 22,
    "2058": 23,
    "2062": 24,
    "2066": 26,
    "2070": 29,
    "2074": 31,
    "2078": 32,
    "2082": 33,
    "2086": 35,
    "2090": 36,
    "2094": 37,
    "2098": 38,
    "2102": 40
}

class GPIOController:
    def __init__(self):
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
        print("[-] GPIO Pins configured and set LOW")

    def set_all_high(self):
        GPIO.output(3, GPIO.HIGH)
        GPIO.output(5, GPIO.HIGH)
        GPIO.output(7, GPIO.HIGH)
        GPIO.output(11, GPIO.HIGH)
        GPIO.output(12, GPIO.HIGH)
        GPIO.output(13, GPIO.HIGH)
        GPIO.output(15, GPIO.HIGH)
        GPIO.output(16, GPIO.HIGH)
        GPIO.output(18, GPIO.HIGH)
        GPIO.output(19, GPIO.HIGH)
        GPIO.output(21, GPIO.HIGH)
        GPIO.output(22, GPIO.HIGH)
        GPIO.output(23, GPIO.HIGH)
        GPIO.output(24, GPIO.HIGH)
        GPIO.output(26, GPIO.HIGH)
        # GPIO.output(27, GPIO.HIGH)
        # GPIO.output(28, GPIO.HIGH)
        GPIO.output(29, GPIO.HIGH)
        GPIO.output(31, GPIO.HIGH)
        GPIO.output(32, GPIO.HIGH)
        GPIO.output(33, GPIO.HIGH)
        GPIO.output(35, GPIO.HIGH)
        GPIO.output(36, GPIO.HIGH)
        GPIO.output(37, GPIO.HIGH)
        GPIO.output(38, GPIO.HIGH)
        GPIO.output(40, GPIO.HIGH)
        print("[-] Set all GPIO pins high")

    def set_all_low(self):
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
        print("[-] Set all GPIO pins low")

    def set_pin_high(self, pin):
        GPIO.output(pin, GPIO.HIGH)
        print(f"[-] Set GPIO pin {pin} HIGH")

    def set_pin_low(self, pin):
        GPIO.output(pin, GPIO.LOW)
        print(f"[-] Set GPIO pin {pin} LOW")

    def check_if_year_valid(self, year):
        if year in master_year_pin_dict or year in slave_year_pin_dict:
            return True
        return False

    def check_if_year_local(self, year):
        if year in master_year_pin_dict:
            print(f"[DEBUG] Year {year} is local")
            return True
        print(f"[DEBUG] Year {year} is not local")
        return False

    def get_pin_from_master_year_dict(self, year):
        return master_year_pin_dict[year]

    def get_pin_from_slave_year_dict(self, year):
        return slave_year_pin_dict[year]
