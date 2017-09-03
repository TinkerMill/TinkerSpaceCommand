#!/bin/python

# A simple script for phutting a Raspberry Pi down when a button is pushed.
#
# 

import RPi.GPIO as GPIO
import time
import os

GPIO_SHUTDOWN = 18

# How long to wait after the off button has been pushed to decide
# the person means it. In seconds.
WAIT_TIME = 5

# Use the Broadcom SOC Pin numbers
# Setup the Pin with Internal pullups enabled and PIN in reading mode.
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_SHUTDOWN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

running = 1
while running:
 # Wait for the button to be pressec.
 GPIO.wait_for_edge(GPIO_SHUTDOWN, GPIO.FALLING, bouncetime = 50)

 print("Button pressed")
 startInterval = time.time()

 # Wait for the button to be released.
 GPIO.wait_for_edge(GPIO_SHUTDOWN, GPIO.RISING, bouncetime = 50)

 interval = time.time() - startInterval

 print("Button released at {}".format(interval))
 if interval > WAIT_TIME:
   running = 0

os.system("sudo shutdown -h now")

