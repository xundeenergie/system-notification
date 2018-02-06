#!/usr/bin/python
"""Emmitter functionality."""
import dbus
import dbus.service
import dbus.glib


class Emitter(dbus.service.Object):
    """Emitter DBUS service object."""

    def __init__(self, bus_name, object_path):
        """Initialize the emitter DBUS service object."""
        dbus.service.Object.__init__(self, bus_name, object_path)

    @dbus.service.signal(dbus_interface='at.xundeenergie.Notification')
    def low(self,*args,**kwargs):
        """Emmit a test signal."""
        print 'Emitted a low test signal'

    @dbus.service.signal(dbus_interface='at.xundeenergie.Notification')
    def normal(self,*args,**kwargs):
        """Emmit a test signal."""
        print 'Emitted a normal test signal'

    @dbus.service.signal(dbus_interface='at.xundeenergie.Notification')
    def critical(self,*args,**kwargs):
        """Emmit a test signal."""
        print 'Emitted a critical test signal'

Simple_Notification = Emitter(dbus.SystemBus(),
        '/at/xundeenergie/notifications/simple/Notification')
Advanced_Notification = Emitter(dbus.SystemBus(),
        '/at/xundeenergie/notifications/advanced/Notification')

#Simple_Notification.low('M')
Advanced_Notification.normal(
        {'sender': 'emitter1.py', 'header': 'Testmessage', 'body': 'Test Body'})

