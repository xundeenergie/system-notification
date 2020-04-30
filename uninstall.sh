#!/bin/bash

DOC_DIR=/usr/share/doc/system-notification
DBUS_DIR=/usr/share/dbus-1/services
LIB_DIR=/usr/lib/system-notification
SYSTEMD_USER_DIR=/etc/systemd/user
XDG_AUTOSTART_DIR=/etc/xdg/autostart

sudo rm "${DBUS_DIR}/at.xundeenergie.notifications.service"
sudo rm "${SYSTEMD_USER_DIR}/system-notification.service"
sudo rm "${XDG_AUTOSTART_DIR}/system-notification.desktop"

for i in "${DOC_DIR}" "${LIB_DIR}";do
    [ -d "${i}" ] && sudo rm -r "${i}"
done



