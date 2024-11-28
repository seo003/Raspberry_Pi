import tos
import time

AM_OSCILLOSCOPE = 0x93

# 포트 설정
SERIAL_PORT = "/dev/ttyUSB1"
BAUD_RATE = 115200

class TemperatureMsg(tos.Packet):
    def __init__(self, packet=None):
        tos.Packet.__init__(self,
                            [('srcID',  'int', 2),
                             ('seqNo', 'int', 4),
                             ('type', 'int', 2),
                             ('Data0', 'int', 2),
                             ],
                            packet)

# 포트와 속도를 설정하는 Serial 객체 생성
serial = tos.Serial(SERIAL_PORT, BAUD_RATE)
am = tos.AM(serial)

def isOver30Degree(data):
    """
        온도 값이 30도 이상인지 확인하는 함수
    """
    # 온도 계산식
    temp = -(39.6) + (data * 0.01)
    print(f"온도: {temp:.2f}")

    # 30도 이상이면 True, 아니면 False 
    return temp >= 30

class TemperatureChecker:
    def __init__(self, serial=serial, baud_rate=BAUD_RATE):
        self.serial = tos.Serial(SERIAL_PORT, BAUD_RATE)
        self.am = tos.AM(self.serial)
        print("온도 측정기가 초기화되었습니다.")

    async def check_temperature(self):
        """
            온도를 주기적으로 체크하고, 30도 이상일 때 True 반환
        """
        p = self.am.read()
        msg = TemperatureMsg(p.data)

        if msg.type == 2:  # 온도 데이터가 맞는지 확인
            # 온도 계산(30도 이상이면 True, 아니면 False)
            return isOver30Degree(msg.Data0)
        else:
            print("온도 데이터가 아닙니다.")
            return False

# main에서 비동기 함수 호출하기
if __name__ == "__main__":
    import asyncio

    async def run():
        
        temp = TemperatureChecker()
        while(True):
            result = await temp.check_temperature()
            if result == True:
                break
            else:
                print("30도 이하입니다.")
        print(f"30도 이상인가? {result}")

    asyncio.run(run())  # 비동기 함수 실행
