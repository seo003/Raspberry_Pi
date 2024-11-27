import tos

class TemperatureMsg(tos.Packet):
    def __init__(self, packet=None):
        tos.Packet.__init__(self,
                            [('srcID',  'int', 2),
                             ('seqNo', 'int', 4),
                             ('type', 'int', 2),
                             ('Data0', 'int', 2),
                             ],
                            packet)

class TemperatureChecker:
    def __init__(self, port="/dev/ttyUSB0", baud_rate=115200):
        self.serial = tos.Serial(port, baud_rate)
        self.am = tos.AM(self.serial)

    def check_temperature(self):
        p = self.am.read()
        msg = TemperatureMsg(p.data)
        if msg.type == 2: 
            temp = -(39.6) + (msg.Data0 * 0.01)
            print(f"온도:{temp}")
            return temp >= 30
        return False
