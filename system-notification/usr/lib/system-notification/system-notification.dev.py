#!/usr/bin/env python

import dbus, dbus.glib, dbus.service
import gobject
import datetime
import notify2 as Notify
def my_callback_func(*args, **kwargs):
    print('my callback')
    #print('ARGS',args)
    #print('KWARGS',kwargs)
    import subprocess
    subprocess.Popen(['gio', 'open', 'backup'])


loop = gobject.MainLoop()
systembus = dbus.SystemBus()
sessionbus = dbus.SessionBus()

notifications = dbus.Interface(sessionbus.get_object(
    'org.freedesktop.Notifications', 
    '/org/freedesktop/Notifications'), 'org.freedesktop.Notifications')

urgencylevels = dict()
urgencylevels['URGENCY_LOW'] = 0
urgencylevels['URGENCY_NORMAL'] = 1
urgencylevels['URGENCY_CRITICAL'] = 2

class Handler:
    def __init__(self):
        #self.callbacks()
        pass

    def unwrap(self, val):
        if isinstance(val, dbus.ByteArray):
            return "".join([str(x) for x in val])
        if isinstance(val, (dbus.Array, list, tuple)):
            return [self.unwrap(x) for x in val]
        if isinstance(val, (dbus.Dictionary, dict)):
            return dict([(self.unwrap(x), self.unwrap(y)) for x, y in val.items()])
        if isinstance(val, dbus.ObjectPath):
            if val.startswith('/org/freedesktop/NetworkManager/'):
                classname = val.split('/')[4]
                classname = {
                    'Settings': 'Connection',
                    'Devices': 'Device',
                }.get(classname, classname)
                return globals()[classname](val)
        if isinstance(val, (dbus.Signature, dbus.String)):
            return unicode(val)
            #return str(val)
        if isinstance(val, dbus.Boolean):
            return bool(val)
        if isinstance(val, (dbus.Int16, dbus.UInt16, dbus.Int32, dbus.UInt32, dbus.Int64, dbus.UInt64)):
            return int(val)
        if isinstance(val, dbus.Byte):
            return bytes([int(val)])
        return val

    def simple_handler(self,*args, **kwargs):
        #self.__set_urgency(kwargs['urgency'])
        print('simple handler')
        #print('ARGS',args)
        #print('KWARGS',kwargs)
        #self.__send_notification(msgheader='simple Notification')
        notification = Notify.Notification("Hi!","Test Text","BLA")
        # The notification will have a button that says
        # "Reply to Message". my_callback_func is something
        # We will have to define
        notification.add_action(
            "action_click",
            "Reply to Message",
            my_callback_func,
            None # Arguments
        )
        notification.show()

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
        #argsuw = self.unwrap(args[0])
        argsuw = args[0]
        #print('A',argsuw.has_key('header'),argsuw,argsuw.keys())
        if argsuw.has_key('sender'): par['sender'] = str(argsuw['sender'])
        if argsuw.has_key('msgid'): par['msgid'] =   int(argsuw['msgid']) 
        if argsuw.has_key('icon'): par['icon']=      str(argsuw['icon']) 
        if argsuw.has_key('header'): par['header'] = str(argsuw['header']) 
        if argsuw.has_key('body'): par['body'] =     str(argsuw['body']) 
        if argsuw.has_key('actions'): par['actions'] =   argsuw['actions'] 
        if argsuw.has_key('hints'): par['hints']=   dict(argsuw['hints']) 
        if argsuw.has_key('expiration_timeout'): par['exptimeout'] = int(argsuw['expiration_timeout']) 
        if 'hints' not in vars() or 'hints' not in globals(): par['hints'] = dict()
        #par['hints']['urgency'] = int(self.urgency)
#        par['actions'] = list()
#        par['actions'].append('default')
#        par['actions'].append('')
#        par['actions'].append("open_filemanager('file:~/backup/')")
#        par['actions'].append('Open Backup')
#        par['actions'].append('callback')
#        par['actions'].append('TEST')

        Notify.init(par['sender'],mainloop='glib')
        notification = Notify.Notification(par['header'], par['body'])
        #print('ACT',par['actions'])
        #for i in par['actions']:print(i) 
        notification.add_action(
            "action_click",
            "Open Backups",
            my_callback_func,
            'action argument' # Arguments
        )
        notification.set_timeout(par['exptimeout'])
        notification.set_urgency(urgencylevels[par['urgency']])
        notification.show()



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

loop.run()
