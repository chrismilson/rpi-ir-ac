import RPi.GPIO as GPIO
from time import sleep

PIN = 15 # GPIO 22
SHORT, LONG = 400, 1300
SHORT /= 1000000
LONG /= 1000000

GPIO.setmode(GPIO.BOARD)

GPIO.setup(PIN, GPIO.OUT)

def txBit(bit):
  GPIO.output(PIN, GPIO.HIGH)
  sleep(SHORT)
  GPIO.output(PIN, GPIO.LOW)
  sleep(SHORT * bit + LONG * (bit ^ 1))

data = [
  0xFF,
  0xFF,
  0,
  0,
  0xFF,
  0xFF,
  0,
  0,
  0xFF,
  0xFF
]

GPIO.output(PIN, GPIO.HIGH)
sleep(.03)
GPIO.output(PIN, GPIO.LOW)
sleep(.05)
GPIO.output(PIN, GPIO.HIGH)
sleep(.03)
GPIO.output(PIN, GPIO.LOW)
sleep(.02)

for val in data:
  for i in range(7, 1, -1):
    txBit((val >> i) & 1)

GPIO.cleanup()
