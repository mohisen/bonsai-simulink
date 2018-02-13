#!/bin/env python3

"""This class provides data synchronization for multiple threads.
"""

import logging
import threading

class DataSync:
    def __init__(self, name):
        self.cv = threading.Condition()
        self.name = name
        self.reset()
        
    def reset(self):
        self.value = None
        self.stopping = False
        
    def wait(self):
        with self.cv:
            # Wait until there is a value
            while not self.value and not self.stopping:
                logging.debug("waiting for %s" % (self.name,))
                self.cv.wait()

            # Take the value, leave a None
            value = self.value
            self.value = None
            logging.debug("returning %s %s" % (self.name, str(value)))
            return value

    def post(self, value):
        with self.cv:
            assert self.value is None
            logging.debug("posting %s %s" % (self.name, str(value)))
            self.value = value
            self.cv.notify()

    def stop(self):
        with self.cv:
            assert self.value is None
            logging.debug("stopping %s" % (self.name))
            self.stopping = True
            self.cv.notify()
        
