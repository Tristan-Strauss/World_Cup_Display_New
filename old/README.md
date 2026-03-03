# World Cup Display


## Table of Contents
* [Required Equipment](#required-equipment)
* [Features](#features)
* [Install](#install)
    * [RPI Hardware Setup](#rpi-hardware-setup)
    * [RPI Software Setup](#rpi-software-setup)
        * [Master Pi](#master-pi-rpi4)
        * [Slave Pi](#slave-pi-rpi_zero)

## Required Equipment

1. GPIO jumper cables
2. Raspberry Pi 4 B+ 8GB Ram (hereby refered to as RPI4)
3. Raspberry Pi Zero 2 W (hereby refered to as RPI_Zero)

## Features

The Pi's talk over a serial connection with custom writen software
1. Listens for input from keypad
2. Receives year input and loads mp4 file
3. Play mp4 file and trigger GPIO pins for relay for LED for associated soccer ball

## Install

### RPI Hardware Setup

Take note of the following pinout on the raspberry pis
![image](./RPI_Pinout.png)

```
RPI4 pin 8 (GPIO 14 TXD) -> RPI_Zero pin 10 (GPIO 15 RXD)

RPI4 pin 10 (GPIO 15 RXD) -> RPI_Zero pin 8 (GPIO 14 TXD)

RPI4 pin 6 (Ground) -> RPI_Zero pin 6 (Ground)
```
RPI4 SD Card must be at least 64GB but ideally 128GB

RPI_Zero SD Card can be as low as 8GB

Both cards must be written with `Rasbian OS 64bit Lite` using the official Raspberry Pi imager software from there site [here](https://www.raspberrypi.com/software/)

### RPI Software Setup

#### Master Pi (RPI4)

Upgrade pi

```bash
sudo apt update ; sudo apt upgrade -y
```

Enable Serial connection

```bash
sudo raspi-config
# Choose Interface > Serial Port > [NO to login shell] > [Yes to enable serial]
# ESC to exit tui
```

Install desktop environment

```bash
sudo apt install lightdm -y
sudo apt install raspberrypi-ui-mods -y
```

Configure boot to use desktop environment

```bash
sudo raspi-config
# Choose System > Boot > [Choose desktop option (option 2 in my case)]
# ESC to exit tui
```

Configure auto login on pi

```bash
sudo rapsi-config
# Choose System > Auto Login > [Choose no to console and yes to desktop]
# ESC to exit tui
```

Reboot

```bash
sudo reboot
```

Install dependencies

```bash
sudo apt install git python3 python3-pip python3-venv -y
git clone https://github.com/Tristan-Strauss/World_Cup_Display.git
cd World_Cup_Display
```

Remove uneeded dependencies

```bash
sudo apt autoremove -y
```

Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create Crontab entry

```bash
sudo crontab -e
# Choose nano as default editor (option 1 in my case)
# Paste the following line in the crontab
# @reboot /home/pi/World_Cup_Display/venv/bin/python /hom/pi/World_Cup_Display/master.py
# Save with CTRL + x then y then ENTER
```

Reboot

```bash
sudo reboot
```

#### Slave Pi (RPI_Zero)

Upgrade pi

```bash
sudo apt update ; sudo apt upgrade -y
```

Enable Serial connection

```bash
sudo raspi-config
# Choose Interface > Serial Port > [NO to login shell] > [Yes to enable serial]
# ESC to exit tui
```

Reboot

```bash
sudo reboot
```

Install dependencies

```bash
sudo apt install git python3 python3-pip python3-venv -y
git clone https://github.com/Tristan-Strauss/World_Cup_Display.git
cd World_Cup_Display
```

Remove uneeded dependencies

```bash
sudo apt autoremove -y
```

Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create Crontab entry

```bash
sudo crontab -e
# Choose nano as default editor (option 1 in my case)
# Paste the following line in the crontab
# @reboot /home/pi/World_Cup_Display/venv/bin/python /hom/pi/World_Cup_Display/slave.py
# Save with CTRL + x then y then ENTER
```

Reboot

```bash
sudo reboot
```
