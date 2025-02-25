WordClock
---------
It's a Wordclock!  See a full walkthrough of the build on my website: https://www.jeremyblum.com/2016/02/03/wordclock/

### Setup Instructions for the WordClock's Raspberry Pi

* Prep a Raspberry Pi.
    * These instructions have been tested on the following configurations (others should work too, but as of Feb 2025, the matrix driving library is [NOT yet supported on the Pi 5](https://github.com/hzeller/rpi-rgb-led-matrix/issues/1603), so stick to an earlier Pi for now):
        * Raspberry Pi 1 Model B+ Rev 1.2 (512MB RAM) running the 32bit "Buster" Raspbian Lite OS Build (Kernel version 5.4.72)
        * Raspberry Pi 3 Model B Rev 1.2 (1GB RAM) running the 64bit "Bookworm" Raspian Lite OS Build (Kernel version 6.6.74)
    * Create an SD card with the Raspbian Lite OS Image (no Desktop GUI is needed for this). The official [Raspberry Pi Imager](https://www.raspberrypi.com/software/) is the easiest way to do this.
    * During imaging, choose the option to edit the boot config to enable SSH, and to enter Wi-Fi credentials (if you will be using it wirelessly). I also recommend setting a custom username, and enabling key based login instead of password login.
* Solder the shield (https://www.adafruit.com/product/2345) together, and add a jumper wire between pins 4 and 18 so that the RGB library can be run in the highest quality mode. This is described in the [Adafruit documentation](https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/driving-matrices#step-2995409).
* Connect the shield to the Pi, and install the coincell battery for the RTC.
* Connect the Pi to the network either via Ethernet, integrated Wi-Fi or a Wi-Fi USB dongle on older Pi's.
* Connect a 5V, 4A power brick to the shield.
* Power on the Pi, and connect via SSH. Check your router for the DHCP-assigned IP address, or use the mDNS local hostname that you assigned via the config options during SD card creation.
* Install all the latest updates using `sudo apt update && sudo apt dist-upgrade -y`. Reboot when complete, then SSH back in.
* Setup the time zone and change the default password (if you didn't already do so as part of sd card creation) by running `sudo raspi-config`. On older Pis, running an older Raspbian OS with minimal RAM, you can also reduce the GPU memory to the minimum since the Pi is running headless, leaving more for the CPU. You shouldn't need to do that on a Pi with >=1GB of RAM.
* SSH back into the pi. Ensure you are in your home directory (`cd ~/`).
* Run this command to download and run an installer script: `curl https://raw.githubusercontent.com/sciguy14/Raspberry-Pi-Installer-Scripts/refs/heads/master/rgb-matrix.sh > rgb-matrix.sh && sudo bash rgb-matrix.sh`. This will install the RGB panel libraries and help configure the RTC. Note that this is my fork of the Adafruit installer to resolve some issues when used on the latest bookworm release.
    * Choose the "HAT + RTC option".
    * Choose to include RTC support.
    * Choose the "QUALITY" option when prompted if you've added the solder jumper described earlier.
    * If you have multi-core Pi, you'll be prompted to choose if you want to enable core isolation. This is recommended to maximize display performance while other tasks are running.
    * Reboot when complete.
* SSH back into the Pi after the reboot.
* Install necessary packages to run my python script: `sudo apt install -y git screen python3-pip libatlas3-base libgfortran5 python3-numpy`
* Set the RTC Time
    * Run `date` to confirm that the date/time that was retreived from the network time server is correct. If not, check your timezone settings.
    * Run `sudo hwclock -w` to write the current datetime to the RTC.
    * Read it back with `sudo hwclock -r` and confirm it is correct.
* Navigate to your home directory if not already there: `cd ~/`
* Clone this repo to your home directory: `git clone https://github.com/sciguy14/WordClock.git`
* You should now have a `WordClock` folder and a `rpi-rgb-led-matrix` folder in your home directory. You can optionally delete the `rgb-matrix.sh` that was used to install the libraries.
* Confirm that everything is functional by running one of the library demos first: `sudo ~/rpi-rgb-led-matrix/examples-api-use/demo -D 4` (Hit Ctrl-C to exit the demo mode)
* Navigate into the `WordClock/Software/` directory and make `WordClock.py` executable: `cd ~/WordClock/Software; chmod +x WordClock.py`
* Add a crontab entry to launch the WordClock software in a screen session on boot:
    * Run this command: `( crontab -l | grep -v -F "wordclock" ; echo "@reboot screen -dmS wordclock sudo /home/${USER}/WordClock/Software/WordClock.py" ) | crontab -`
    * A cron entry is now installed. By launching the script in a screen session, you can easily ssh in and attach to the already running session to see debug output without having to kill and manually relaunch it: SSH back in anytime and run `screen -r` to attach to the running instance and hit `ctrl-A, d` to detach.
* Reboot.
* The wordclock should run and show the time after reboot. It is no longer necessary to keep the wordclock connected to Wi-Fi/Ethernet, as the onboard RTC will keep time. But you can keep it connected if you want to ensure that you stay syncronized with the network time server.

License
-------
(C) 2025 Jeremy Blum
This work is licensed under the [GNU GPL v3](http://www.gnu.org/licenses/gpl.html).
Please share improvements or remixes with the community, and attribute me (Jeremy Blum, <https://www.jeremyblum.com>) when reusing portions of my code.