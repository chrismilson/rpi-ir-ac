from command import Command
from remote import Remote

def tempByte(val):
  i = 0
  byte = 0
  while i < 6:
    byte = (byte << 1) | ((val >> i) & 1)
    i += 1
  return byte

def modeByte(mode):
  if mode == "heat":
    return 0x6
  elif mode == "cool":
    return 0xC
  return 0x00 # default to dry

def fanByte(fan):
  if fan == 1:
    return 0x8
  elif fan == 2:
    return 0x4
  elif fan == 3:
    return 0xC
  elif fan == 4:
    return 0x2
  elif fan == 5:
    return 0x6
  return 0xA # default to auto

def commandFromDetails(*,
  power = "on",
  temperature = 24,
  mode = "heat",
  fan = "auto"):
  bytes = [
    0x02, 0xFF, 0x33,
    0x00, # Check byte?
    0x00, # Check byte?
    tempByte(temperature),
    0x00, 0x00, 0x00, 0x00, 0x00,
    modeByte(mode) << 4 | fanByte(fan),
    0x8F if power == "on" else 0x87,
    0x00, 0x00, 0x01, 0xC0, 0x80, 0x11, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF
  ]
  c = Command([0x80, 0x08, 0x00], repeatWithInvert=False)
  c += Command(bytes)
  c.name = "{}{}{}{}".format(power, temperature, mode, fan)
  return c

c = commandFromDetails(
  power = "on",
  temperature = 27,
  mode = "heat",
  fan = "auto"
)

# print(" ".join(["1" if b else "0" for b in c]))
# print(Remote("aircon").add(c).getConf())

SHORT, LONG = "400", "1200"
for bit in c:
  print(f"pulse {SHORT}")
  if bit: print(f"space {LONG}")
  else: print(f"space {SHORT}")
print(f"pulse {SHORT}")