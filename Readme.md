

Configure i2C Support:
https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c

Setup Timezone in `sudo raspi-config`

Configure RTC:
https://learn.adafruit.com/adding-a-real-time-clock-to-raspberry-pi/set-rtc-time

Get the right python libraries:
https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/driving-matrices

Clone this repo on the PI (or at least the software directory) and navigate into it
Run `sudo make` in the "matrix" directory - Python will bind to the rgbmatrix.so file that is generated.
Make WordClock.py executable.