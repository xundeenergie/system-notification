#!/usr/bin/env python

import dbus, dbus.glib
import gtk
import datetime

systembus = dbus.SystemBus()
sessionbus = dbus.SessionBus()

notifications = dbus.Interface(sessionbus.get_object('org.freedesktop.Notifications', 
                                        '/org/freedesktop/Notifications'), 'org.freedesktop.Notifications')

#icon = gtk.icon_theme_get_default().lookup_icon("update-none", 22, 
#                         gtk.ICON_LOOKUP_USE_BUILTIN).get_filename()
icon = '/usr/share/icons/oxygen/base/48x48/actions/svn-update.png'


def notify_updates(*args):
    """format is defined here:
    https://developer.gnome.org/notification-spec/
    convert arguments from dbus.String to normal string with str() to avoid
    errors"""
    notifications.Notify("system notification", 0, icon, "%s" % (str(args[0])), 
            str(' '.join(args[1:])),
            "", {}, 0)

systembus.add_signal_receiver(notify_updates, 'Notification',
        'at.xundeenergie.notifications')


gtk.main()
