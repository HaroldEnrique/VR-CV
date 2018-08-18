# Installation & Set Up guide for Leap Motion controller

### Install:
* Download and install "Python 2.6"
* Download and install SDK "Leap Motion Orion 3.2.1"

### Set Up:
1) Locate the SDK folder and the files, gestures.py and client.py on the same directory
2) From the SDK folder copy: Leap.py, LeapPython.so and libLeap.so outside of the folder, ie, same directory as gestures.py file

### Run:
1) Connect the leap motion controller
2) Open a terminal and run "sudo leapd"
3) Open another terminal and run gestures.py
* Optional: leap motion control panel, run in terminal "sudo LeapControlPanel --showsettings"
