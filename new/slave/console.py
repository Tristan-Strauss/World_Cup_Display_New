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
        print(f"\n[+] Received command from master: {command}")
        if (command.split("_")[1] == "High"):
            pin = command.split("-")[0]
            gpio.set_pin_high(pin=pin)
        elif (command.split("_")[1] == "Low"):
            pin = command.split("-")[0]
            gpio.set_pin_low(pin=pin)
        elif (command.split("_")[1] == "ON"):
            gpio.set_all_low()
        elif (command.split("_")[1] == "OFF"):
            gpio.set_all_high()
        else:
            print(f"[!] Unknown command from master")