#!/usr/bin/env python3
import time
from datetime import datetime

import RPi.GPIO as GPIO

from threads.display_thread import DisplayThread

GPIO_PIN_MOTION_DATA = 18

GPIO.setmode(GPIO.BOARD)
GPIO.setup(GPIO_PIN_MOTION_DATA, GPIO.IN)

print("Started app (CTRL-C to exit)")
print("Calibrating PIR")

while GPIO.input(GPIO_PIN_MOTION_DATA) != 0:
    time.sleep(0.1)
print("Ready...")


def motion(pir_gpio):
    print("%s - Movement detected!" % datetime.now())
    thread_display = DisplayThread()
    thread_display.join()
    print("%s - Waiting for next movement" % datetime.now())


print("%s - Waiting for movement" % datetime.now())

try:
    # Triggering on rising flank
    GPIO.add_event_detect(GPIO_PIN_MOTION_DATA, GPIO.RISING, callback=motion)
    # sleep until callback is triggered
    while True:
        time.sleep(60)

except KeyboardInterrupt:
    print("Shutdown...")
    GPIO.cleanup()
