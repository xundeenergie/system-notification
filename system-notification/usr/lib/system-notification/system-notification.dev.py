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
        print('Function established',func,signal_name)
        function = getattr(self, func)
        print(func,'FUNCTION',function)
        self.systembus.add_signal_receiver(function, signal_name,
                busname)

    def send_sig(self, *args, **kwargs):
        sender           = str(args[0]['sender']) if args[0].has_key('sender') else 'Notification'
        msgid            = int(args[0]['msgid']) if args[0].has_key('msgid') else 0
        icon             = str(args[0]['icon']) if args[0].has_key('icon') else self.icon
        msgheader        = str(args[0]['msgheader']) if args[0].has_key('msgheader') else 'Notification'
        msgbody          = str(args[0]['msgbody']) if args[0].has_key('msgbody') else 'This is a default-notification'
        actions          = str(args[0]['actions']) if args[0].has_key('actions') else ''
        hints            = dict(args[0]['hints']) if args[0].has_key('hints') else dict()
        exptimeout       = int(args[0]['expiration_timeout']) if args[0].has_key('expiration_timeout') else -1
        hints['urgency'] = int(self.urgency)

    def send_notification(self, sender='Notification', msgid=0, icon=self.icon,
            msgheader="Test-notification", msgbody="This is a
            unconfigured notification",
            actions='', hints=dict(), exptimeout=-1):
        self.notifications.Notify(
                sender, 
                msgid, 
                icon,
                msgheader, 
                msgbody,
                actions, 
                hints, 
                exptimeout)

    def send_simple_sig(self, *args, **kwargs):
        hints = dict()
        hints['urgency'] = int(self.urgency)
        self.notifications.Notify(
                str(args[0]), 
                0, 
                self.icon,
                str(args[1]), 
                str(' '.join(args[2:])),
                "", 
                hints, 
                -1)



    def send_signal_decor(setvars):
        def wrapper(self, *args, **kwargs):
            print("Before",self.icon,dir(wrapper.func_globals['Notification_simple_low'].send_signal))
            setvars(self,*args, **kwargs)
            self.notifications.Notify(
                    self.sender, 
                    self.msgid, 
                    self.icon,
                    self.msgheader, 
                    self.msgbody,
                    self.actions, 
                    self.hints, 
                    self.exptimeout)
            print("After")
        return(wrapper)

    @send_signal_decor
    def send_signal(self,*args,**kwargs):
        print('send_sig')
        sender           = str(args[0]['sender']) if args[0].has_key('sender') else 'Notification'
        self.sender           = str(args[0]['sender']) if args[0].has_key('sender') else 'Notification'
        self.msgid            = int(args[0]['msgid']) if args[0].has_key('msgid') else 0
        self.icon             = str(args[0]['icon']) if args[0].has_key('icon') else self.icon
        self.msgheader        = str(args[0]['msgheader']) if args[0].has_key('msgheader') else 'Notification'
        self.msgbody          = str(args[0]['msgbody']) if args[0].has_key('msgbody') else 'This is a default-notification'
        self.actions          = str(args[0]['actions']) if args[0].has_key('actions') else ''
        self.hints            = dict(args[0]['hints']) if args[0].has_key('hints') else dict()
        self.exptimeout       = int(args[0]['expiration_timeout']) if args[0].has_key('expiration_timeout') else -1
        self.hints['urgency'] = int(self.urgency)

        
    @send_signal_decor
    def send_simple_signal(self,*args,**kwargs):
        print('send_simple_sig')
        print(args)
        sender           = str(args[0])
        self.sender           = str(args[0])
        self.msgid            = 0
        self.icon             = self.icon
        self.msgheader        = str(args[1])
        self.msgbody          = str(' '.join(args[2:]))
        self.actions          = ''
        self.hints            = dict()
        self.exptimeout       = -1
        self.hints['urgency'] = int(self.urgency)


Notification_low      = SignalReceiver(urgency=0,func='send_signal',signal_name='Notification_low')
Notification_normal   = SignalReceiver(urgency=1,func='send_signal',signal_name='Notification_normal')
Notification_critical = SignalReceiver(urgency=2,func='send_signal',signal_name='Notification_critical')
Notification_simple_low      = SignalReceiver(urgency=0,func='send_simple_signal',signal_name='Notification_simple_low')
Notification_simple_normal   = SignalReceiver(urgency=1,func='send_simple_signal',signal_name='Notification_simple_normal')
Notification_simple_critical = SignalReceiver(urgency=2,func='send_simple_signal',signal_name='Notification_simple_critical')


gtk.main()
