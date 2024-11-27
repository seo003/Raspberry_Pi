import serial
import time

class MotionDetector:
    def __init__(self, port='/dev/ttyACM0', baudrate=9600, timeout=1):
        # 시리얼 포트 초기화
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        time.sleep(2)  # 아두이노 초기화를 위한 대기 시간
        self.motion_count = 0  # 연속 감지 횟수를 저장하는 변수
        print("모션 감지기가 초기화되었습니다.")

    def detect_motion(self):
        if self.ser.in_waiting > 0:  # 시리얼 포트에 데이터가 있는지 확인
            sensor_val = self.ser.readline().decode('utf-8').strip()
            print(f"모션 센서 값: {sensor_val}")
            if sensor_val == "1":  # 모션이 감지되면
                self.motion_count += 1
                print(f"모션 감지됨. 카운트: {self.motion_count}")
                if self.motion_count >= 3:  # 3번 연속 감지되면
                    self.motion_count = 0  # 카운터 초기화
                    print("모션이 확인되었습니다.")
                    return True
            else:
                self.motion_count = 0  # 모션이 감지되지 않으면 카운터 초기화
        return False

    def close(self):
        # 시리얼 포트 닫기
        self.ser.close()
