WordClock is a custom clock.

* Solder the shield together
* Connect the shield to the Pi
* Connect a 5V, 4A power brick to the shield.
* Connect the Pi to Ethernet (This assumes the Pi is Running Raspbian Jessie)
* Log in via SSH
* Setup Timezone by running `sudo raspi-config`
* Configure RTC: `https://www.raspberrypi.org/forums/viewtopic.php?f=66&t=125003`
* Get the right python libraries: https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/driving-matrices
* Clone this repo on the PI (or at least the software directory) and navigate into it
* Run `sudo make` in the "matrix" directory - Python will bind to the rgbmatrix.so file that is generated.
* Make WordClock.py executable: chmod +x WordClock.py
* Add this to crontab (`crontab -e`): `@reboot sudo /home/pi/WordClock.py > /dev/null 2>&1`
* Reboot
* The ethernet is no longer needed, but you can connect it briefly to auto-update the time if the RTC drifts.