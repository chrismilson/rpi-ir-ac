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
        arr.append(short)
      else:
        arr.append(long)
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
