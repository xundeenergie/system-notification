#!/bin/bash

DOC_DIR=/usr/share/doc/system-notification
DBUS_DIR=/usr/share/dbus-1/services
LIB_DIR=/usr/lib/system-notification
SYSTEMD_USER_DIR=/etc/systemd/user
XDG_AUTOSTART_DIR=/etc/xdg/autostart

for i in "${DOC_DIR}" "${DBUS_DIR}" "${LIB_DIR}" "${SYSTEMD_USER_DIR}" "${XDG_AUTOSTART_DIR}";do
    [ -d "${i}" ] || sudo mkdir -p "${i}"
done

sudo cp ./usr/share/doc/system-notification/system-notification-example.py "${DOC_DIR}"
sudo cp ./usr/share/doc/system-notification/system-notification-example.simple.py "${DOC_DIR}"
sudo cp ./usr/share/doc/system-notification/emitter1.py "${DOC_DIR}"
sudo cp ./usr/lib/system-notification/system-notification.py "${LIB_DIR}"
sudo cp ./usr/lib/system-notification/system-notification.simple.py "${LIB_DIR}"
sudo cp ./usr/share/dbus-1/services/at.xundeenergie.notifications.service "${DBUS_DIR}"
sudo cp ./etc/systemd/user/system-notification.service "${SYSTEMD_USER_DIR}"
sudo cp ./etc/xdg/autostart/system-notification.desktop "${XDG_AUTOSTART_DIR}"


