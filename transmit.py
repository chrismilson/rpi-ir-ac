import RPi.GPIO as GPIO
from time import sleep
from command import Command

PIN = 15
FREQ = 38000

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN, GPIO.OUT)

ir = GPIO.PWM(PIN, FREQ)

MICRO = 1000000
SHORT, LONG = 400, 1200

def txBit(bit):
  ir.start(33)
  sleep(SHORT / MICRO)
  ir.start(0)
  sleep((SHORT * bit + LONG * (bit ^ 1)) / MICRO)

def sendCommand(command):
  ir.start(50)
  sleep(30000 / MICRO)
  ir.start(0)
  sleep(16000 / MICRO)
  for bit in command: txBit(bit)
  ir.start(50)
  sleep(1600 / MICRO)
  ir.start(0)

sendCommand(Command.commandFromDetails("on", "heat", 26, "auto"))

GPIO.cleanup()