"""
  This code is adapted from Camillo Addis's code on 
  https://medium.com/@camilloaddis/smart-air-conditioner-with-raspberry-pi-an-odissey-2a5b438fe984
"""

import RPi.GPIO as GPIO
from datetime import datetime

PIN = 16

SHORT, MEDIUM, LONG, LONGEST = 600, 1500, 24000, 30000

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN, GPIO.IN)

while True:
  val = 1
  while val:
    val = GPIO.input(PIN)
  
  start = datetime.now()
  ones = 0
  prev = 0
  command = []

  while True:
    if val != prev:
      now = datetime.now()
      pulse = now - start
      start = now
      command.append((prev, pulse.microseconds))

    if ones > LONGEST:
      break

    if val: ones += 1
    else: ones = 0

    prev = val
    val = GPIO.input(PIN)

  print("----------------START----------------")

  binary = ""
  for i in range(len(command) - 1):
    if command[i][0] == 0:
      on, off = command[i][1], command[i+1][1]
      if on < SHORT:
        if off < SHORT:
          binary += "0"
        elif off < MEDIUM:
          binary += "1"
        elif off < LONG:
          print(binary)
          binary = ""
          print("A")
        else:
          print(binary)
          binary = ""
          print("B")
      elif on > LONG and off > LONG:
        print(binary)
        binary = ""
        print("C")

  print(binary)
  print("-----------------END-----------------")