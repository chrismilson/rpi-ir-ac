class Command:
  def __init__(self, bytes = [], *, name = "command", repeatWithInvert=True):
    self.name = name
    if repeatWithInvert:
      inverted = map(lambda x : ~x & 0xFF, bytes)
      self.bytes = [b for pair in zip(bytes, inverted) for b in pair]
    else:
      self.bytes = bytes

  def pulseSpace(self, short, long):
    arr = []
    for bit in self:
      arr.append(short)
      if bit:
        arr.append(long)
      else:
        arr.append(short)
    return arr

  def __add__(self, other):
    return Command(self.bytes + other.bytes, repeatWithInvert=False)

  def __iter__(self):
    self.bit = 7
    self.byteIdx = 0
    return self

  def __next__(self):
    if self.byteIdx < len(self.bytes):  
      bit = (self.bytes[self.byteIdx] >> self.bit) & 1
      if self.bit == 0:
        self.bit = 7
        self.byteIdx += 1
      else:
        self.bit -= 1
      return bit
    else:
      raise StopIteration

  @staticmethod
  def tempByte(val):
    i = 0
    byte = 0
    while i < 6:
      byte = (byte << 1) | ((val >> i) & 1)
      i += 1
    return byte

  @staticmethod
  def modeByte(mode):
    if mode == "heat":
      return 0x6
    elif mode == "cool":
      return 0xC
    return 0x00 # default to dry

  @staticmethod
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

  @staticmethod
  def commandFromDetails(power = "off", mode = "heat", temp = 24, fan = "auto"):
    bytes = [
      0x02, 0xFF, 0x33,
      0x49, 
      0xC8,
      Command.tempByte(temp),
      0x00, 0x00, 0x00, 0x00, 0x00,
      Command.modeByte(mode) << 4 | Command.fanByte(fan),
      0x8F if power == "on" else 0x87,
      0x00, 0x00, 0x01, 0xC0, 0x80, 0x11, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF
    ]
    c = Command([0x80, 0x08, 0x00], repeatWithInvert=False)
    c += Command(bytes)
    c.name = "{}{}{}{}".format(power, temp, mode, fan)
    return c
