WordClock
---------
It's a Wordclock!  See a full walkthrough of the build on my website: https://www.jeremyblum.com/2016/02/03/wordclock/

### Setup Instructions for the WordClock's Raspberry Pi

* Prep a Raspberry Pi.
    * These instructions have been tested on a Raspberry Pi 2 B running The "Buster" Raspbian Lite OS Build (Kernel version 5.4.72+), but newer Pi hardware should work too.
    * Create an SD card with the Raspbian Lite OS Image (no Desktop GUI is needed for this)
    * To enable headless setup, add a file called `ssh` to the boot partition root directoy (no extension). This will enable SSH on boot by default.
    * If you are using a Wi-Fi USB dongle instead of Ethernet, plug it in, and [configure the wpa_supplicant.conf file](https://www.raspberrypi.org/documentation/configuration/wireless/headless.md) in the boot partition so that the pi automatically connects on boot.
* Solder the shield (https://www.adafruit.com/product/2345) together, and add a jumper wire between pins 4 and 18 so that the RGB library can be run in the highest quality mode. This is described in the Adafruit documentation linked below.
* Connect the shield to the Pi, and install the coincell battery for the RTC
* Connect the Pi to Ethernet, or install a supported Wi-Fi dongle into one of the USB ports if you haven't already.
* Connect a 5V, 4A power brick to the shield.
* Power on the Pi, and connect via SSH using the default password. (Check your router for the DHCP-assigned IP address)
* Setup the time zone and change the default password by running `sudo raspi-config`. I also suggest expanding the SD card partition and reducing GPU memory to the minimum since the Pi is running headless.
* Install all the latest updates using `sudo apt update && sudo apt dist-upgrade -y`. Reboot when complete.
* SSH back in and run this command to download and run an installer script (forked from Adafruit to use a newer library version): `curl https://raw.githubusercontent.com/sciguy14/Raspberry-Pi-Installer-Scripts/master/rgb-matrix.sh > rgb-matrix.sh && sudo bash rgb-matrix.sh`. This will install the RGB panel libraries and help configure the RTC. Run the script from the home directory (/home/pi). Choose the "QUALITY" option when prompted if you've added the solder jumper described earlier. Reboot when complete.
* Install pip for python3 and numpy: `sudo apt install -y python3-pip libatlas3-base libgfortran5 && sudo pip3 install numpy`
* Set the RTC Time
    * Run `date` to confirm that the date/time that was retreived from the network time server is correct. If not, check your timezone settings.
    * Run `sudo hwclock -w` to write the current datetime to the RTC.
    * Read it back with `sudo hwclock -r` and confirm it is correct.
* SSH back into the Pi and clone this repo to your home directory (`git clone https://github.com/sciguy14/WordClock.git`). You should now have a `WordClock` folder and a `rpi-rgb-led-matrix` folder in your /home/pi directory. You can delete the `rgb-matrix.sh` that was used to install the libraries.
* Confirm that everything is functional by running one of the library demos: `sudo /home/pi/rpi-rgb-led-matrix/examples-api-use/demo -t 10 -D 4`
* Navigate into the `WordClock/Software/` directory and make `WordClock.py` executable: `chmod +x WordClock.py`
* Install screen: `sudo apt install screen`
* Add this to crontab (`crontab -e`): `@reboot screen -dmS wordclock sudo /home/pi/WordClock/Software/WordClock.py`. By launching the script in a screen, you can easily ssh in and attach to the already running session to see debug output without having to kill and manuall relaunch it.
* Reboot.
* The wordclock should run and show the time after reboot. It is no longer necessary to keep the wordclock connected to Wi-Fi/Ethernet, as the onboard RTC will keep time. But you can keep it connected if you want to ensure that you stay syncronized with the network time server.

License
-------
This work is licensed under the [GNU GPL v3](http://www.gnu.org/licenses/gpl.html).
Please share improvements or remixes with the community, and attribute me (Jeremy Blum, <http://www.jeremyblum.com>) when reusing portions of my code.