import threading
from gui import VideoPlayer
from keyboardListener import KeyboardListener
from console import SlaveController
from gpio import GPIOController
import os
import time

# --- Init hardware ---
slave = SlaveController()
gpio = GPIOController()

# --- Init GUI ---
player = VideoPlayer()

# --- Callback when a valid year is confirmed (Enter pressed) ---
def handle_valid_year(year, video_name):
    print(f"[+] Year accepted: {year}")

    # Turn off all GPIO pins to reset state before playing video
    gpio.set_all_high()
    slave.send("ALL_OFF")

    # Start GPIO (stopped by video stop callback)
    if gpio.check_if_year_local(year):
        pin = gpio.get_pin_from_master_year_dict(year)
        gpio.set_pin_low(pin)
    else:
        pin = gpio.get_pin_from_slave_year_dict(year)
        slave.send(f"{pin}_Low")

    # Play Video
    player.play_by_name(video_name)


# --- Callback to update bottom 4-digit display ---
def handle_update_display(text):
    player.update_year_display(text)


# --- Callback to volume control ---
def on_volume_up():
    os.system("pactl set-sink-volume 0 +10%")

def on_volume_down():
    os.system("pactl set-sink-volume 0 -10%")

# --- Calback to video stop (needs to control video and gpio) ---
def on_video_stop():
    print("[DEBUG] Stopping video and resetting GPIO")
    player.stop_video()
    gpio.set_all_low()
    slave.send("ALL_ON")

# --- Start keyboard listener in background ---
keyboard_listener = KeyboardListener(
    on_valid_year=handle_valid_year,
    on_update_display=handle_update_display,
    on_stop_video=on_video_stop,
    on_volume_up=on_volume_up,
    on_volume_down=on_volume_down
)

kb_thread = threading.Thread(
    target=keyboard_listener.start,
    daemon=True
)
kb_thread.start()

# --- Start GUI (main thread) ---
player.start()