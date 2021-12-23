#!/usr/bin/python3

import RPi.GPIO as GPIO
import time

led = 23

GPIO.setmode(GPIO.BOARD)
GPIO.setup(led, GPIO.OUT)

for i in range(10):
    GPIO.output(led, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(led, GPIO.LOW)
    time.sleep(1)

GPIO.cleanup()