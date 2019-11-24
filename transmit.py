import RPi.GPIO as GPIO
from time import sleep

PIN = 15 # GPIO 22
SHORT, LONG = 400, 1300

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN, GPIO.OUT)

def txBit(bit):
  GPIO.output(PIN, GPIO.HIGH)
  if bit:
    sleep(SHORT / 1000)
  else:
    sleep(LONG / 1000)
  GPIO.output(PIN, GPIO.LOW)
  sleep(SHORT / 1000)

data = [
  0xFF,
  0x00,
  0xFF,
  0x00
]

for i in range(len(data)):
  byte = data[i]
  for j in range(8):
    txBit((byte >> j) & 1)