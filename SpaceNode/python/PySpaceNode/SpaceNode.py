#!/usr/bin/python3

# Incubator control software
#
# Written by Keith M. Hughes
#
# This code is for driving an incubator. It assumes a DHT22 temperature humidity
# sensor. It has a GUI control interface for setting temperatures and 
# seeing the current temperature.
#
# It makes use of Python threads.

# This code uses libraries:
#
# Adafruit DH22 
# ivpid

import sys

import Adafruit_DHT
import RPi.GPIO as GPIO

import threading
import time

import PID

import tkinter as tk

# The GPIO pin for the DHT 22 sensor signal output.
DHT_22_SIGNAL_PIN = 4

# The GPIO pin for controlling the relay that controls the heating element.
HEATING_ELEMENT_RELAY_SIGNAL_PIN = 6


class SensorThread (threading.Thread):
  def __init__(self, threadID, name):
    threading.Thread.__init__(self)
    self.threadID = threadID
    self.name = name
    self.controller = controller
    self.running = True

  def run(self):
    while self.running:
      self.controller.process()
      time.sleep(5)

  def stop(self):
    self.running = False

  def set_controller(self, controller):
    self.controller = controller

class Controller:
  def __init__(self, sensor, actuator):
    self.sensor = sensor
    self.actuator = actuator
    self.pid = PID.PID(0.8, 0, 0)
    self.setPointValue = None
    self.newTemperatureHandler = None
    self.newHumidityHandler = None

  def start(self):
    self.sensorThread = SensorThread(1, "Controller")
    self.sensorThread.set_controller(self)
    self.sensorThread.start()

  def stop(self):
    self.sensorThread.stop()

  def process(self):
    if self.setPointValue is not None:
      temperature, humidity = self.sensor.readSensor()
      if humidity is not None and temperature is not None:
        if self.newTemperatureHandler is not None:
          self.newTemperatureHandler(temperature)
        if self.newHumidityHandler is not None:
          self.newHumidityHandler(humidity)

        print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
        self.pid.update(temperature)
        output = self.pid.output
        print('PID output={0:0.1f}*'.format(output))
        actuatorOn = (output) > 0
        self.actuator.setState(actuatorOn)

  def setPoint(self, value):
    self.setPointValue = value
    self.pid.SetPoint = value
  
  def modifyTemperature(self, delta):
    newTemp = self.setPointValue + delta
    self.setPoint(newTemp)

    return newTemp

  def setNewTemperatureHandler(self, newTemperatureHandler):
    self.newTemperatureHandler = newTemperatureHandler

  def setNewHumidityHandler(self, newHumidityHandler):
    self.newHumidityHandler = newHumidityHandler
    

class TemperatureSensor:
  def __init__(self, pin):
    self.pin = pin
    self.sensor=Adafruit_DHT.DHT22

  def readSensor(self):
    humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)

    temperature = temperature * 9/5.0 + 32

    # Note that sometimes you won't get a reading and
    # the results will be null (because Linux can't
    # guarantee the timing of calls to read the sensor).
    # If this happens try again!
    return temperature, humidity

GPIO.setmode(GPIO.BCM)

class PowerRelay:
  def __init__(self, pin):
    self.pin = pin
    GPIO.setup(self.pin, GPIO.OUT)

  def setState(self, newState):
    if newState:
      self.powerOn()
    else:
      self.powerOff()

  def powerOn(self):
    GPIO.output(self.pin, 1)

  def powerOff(self):
    GPIO.output(self.pin, 0)

relay = PowerRelay(HEATING_ELEMENT_RELAY_SIGNAL_PIN)

sensor = TemperatureSensor(DHT_22_SIGNAL_PIN)
controller = Controller(sensor, relay)

relay.powerOn()
time.sleep(5)
relay.powerOff()

print(controller)
controller.setPoint(87)

class Application(tk.Frame):
  def __init__(self, controller, master=None):
    super().__init__(master)

    self.controller = controller

    self.pack()
    self.create_widgets()
    self.pack()

    self.controller.setNewTemperatureHandler(self.newTemperature)
    self.controller.setNewHumidityHandler(self.newHumidity)

  def create_widgets(self):
    tk.Label(self, text="Incubator").grid(row=0, column=1, sticky=tk.W)

    tk.Label(self, text="Set Point:").grid(row=1, column=1, sticky=tk.W)
    self.setPoint = tk.StringVar(self,"100 F")    
    tk.Label(self, textvariable=self.setPoint).grid(row=1, column=2, sticky=tk.W)

    tk.Label(self, text="Actual Temperature:").grid(row=2, column=1, sticky=tk.W)
    self.actualTemperature = tk.StringVar(self,"100 F")    
    tk.Label(self, textvariable=self.actualTemperature).grid(row=2, column=2, sticky=tk.W)

    tk.Label(self, text="Actual Humidity:").grid(row=3, column=1, sticky=tk.W)
    self.actualHumidity = tk.StringVar(self,"100%")    
    tk.Label(self, textvariable=self.actualHumidity).grid(row=3, column=2, sticky=tk.W)

    tk.Button(self, text='Up', command=self.temperatureUp).grid(row=10, column=1, sticky=tk.W, pady=4)
    tk.Button(self, text='Down', command=self.temperatureDown).grid(row=10, column=2, sticky=tk.W, pady=4)
    tk.Button(self, text='Quit', command=self.shutdown).grid(row=11, column=1, sticky=tk.W, pady=4)

  def startup(self):
    self.controller.start()
    self.mainloop()

  def shutdown(self):
    self.controller.stop()
    self.master.destroy()

  def temperatureUp(self):
    newTemp = self.controller.modifyTemperature(1)
    self.setPoint.set('{0:0.1f} *F'.format(newTemp))

  def temperatureDown(self):
    newTemp = self.controller.modifyTemperature(-1)
    self.setPoint.set('{0:0.1f} *F'.format(newTemp))

  def newTemperature(self, newTemp):
    self.actualTemperature.set('{0:0.1f} *F'.format(newTemp))

  def newHumidity(self, newHumidity):
    self.actualHumidity.set('{0:0.1f}%'.format(newHumidity))

ui_root = tk.Tk()
incubator_app = Application(controller=controller, master=ui_root)

incubator_app.startup()
