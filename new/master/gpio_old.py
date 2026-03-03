import RPi.GPIO as GPIO

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

master_year_pin_dict = {
    "1930": 3,
    "1934": 5,
    "1938": 7,
    "1942": 11,
    "1946": 12,
    "1950": 13,
    "1954": 15,
    "1958": 16,
    "1962": 18,
    "1966": 19,
    "1970": 21,
    "1974": 22,
    "1978": 23,
    "1982": 24,
    "1986": 26,
    "1990": 27,
    "1994": 28,
    "1998": 29,
    "2002": 31,
    "2006": 32,
    "2010": 33,
    "2014": 35,
    "2018": 36,
    "2022": 37,
    "2026": 38,
    "2030": 40
}

slave_year_pin_dict = {
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

print("[-] Master and Slave pin dictionaries initialized")

def set_pin_high(pin):
    GPIO.output(pin, GPIO.HIGH)
    print(f"[-] Set GPIO pin {pin} HIGH")

def set_pin_low(pin):
    GPIO.output(pin, GPIO.LOW)
    print(f"[-] Set GPIO pin {pin} LOW")

def check_if_year_valid(year):
    if year in master_year_pin_dict or year in slave_year_pin_dict:
        return True
    return False

def check_if_year_local(year):
    if year in master_year_pin_dict:
        print(f"[DEBUG] Year {year} is local")
        return True
    print(f"[DEBUG] Year {year} is not local")
    return False

def get_pin_from_master_year_dict(year):
    return master_year_pin_dict[year]

def get_pin_from_slave_year_dict(year):
    return slave_year_pin_dict[year]