#!bin/bash
# This script is used to setup the environment for the project.
# Run this script as the pi user
# Run this script in the directory it is found in. IE: /path/to/World_Cup_Display/new/master/setup.sh

echo "Getting required system packages"
sudo apt update
sudo apt install -y python3-venv python3-pip

echo "Setting up tailscale. Please use link provided by tailscale to connect this device to your tailscale network."
curl -fsSL https://tailscale.com/install.sh | sh
sudo systemctl enable tailscaled
sudo tailscale up --authkey tskey-auth-kYSdVJXqsj11CNTRL-CpePqj27aL3smFuNLNHAL3n9eWUF5Mxab # This expires in 90 days, so you will need to generate a new one after that. You can do this in the Tailscale admin console.

echo "Setting up autostart for the World Cup Display - Slave"
mkdir -p ~/.config/systemd/user
cp ./world_cup_display.service ~/.config/systemd/user/

systemctl --user daemon-reexec
systemctl --user daemon-reload
systemctl --user enable world_cup_display.service
systemctl --user start world_cup_display.service

echo "Setting up python environment"
cd ../..
python3 -m venv venv
source venv/bin/activate

echo "Installing required python packages"
pip install -r new/slave/requirements.txt

echo "Setup complete. The World Cup Display - Slave will now start automatically on boot."