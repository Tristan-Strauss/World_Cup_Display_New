import threading
from gui import VideoPlayer
from keyboardListener import KeyboardListener
from console import SlaveController
from gpio import GPIOController
import os
import re

# --- Init hardware ---
slave = SlaveController()
gpio = GPIOController()

# ---------- Callback For Video Finish ----------
# This is here because we need it in an init function

def on_video_stop():
    print("[DEBUG] Stopping video and resetting GPIO")
    gpio.set_all_low()
    slave.send("ALL_ON")

# --- Init GUI ---
player = VideoPlayer(on_video_finished=on_video_stop)

# ---------- Volume helpers ----------

def get_volume():
    """
    Returns current sink volume as int (0–100)
    """
    try:
        output = os.popen("pactl get-sink-volume 0").read()
        match = re.search(r'(\d+)%', output)
        if match:
            return int(match.group(1))
    except Exception:
        pass
    return None


def set_volume(volume):
    """
    Safely set volume, clamped between 0 and 100
    """
    volume = max(0, min(100, volume))
    os.system(f"pactl set-sink-volume 0 {volume}%")
    player.show_volume(volume)


def on_volume_up():
    current = get_volume()
    if current is None:
        return

    new_volume = min(100, current + 5)
    set_volume(new_volume)


def on_volume_down():
    current = get_volume()
    if current is None:
        return

    new_volume = max(0, current - 5)
    set_volume(new_volume)

# ---------- Callbacks ----------

def handle_valid_year(year, video_name):
    print(f"[+] Year accepted: {year}")

    gpio.set_all_high()
    slave.send("ALL_OFF")

    if gpio.check_if_year_local(year):
        pin = gpio.get_pin_from_master_year_dict(year)
        gpio.set_pin_low(pin)
    else:
        pin = gpio.get_pin_from_slave_year_dict(year)
        slave.send(f"{pin}_Low")

    player.play_by_name(video_name)


def handle_update_display(text):
    player.update_year_display(text)

# ---------- Keyboard listener ----------

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

# ---------- Start GUI ----------
player.start()