#!/usr/bin/python3 -u
import dbus
import datetime

class desktop_notification:
    def __init__(self, tag, signal_name='Notification_normal'):
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
        msg_dev = dict()
        msg_dev['sender'] = "mkbackup-dev"
        msg_dev['msgheader'] = "%s-backup" % (self.tag)
        msg_dev['msgbody'] = """Message Body 
\rNotification is sent to socket %s.
\r 
\rSent on %s %s
\r%s""" % (self.signal_name, self.date, self.time, '\n'.join(args))
        #msg_dev['urgency'] = '2'
        msg_dev['expiration_timeout'] = '-1'
        print('A',msg_dev, *msg_dev, type(msg_dev))
        message = dbus.lowlevel.SignalMessage(self.dbus_path, self.dbus_iface, self.signal_name)
        print('B',message.guess_signature(msg_dev))
        #message.append(*msg_dev, signature=message.guess_signature(*msg_dev))
        message.append(msg_dev)
        self.bus.send_message(message)

if __name__ == '__main__':
    cv = 'Testbody'

    notify = desktop_notification('Test-Header')
    notify.send_signal(cv) 

