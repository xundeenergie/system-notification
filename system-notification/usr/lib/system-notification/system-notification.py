#!/usr/bin/env python

import dbus, dbus.glib
import gtk
import datetime

systembus = dbus.SystemBus()
sessionbus = dbus.SessionBus()
notifications = dbus.Interface(sessionbus.get_object(
    'org.freedesktop.Notifications', 
    '/org/freedesktop/Notifications'), 'org.freedesktop.Notifications')

#class SignalReceiver(dbus.service.Object):
#     """Emitter DBUS service object."""
#
#    def __init__(self, bus_name, object_path):
#        """Initialize the emitter DBUS service object."""
#        dbus.service.Object.__init__(self, bus_name, object_path)
#
#    @dbus.service.signal('tld.domain.sub.event')
#    def test(self):
#        """Emmit a test signal."""
#        print 'Emitted a test signal'
#
#    @dbus.service.signal('tld.domain.sub.event')
#    def quit_signal(self):
#        """Emmit a quit signal."""
#        print 'Emitted a quit signal'
#
#    def __init__(self):
#
#        print('V')
##        self.systembus = dbus.SystemBus()
##        self.sessionbus = dbus.SessionBus()
##        self.notifications = dbus.Interface(self.sessionbus.get_object(
##            'org.freedesktop.Notifications', 
##            '/org/freedesktop/Notifications'), 'org.freedesktop.Notifications')
#        #print(dir(self.notifications.connect_to_signal))
#        #self.notifications.connect_to_signal('ActionInvoked',self.callback,'org.freedesktop.Notifications')
#        notifications.connect_to_signal('ActionInvoked',self.callback, 'org.freedesktop.Notifications')
#        #sessionbus.add_signal_receiver(self.callback(), 'ActionInvoked',
#        #        'org.freedesktop.Notifications')
#
#    def callback(*args, **kwargs):
#        
#        print('CALLBACK', type(args))
##        print('ARGS',args)
#        print('A',dir(args[0]))
#        print('A',args[0])
##        print('B',args[0].callback)
##        print('B',args[0].icon)
##        print('B',args[0].notifications)
##        print('B',args[0].send_signal)
##        print('B',args[0].send_simple_signal)
##        print('B',args[0].sessionbus)
##        print('B',args[0].systembus)
##        print('C',args[0].urgency)
#        #args[0].open_filemanager(args[1])
#
##        print('KWARGS')
##        for i in kwargs:
##            print(i, type(i), dir(i))
#
#    def open_filemanager(self,*args):
#        print('X Open Filemanager')
#"""

class SignalProxy:
    def __init__(self,urgency=1, ntype='advanced',dbus_interface='at.xundeenergie.notifications'):

        self.urgency = urgency
        
        if ntype == 'advanced': z=''
        elif ntype == 'simple': z='simple_'
        else: z='simple_'
        function = getattr(self, 'send_'+z+'signal')


        if urgency == 0:
            self.signal_name='Notification_low'
        elif urgency == 1:
            self.signal_name='Notification_normal'
        elif urgency == 2:
            self.signal_name='Notification_critical'
        else:
            self.urgency = 1
            self.signal_name='Notification_normal'
            

        systembus.add_signal_receiver(function, signal_name=self.signal_name,
                dbus_interface=dbus_interface+'.'+ntype)

    def __send_notification(self,
            sender='Notification', msgid=0, icon='', msgheader="Test-notification", 
            msgbody="This is a unconfigured notification", actions='', hints=dict(), exptimeout=-1):

        print('Y',msgbody)
        if len(icon) == 0:
            icon = '/usr/share/icons/gnome/48x48/categories/preferences-system.png'
        notifications.Notify( sender, msgid, icon, msgheader, msgbody,
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
        if args[0].has_key('actions'): par['actions'] = args[0]['actions'] 
        if args[0].has_key('hints'): par['hints']= dict(args[0]['hints']) 
        if args[0].has_key('expiration_timeout'): par['exptimeout'] = int(args[0]['expiration_timeout']) 
        if 'hints' not in vars() or 'hints' not in globals(): par['hints'] = dict()
        par['hints']['urgency'] = int(self.urgency)
        par['actions'] = list()
        par['actions'].append('default')
        par['actions'].append('')
        par['actions'].append("open_filemanager('file:~/backup/')")
        par['actions'].append('Open Backup')
        par['actions'].append('callback')
        par['actions'].append('TEST')

        print('PAR',par)

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

Notification_low      = SignalProxy(urgency=0)
Notification_normal   = SignalProxy(urgency=1)
Notification_critical = SignalProxy(urgency=2)
Notification_simple_low      = SignalProxy(urgency=0,ntype='simple')
Notification_simple_normal   = SignalProxy(urgency=1,ntype='simple')
Notification_simple_critical = SignalProxy(urgency=2,ntype='simple')



#Recvr = SignalReceiver()

gtk.main()
