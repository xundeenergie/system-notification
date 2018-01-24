#!/usr/bin/env python

import dbus, dbus.glib
import gtk
import datetime

class SignalReceiver:
    def __init__(self,func='send_signal', signal_name='Notification', busname='at.xundeenergie.notifications',urgency=1):
        self.systembus = dbus.SystemBus()
        self.sessionbus = dbus.SessionBus()
        self.urgency = urgency
        self.icon = '/usr/share/icons/gnome/48x48/categories/preferences-system.png'
        self.notifications = dbus.Interface(self.sessionbus.get_object(
            'org.freedesktop.Notifications', 
            '/org/freedesktop/Notifications'), 'org.freedesktop.Notifications')
        function = getattr(self, func)
        self.systembus.add_signal_receiver(function, signal_name,
                busname)
        
    def __send_notification(
            self, sender='Notification', msgid=0, icon='', msgheader="Test-notification", 
            msgbody="This is a unconfigured notification", actions='', hints=dict(), exptimeout=-1):

        if len(icon) == 0:
            icon = '/usr/share/icons/gnome/48x48/categories/preferences-system.png'
        self.notifications.Notify( sender, msgid, icon, msgheader, msgbody,
            actions, hints, exptimeout)

    def send_signal(self, *args, **kwargs):
        """Send advanced messages to notification-daemon. Format see https://developer.gnome.org/notification-spec/
        convert arguments from dbus.String to normal string with str() to avoid
        errors
        all parameters are packed in one dictionary - sent over dbus"""
        par = dict()
        if args[0].has_key('sender'): par['sender'] = str(args[0]['sender'])
        if args[0].has_key('msgid'): par['msgid'] = int(args[0]['msgid']) 
        if args[0].has_key('icon'): par['icon']= str(args[0]['icon']) 
        if args[0].has_key('msgheader'): par['msgheader'] = str(args[0]['msgheader']) 
        if args[0].has_key('msgbody'): par['msgbody'] = str(args[0]['msgbody']) 
        if args[0].has_key('actions'): par['actions'] = str(args[0]['actions']) 
        if args[0].has_key('hints'): par['hints']= dict(args[0]['hints']) 
        if args[0].has_key('expiration_timeout'): par['exptimeout'] = int(args[0]['expiration_timeout']) 
        if 'hints' not in vars() or 'hints' not in globals(): hints = dict()
        hints['urgency'] = int(self.urgency)

        self.__send_notification( **par)

    def send_simple_signal(self, *args, **kwargs):
        """Send simple notifications. 3 strings
        sender (is shown on lockscreen)
        message title/header
        message body
        dbus-send --system /at/xundeenergie/notifications at.xundeenergie.notifications.Notification_simple_[low|normal|critical] string:"Sender" string:"Header" string:"Body" 
        """
        hints = dict()
        hints['urgency'] = int(self.urgency)
        self.__send_notification(str(args[0]), 0, self.icon, 
                str(args[1]), str(' '.join(args[2:])), "", hints, -1)

"""set Listeners for simple and advanced notifications on the 3 urgency-levels
low, normal and critical"""
Notification_low      = SignalReceiver(urgency=0,func='send_signal',signal_name='Notification_low')
Notification_normal   = SignalReceiver(urgency=1,func='send_signal',signal_name='Notification_normal')
Notification_critical = SignalReceiver(urgency=2,func='send_signal',signal_name='Notification_critical')
Notification_simple_low      = SignalReceiver(urgency=0,func='send_simple_signal',signal_name='Notification_simple_low')
Notification_simple_normal   = SignalReceiver(urgency=1,func='send_simple_signal',signal_name='Notification_simple_normal')
Notification_simple_critical = SignalReceiver(urgency=2,func='send_simple_signal',signal_name='Notification_simple_critical')


gtk.main()
