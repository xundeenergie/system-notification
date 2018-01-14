#!/usr/bin/python3 -u
import dbus
import datetime

class desktop_notification:
    def __init__(self, tag, signal_name='Notification'):
        self.tag          = tag
        self.dbus_path    = "/at/xundeenergie/notifications"
        self.dbus_iface   = "at.xundeenergie.notifications"
        self.dbus_busname = "at.xundeenergie.notifications"
        self.timestamp    = datetime.datetime.now()
        self.time         = self.timestamp.strftime('%H:%M:%S')
        self.date         = self.timestamp.strftime('%d. %B. %Y')
        self.bus          = dbus.SystemBus()
        self.signal_name  = signal_name

    def send_signal(self, *args):
        """Send a signal on the bus."""
        signature=''
        print(' '.join(args))
        msg = [self.tag, ' '.join(args)]
        for i in msg:
            if type(i) is float:
                signature += 'd' 
            elif type(i) is int:
                signature += 'i' 
            elif type(i) is str:
                signature += 's' 
            else:
                signature += 'v'

        message = dbus.lowlevel.SignalMessage(self.dbus_path, self.dbus_iface, self.signal_name)
        message.append(signature=signature, *msg)
        #message.append(*msg)
        self.bus.send_message(message)

if __name__ == '__main__':
    cv = 'Testbody'

    notify = desktop_notification('Test-Header')
    notify.send_signal(cv) 

