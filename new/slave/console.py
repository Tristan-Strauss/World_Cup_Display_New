import serial
import time
import gpio

ser = serial.Serial("/dev/serial0", 9600)
time.sleep(2)

print("[+] Serial Connection to Master Initialized")

print("[-] Waiting for commands from master...")
while True:
    if ser.in_waiting > 0:
        command = ser.readline().decode().strip()
        print(f"[+] Received command from master: {command}")
        if (command.split("_")[1] == "High"):
            pin = command.split("-")[0]
            gpio.set_pin_high(pin=pin)
        elif (command.split("_")[1] == "Low"):
            pin = command.split("-")[0]
            gpio.set_pin_low(pin=pin)
        else:
            print(f"[!] Unknown command from master")