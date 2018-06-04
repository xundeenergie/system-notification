#!/usr/bin/env python

import dbus, dbus.glib, dbus.service
import gobject
import datetime
import notify2 as Notify
Notify.init('Notifications', mainloop='glib')

import sys
from os.path import expanduser
import uuid


loop = gobject.MainLoop()
systembus = dbus.SystemBus()
sessionbus = dbus.SessionBus()

urgencylevels = dict()
urgencylevels['URGENCY_LOW'] = 0
urgencylevels['URGENCY_NORMAL'] = 1
urgencylevels['URGENCY_CRITICAL'] = 2

class Handler():
    def __init__(self):
        self.callbacks = {'my_callback_func': self.my_callback_func,
                'pathopen': self.pathopen }
        #self.callbacks()
        pass

    def my_callback_func(self, *args, **kwargs):
        print('my callback')
        #print('ARGS',args)
        #print('KWARGS',kwargs)
        import subprocess
        subprocess.Popen(['gio', 'open', 'backup'])
        #self.notifications.close()

    def pathopen(self, *args, **kwargs):
        print('callback open path')
        print('ARGS',args)
        print('KWARGS',kwargs)
        
        if len(args) > 2:
            import subprocess
            subprocess.Popen(['gio', 'open', expanduser(args[2])])
        #self.notification.show()
        self.notification.close()

    def closed_cb(self, n):
        print("Notification closed")
        self.notification.close()
        #loop.quit()

    def simple_handler(self,*args, **kwargs):
        print('simple handler')
        self.notification = Notify.Notification("Hi!","Test Text","BLA")
        # The notification will have a button that says
        # "Reply to Message". my_callback_func is something
        # We will have to define
        self.notification.add_action(
            "action_click",
            "Reply to Message",
            my_callback_func,
            None # Arguments
        )
        self.notification.show()

    def advanced_handler(self,*args, **kwargs):
        #self.__set_urgency(kwargs['urgency'])
        print('advanced handler')
        print('ARGS',args)
        #print('KWARGS',kwargs)
        """Send advanced messages to notification-daemon. Format see https://developer.gnome.org/notification-spec/
        convert arguments from dbus.String to normal string with str() to avoid
        errors
        all parameters are packed in one dictionary - sent over dbus"""
        par = dict()
        par['sender'] = 'System Notification'
        par['header'] = 'Unconfigured Summary'
        par['body'] = 'Unconfigured Body'
        par['actions'] = ''
        par['hints'] = ''
        par['exptimeout'] = -1
        par['icon'] = '/usr/share/icons/gnome/48x48/categories/preferences-system.png'
        par['urgency'] = 'URGENCY_' + str(kwargs['urgency']).upper()
        if args[0].has_key('sender'): par['sender'] = str(args[0]['sender'])
        if args[0].has_key('msgid'): par['msgid'] =   int(args[0]['msgid']) 
        if args[0].has_key('icon'): par['icon']=      str(args[0]['icon']) 
        if args[0].has_key('header'): par['header'] = str(args[0]['header']) 
        if args[0].has_key('body'): par['body'] =     str(args[0]['body']) 
        if args[0].has_key('actions'): par['actions'] = args[0]['actions'].split(',') 
        if args[0].has_key('hints'): par['hints']=   dict(args[0]['hints']) 
        if args[0].has_key('expiration_timeout'): par['exptimeout'] = int(args[0]['expiration_timeout']) 
        if 'hints' not in vars() or 'hints' not in globals(): par['hints'] = dict()
        #par['hints']['urgency'] = int(self.urgency)
#        par['action'] = list()
#        for i in par['actions']: par['action'].append
#        cb = 'pathopen'
#        par['action'].append('openbackup')
#        par['action'].append('Open Backup')
#        par['action'].append(cb)
#        par['action'].append(expanduser('~/backup'))
    

        #Notify.init(par['sender'],mainloop='glib')
        server_capabilities = Notify.get_server_caps()
        self.notification = Notify.Notification(par['header'], message=par['body'],
                icon=par['icon'])
        i=0
        ap=dict()
        if ('actions' in server_capabilities):
            for a in par['actions']:
                if i == 0: ap[i]=uuid.uuid4().hex 
                if i == 0: ap[i+1]=a
                if i == 1: ap[i+1]=self.callbacks[a] if a in self.callbacks else None
                if i == 2: ap[i+1]=a
                i += 1
                if i >= 3:
                    #notification.add_action(
                    #    "uniq short summary",
                    #    "Title shown on button",
                    #    my_callback_func,
                    #    'action argument' # Arguments
                    #)
                    self.notification.add_action( ap[0], ap[1], ap[2], ap[3])
                    i=0
        self.notification.set_timeout(par['exptimeout'])
        self.notification.set_urgency(urgencylevels[par['urgency']])
        self.notification.connect('closed', self.closed_cb)
        
        if not self.notification.show():
            print("Failed to send notification")
            sys.exit(1)



handler = Handler()

systembus.add_signal_receiver(handler.simple_handler,
        dbus_interface='at.xundeenergie.Notification',
        path='/at/xundeenergie/notifications/simple/Notification',
        signal_name='low',
        member_keyword='urgency')

systembus.add_signal_receiver(handler.simple_handler,
        dbus_interface='at.xundeenergie.Notification',
        path='/at/xundeenergie/notifications/simple/Notification',
        signal_name='normal',
        member_keyword='urgency')

systembus.add_signal_receiver(handler.simple_handler,
        dbus_interface='at.xundeenergie.Notification',
        path='/at/xundeenergie/notifications/simple/Notification',
        signal_name='critical',
        member_keyword='urgency')

systembus.add_signal_receiver(handler.advanced_handler,
        dbus_interface='at.xundeenergie.Notification',
        path='/at/xundeenergie/notifications/advanced/Notification',
        signal_name='low',
        member_keyword='urgency')

systembus.add_signal_receiver(handler.advanced_handler,
        dbus_interface='at.xundeenergie.Notification',
        path='/at/xundeenergie/notifications/advanced/Notification',
        signal_name='normal',
        member_keyword='urgency')

systembus.add_signal_receiver(handler.advanced_handler,
        dbus_interface='at.xundeenergie.Notification',
        path='/at/xundeenergie/notifications/advanced/Notification',
        signal_name='critical',
        member_keyword='urgency')

#loop.run()
# Run the loop
try:
    # Create our initial objects
    #from dbustest.random_data import RandomData
    #RandomData(bus_name)

    loop.run()
except KeyboardInterrupt:
    print("keyboard interrupt received")
except Exception as e:
    print("Unexpected exception occurred: '{}'".format(str(e)))
finally:
    loop.quit()
