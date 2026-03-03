#!bin/bash
# This script is used to setup the environment for the project.
# Run this script as the pi user
# Run this script in the directory it is found in. IE: /path/to/World_Cup_Display/new/master/setup.sh

echo "Getting required system packages"
sudo apt update
sudo apt install -y python3-venv python3-pip
sudo apt install -y mpv numlockx

echo "Setting up tailscale. Please use link provided by tailscale to connect this device to your tailscale network."
curl -fsSL https://tailscale.com/install.sh | sh
sudo systemctl enable tailscaled
sudo tailscale up

echo "Setting up autostart for the World Cup Display - Master"
mkdir -p ~/.config/autostart
cp ./world_cup_display.desktop ~/.config/autostart/

echo "Setting up python environment"
cd ../..
python3 -m venv venv
source venv/bin/activate

echo "Installing required python packages"
pip install -r new/master/requirements.txt

echo "Setup complete. The World Cup Display - Master will now start automatically on boot."
echo "Please follow the below instructions for setting up numlockx:"
echo "1. Open the configuration file:"
echo "sudo nano /etc/lightdm/lightdm.conf"
echo "Uncomment and modify the line:"
echo "2. greeter-setup-script=/usr/bin/numlockx on"