read -p "Master or Slave? (m/s): " type

if ! type == "m" && ! type == "s"
then
    echo "Invalid input. Please enter 'm' for Master or 's' for Slave."
    exit 1
fi

sudo apt update ; sudo apt upgrade -y
sudo apt install git python3 python3-pip python3-venv -y
git clone https://github.com/Tristan-Strauss/World_Cup_Display.git
cd World_Cup_Display
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
sudo apt autoremove -y

if type == "m"
then
    sudo apt install lightdm -y
    sudo apt install raspberrypi-ui-mods -y
    sudo apt install vlc -y
    clear
    echo "Please reboot the pi and then run sudo raspi-config"
    echo "System > Boot > [Choose desktop option]"
    echo "System > Auto Login > Desktop Autologin"
    echo "Interface > Serial Port > [NO to login shell] > [YES to serial port hardware]"
    echo "Finish and reboot"
fi

if type == "s"
then
    echo "Please reboot the pi and then run sudo raspi-config"
    echo "Interface > Serial Port > [NO to login shell] > [YES to serial port hardware]"
    echo "Finish and reboot"
fi
