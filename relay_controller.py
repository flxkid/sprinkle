#!/usr/bin/env python2.7
"""This module provides an interface to relays connected to GPIO pins. The relays are considered to
be part of a "controller" which is simply a collection of relays (you might define a controller to
match with an actual multi-channel relay board, although this isn't required)."""

# wiringpi uses a lil different pin numbering scheme. It's not physical pin or GPIO, it's their
# own setup. You can see the reference to it here: https://projects.drogon.net/raspberry-pi/wiringpi/pins/
from datetime import datetime
import time
import threading
import wiringpi

class Relay(object):
    """ This class defines the basic operation of a relay connected via a GPIO pin. It
    includes Threading support to allow a relay to be "turned on" (closed) for a period
    of time after which it is automatically "turned off" (opened)"""

    CLOSED = 1
    OPEN = 0
    UNKNOWN = -1

    gpio_pin = 0
    ordinal_pos = 0
    name = ''
    interruptor = None

    def __init__(self, pin, position=0, state=-1, name='', interruptor=None):
        self.gpio_pin = pin
        self.ordinal_pos = position
        self.name = name
        self.interruptor = interruptor
        wiringpi.pinMode(self.gpio_pin, 1) # set the pin to output mode
        
        # If no initial state is passed, then don't assume any state is correct, leave
        # it as-is.
        if (state <> self.UNKNOWN):
            self.set_state(state)

    def get_state(self):
        return wiringpi.digitalRead(self.gpio_pin)

    def set_state(self, relay_state):
        wiringpi.digitalWrite(self.gpio_pin, relay_state)
    
    def _close(self, duration):
        self.set_state(self.CLOSED)
        started_at = datetime.now()
        while not self.interruptor.is_set():
            time.sleep(0) # pass control to other threads
            if (datetime.now() - started_at).total_seconds() > duration:
                break

        self.set_state(self.OPEN)

    def close(self, duration=10):
        t = threading.Thread(target=self._close, args=(duration,))
        t.start()
       
class RelayController(object):
    """This class is what is used to talk to a relay rather than using the relay class directly."""
    channels = 0
    relays = []

    # The "interruptor" is used to stop relay channels that have a threaded function
    # sleeping, waiting to "open" or shut off a relay for a duration. If that duration
    # needs to be interrupted, then the interruptor can be "Set". This will interrupt
    # ALL currently sleeping relays!
    interruptor = threading.Event()

    def __init__(self, relays=None):
        wiringpi.wiringPiSetup()
        if isinstance(relays, list):
            for idx, channel in enumerate(relays, start=1):
                # if there isn't a position in the dictionary, set it based on where in the 
                # array it is so that each channel is numbered ordinally.
                if not "position" in channel:
                    channel["position"] = idx
                channel["interruptor"] = self.interruptor
                self.relays.append(Relay(**channel))
        else:
            raise KeyError("Pass a list of format: [{'name': 'front', 'pin': 1, 'latching': False, 'position': 1, 'state': relay.UNKNOWN}]")
        
        self.channels = len(relays)
        self.open_all()

    def open_all(self):
        """ This can be used to "turn off" all relays immediately. We also set and clear our interruptor so
        that any threads that are currently holding a relay in a state will exit"""

        self.interruptor.set()

        # putting a small pause in here to make sure any threads that may be still running get a chance to see
        # the interruptor event being set. This is easier than maintaining a list and verifying they have all
        # seen the event.
        time.sleep(0.1)
        for channel in self.relays:
            channel.set_state(Relay.OPEN)
        self.interruptor.clear()
    
    def close_channel(self, channel, duration):
        self.relays[channel-1].close(duration)
    
    def close_all(self, duration):
        self.interruptor.set()
        time.sleep(0.1)
        self.interruptor.clear()

        time.sleep(0.1)
        for i in range(len(self.relays)):
            self.close_channel(i+1, duration)

    

