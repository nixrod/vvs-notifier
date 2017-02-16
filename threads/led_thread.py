import threading
import time
from datetime import datetime

import RPi.GPIO as GPIO

import services.twitter_service

GPIO_PIN_LED_S1 = 7
GPIO_PIN_LED_S2 = 11
GPIO_PIN_LED_S3 = 12
GPIO_PIN_LED_S4 = 13
GPIO_PIN_LED_S5 = 15
GPIO_PIN_LED_S6 = 16


def display_interruptions(interruptions):
    print('%s - Interruptions in the last 2 hours: %s' % (datetime.now(), interruptions))

    is_interruption = False
    for i in interruptions:
        if interruptions[i]:
            is_interruption = True

    if is_interruption:
        if interruptions['s1']:
            GPIO.output(GPIO_PIN_LED_S1, GPIO.HIGH)
        if interruptions['s2']:
            GPIO.output(GPIO_PIN_LED_S2, GPIO.HIGH)
        if interruptions['s3']:
            GPIO.output(GPIO_PIN_LED_S3, GPIO.HIGH)
        if interruptions['s4']:
            GPIO.output(GPIO_PIN_LED_S4, GPIO.HIGH)
        if interruptions['s5']:
            GPIO.output(GPIO_PIN_LED_S5, GPIO.HIGH)
        if interruptions['s6']:
            GPIO.output(GPIO_PIN_LED_S6, GPIO.HIGH)
        time.sleep(18)
    else:
        play_animation(3)


def play_animation(count):
    light_on_time = 0.15
    for i in range(0, count):
        GPIO.output(GPIO_PIN_LED_S1, GPIO.HIGH)
        time.sleep(light_on_time)
        GPIO.output(GPIO_PIN_LED_S1, GPIO.LOW)

        GPIO.output(GPIO_PIN_LED_S2, GPIO.HIGH)
        time.sleep(light_on_time)
        GPIO.output(GPIO_PIN_LED_S2, GPIO.LOW)

        GPIO.output(GPIO_PIN_LED_S3, GPIO.HIGH)
        time.sleep(light_on_time)
        GPIO.output(GPIO_PIN_LED_S3, GPIO.LOW)

        GPIO.output(GPIO_PIN_LED_S4, GPIO.HIGH)
        time.sleep(light_on_time)
        GPIO.output(GPIO_PIN_LED_S4, GPIO.LOW)

        GPIO.output(GPIO_PIN_LED_S5, GPIO.HIGH)
        time.sleep(light_on_time)
        GPIO.output(GPIO_PIN_LED_S5, GPIO.LOW)

        GPIO.output(GPIO_PIN_LED_S6, GPIO.HIGH)
        time.sleep(light_on_time)
        GPIO.output(GPIO_PIN_LED_S6, GPIO.LOW)


def reset_led():
    GPIO.output(GPIO_PIN_LED_S1, GPIO.LOW)
    GPIO.output(GPIO_PIN_LED_S2, GPIO.LOW)
    GPIO.output(GPIO_PIN_LED_S3, GPIO.LOW)
    GPIO.output(GPIO_PIN_LED_S4, GPIO.LOW)
    GPIO.output(GPIO_PIN_LED_S5, GPIO.LOW)
    GPIO.output(GPIO_PIN_LED_S6, GPIO.LOW)


class LedThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        GPIO.setmode(GPIO.BOARD)

        # S1 - Orange Cable
        GPIO.setup(GPIO_PIN_LED_S1, GPIO.OUT)
        # S2 - Yellow Cable
        GPIO.setup(GPIO_PIN_LED_S2, GPIO.OUT)
        # S3 - Brown Cable
        GPIO.setup(GPIO_PIN_LED_S3, GPIO.OUT)
        # S4 - Grey Cable
        GPIO.setup(GPIO_PIN_LED_S4, GPIO.OUT)
        # S5 - Blue Cable
        GPIO.setup(GPIO_PIN_LED_S5, GPIO.OUT)
        # S6 - White Cable
        GPIO.setup(GPIO_PIN_LED_S6, GPIO.OUT)

        self.daemon = True
        self.start()

    def run(self):
        play_animation(1)
        interruptions = services.twitter_service.fetch_disruptions_for_sbahn_line()
        display_interruptions(interruptions)
        reset_led()
