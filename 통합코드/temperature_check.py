#!/usr/bin/env python
import tos
import time

class TemperatureMsg(tos.Packet):
    def __init__(self, packet=None):
        # 온도 데이터 패킷 구조 정의
        tos.Packet.__init__(self,
                            [('srcID',  'int', 2),
                             ('seqNo', 'int', 4),
                             ('type', 'int', 2),
                             ('Data0', 'int', 2),
                             ],
                            packet)

class TemperatureChecker:
    def __init__(self, port="/dev/ttyUSB0", baud_rate=115200):
        # 시리얼 포트 초기화
        self.serial = tos.Serial(port, baud_rate)
        self.am = tos.AM(self.serial)
        print("온도 설정이 초기화되었습니다.")

    def check_temperature(self):
        print("온도를 체크합니다")
        
        # 패킷을 여러 번 시도하여 읽어봅니다
        for _ in range(5):
            p = self.am.read()  # 패킷 읽기
            if p is None or p.data is None:
                print("패킷 읽기 실패 또는 데이터 없음")
                time.sleep(1)  # 잠시 기다리고 재시도
                continue
            
            # CRC 체크
            if p.check_crc() is False:
                print(f"경고: 잘못된 CRC! (받은 CRC: {p.get_crc()}, 예상 CRC: {p.expected_crc()})")
                continue  # CRC 오류가 발생한 경우 패킷을 건너뜁니다.
            
            print("패킷 읽기 완료")
            
            msg = TemperatureMsg(p.data)
            print(f"수신된 타입: {msg.type}")
            if msg.type == 2:  # 온도 데이터 타입인 경우
                temp = -(39.6) + (msg.Data0 * 0.01)
                print(f"온도: {temp}°C")
                if temp >= 30:
                    print("고온이 감지되었습니다.")
                    return True
                else:
                    print("저온이 감지되었습니다.")
                    return False
            else:
                print(f"온도 데이터가 아닌 다른 데이터 타입입니다. 타입: {msg.type}")
                return False
        
        print("패킷을 여러 번 시도했지만 데이터를 읽지 못했습니다.")
        return False

if __name__ == '__main__':
    tem = TemperatureChecker()
    tem.check_temperature()
