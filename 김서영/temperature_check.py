#!/usr/bin/env python
# Temperature check script
# Data Format
# THL Temperature Data0

import sys
import tos
import time

AM_OSCILLOSCOPE = 0x93

# 포트 설정
SERIAL_PORT = "/dev/ttyUSB0"
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

def start_temperature_check(data0):
    """
    온도 값이 30도 이상인지 확인하는 함수
    """
    # 온도 계산식
    temp = -(39.6) + (data0 * 0.01)

    # 30도 이상이면 True, 아니면 False 
    return temp >= 30

def run_temperature_check():
    """
    온도를 주기적으로 체크하고, 30도 이상일 때 True 반환
    """
    while True:
        p = am.read()
        msg = TemperatureMsg(p.data)

        if msg.type == 2: 
            # 온도 값만 추출
            temp = -(39.6) + (msg.Data0 * 0.01)

            # 결과 출력
            print(f"Temperature: {temp}°C")
            
            # 온도가 30도 이상인지 확인
            if start_temperature_check(msg.Data0):
                print("Result: True")
                return True
            else:
                print("Result: False")
                
if __name__ == "__main__":
    run_temperature_check()
