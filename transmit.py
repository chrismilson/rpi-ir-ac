import pigpio
from time import sleep
from command import Command

MICRO = 1000000
SHORT, LONG = 400 / MICRO, 1200 / MICRO
PIN = 22
FREQ = 38000

pi = pigpio.pi()
pi.set_mode(PIN, pigpio.OUTPUT)

pi.set_PWM_frequency(PIN, FREQ)

def txBit(bit):
  pi.set_PWM_dutycycle(PIN, 100)
  sleep(SHORT)
  pi.set_PWM_dutycycle(PIN, 0)
  sleep(SHORT * bit + LONG * (bit ^ 1))

def sendCommand(command):
  pi.set_PWM_dutycycle(PIN, 100)
  sleep(30000 / MICRO)
  pi.set_PWM_dutycycle(PIN, 0)
  sleep(16000 / MICRO)
  for bit in command: txBit(bit)
  pi.set_PWM_dutycycle(PIN, 100)
  sleep(1600 / MICRO)
  pi.set_PWM_dutycycle(PIN, 0)

# sendCommand(Command.commandFromDetails("on", "heat", 26, "auto"))
sendCommand(Command([0x00] * 10))