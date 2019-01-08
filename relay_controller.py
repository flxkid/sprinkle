#!/usr/bin/env python2.7

# wiringpi uses a lil different pin numbering scheme. It's not physical pin or GPIO, it's their
# own setup. You can see the reference to it here: https://projects.drogon.net/raspberry-pi/wiringpi/pins/
import wiringpi
import time
import threading
import datetime

class relay():
    CLOSED = 1
    OPEN = 0
    UNKNOWN = -1

    GPIO_Pin = 0
    latching = False
    ordinal_pos = 0
    name = ''
    interruptor = None

    def __init__(self, pin, position=0, latching=False, state=-1, name='', interruptor=None):
        self.GPIO_Pin = pin
        self.ordinal_pos = position
        self.name = name
        self.interruptor = interruptor
        wiringpi.pinMode(self.GPIO_Pin, 1) # set the pin to output mode
        
        # If no initial state is passed, then don't assume any state is correct, leave
        # it as-is.
        if (state <> self.UNKNOWN):
            self.set_state(state)

    def get_state(self):
        return wiringpi.digitalRead(self.GPIO_Pin)

    def set_state(self, relay_state):
        wiringpi.digitalWrite(self.GPIO_Pin, relay_state)
    
    def _close(self, duration):
        self.set_state(self.CLOSED)
        started_at = datetime.now()
        while not self.interruptor.is_set():
            time.sleep(0) # pass control to other threads
            if (datetime.now() - started_at).total_seconds() > duration:
                break

        self.set_state(self.OPEN)

    def close(self, duration=10):
        t = threading.Thread(target=self._close, args=(duration))
        t.start()
       
class relay_controller:
    channels = 0
    relays = []

    # The "interruptor" is used to stop relay channels that have a threaded function
    # sleeping, waiting to "open" or shut off a relay for a duration. If that duration
    # needs to be interrupted, then the interruptor can be "Set". This will interrupt
    # ALL currently sleeping relays!
    interruptor = threading.Event()

    def __init__(self, relays=[]):
        wiringpi.wiringPiSetup()
        if isinstance(relays, list):
            for idx, channel in enumerate(relays, start=1):
                # if there isn't a position in the dictionary, set it based on where in the 
                # array it is so that each channel is numbered ordinally.
                if not "position" in channel:
                    channel["position"] = idx
                channel["interruptor"] = self.interruptor
                self.relays.append(relay(**channel))
        else:
            raise KeyError("Pass a list of format: [{'name': 'front', 'pin': 1, 'latching': False, 'position': 1, 'state': relay.UNKNOWN}]")
        
        self.channels = len(relays)

    def open_all(self):
        self.interruptor.set()

        # putting a small pause in here to make sure any threads that may be still running get a chance to see
        # the interruptor event being set. This is easier than maintaining a list and verifying they have all
        # seen the event.
        time.sleep(0.1)
        for channel in self.relays:
            channel.set_state(relay.OPEN)
        self.interruptor.clear()
    
    def close_channel(self, channel, duration):
        self.relays[channel-1].close(duration)

    

