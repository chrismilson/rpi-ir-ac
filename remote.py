from textwrap import wrap

class Remote:
  SHORT, LONG = "400", "1200"
  def __init__(self, name):
    self.name = name
    self.commands = []

  def add(self, command):
    self.commands.append(command)
    return self

  def getConf(self):
    s =  "begin remote\n"
    s += "  name  {}\n".format(self.name)
    s += "  flags RAW_CODES\n"
    s += "  eps   30\n"
    s += "  aeps  100\n"
    s += "  begin raw_codes\n"
    for command in self.commands:
      s += "    name {}\n".format(command.name)
      s += "\n".join(wrap(
        " ".join(command.pulseSpace(self.SHORT, self.LONG)),
        80,
        initial_indent="      ",
        subsequent_indent="      "
      )) + " {}\n".format(self.LONG)
    s += "  end raw_codes\n"
    s += "end remote\n"

    return s