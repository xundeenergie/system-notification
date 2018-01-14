# system-notification
The problem is to send a desktop-notification from a system-service or cronjob to the notification-daemon from all graphical sessions.

I found only solutions which try to find out, which users are logged in, and then try to find out the graphical sessions from this users. Then you have to finde some environment-variables, use su or sudo to export this environment (f.e. $DISPLAY and $DBUS_SESSION_BUS_ADDRESS) and use notify-send for every single graphical session for every logged in user.
This is not practicable, needs much code for each login-manager (logind, console-kit...) and even the use of su or sudo.

## Using dbus ##
Or you can just use dbus' sessionbus and a listener-service in each graphical session.

You script or service sends a message to dbus-systembus.
Start a listener-service with xdg-autostart, which listens on the systembus, takes the message and send ist further to the local notification-daemon.

This package is this listener-service implemented in python3. 

Be careful, you have a notification-service running. This is standard in gnome3, kde and xfce. For windowmanagers like dwm, fvwm or openbox/fluxbox you have to install and run one. Try dunst, xfce4-notifyd or notify-osd.

Try if a notification-daemon is running:

    notify-send Testheader Testbody

You must see a desktop-notification immediateiy.

### Run it from shell (or test it) ###
So you can install this listener-service and the autostart-entry, log out and relogin.

Then you can test the new service. Run the following command from a terminal as you user, as user root, from a test-unit in systemd or even from debug-shell from systemd:

    dbus-send --system /at/xundeenergie/notifications at.xundeenergie.notifications.Notification string:"Test Header" string:"Testbody"

### Run it from python###
Use the bindings for dbus. You can find a test-implementation in /usr/share/doc/system-notification/notification-example.py

### Run it from other language###
If someone is able to write a implementation for perl, C, or other languages, feel free, and share this with my repo.

