import serial
import time

class MotionDetector:
    def __init__(self, port='/dev/ttyACM0', baudrate=9600, timeout=1):
        """
        MotionDetector 초기화 함수
        :param port: Arduino가 연결된 시리얼 포트
        :param baudrate: 통신 속도
        :param timeout: 데이터 수신 대기 시간
        """
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        time.sleep(2)  # Arduino 초기화 대기
        self.motion_count = 0  # 연속 감지 카운터 초기화

    def detect_motion(self):
        """
        모션 감지 상태를 반환
        :return: 1이 3번 연속 감지되면 True, 그렇지 않으면 False
        """
        if self.ser.in_waiting > 0:  # 시리얼 데이터가 있을 경우
            sensor_val = self.ser.readline().decode('utf-8').strip()
            if sensor_val == "1":
                self.motion_count += 1  # 1 감지 시 카운터 증가
                if self.motion_count >= 3:  # 3번 연속 감지되었는지 확인
                    self.motion_count = 0  # 카운터 초기화
                    return True
            else:
                self.motion_count = 0  # 연속 감지가 끊기면 카운터 초기화
        return False

    def close(self):
        """시리얼 포트 닫기"""
        self.ser.close()

# 모듈 테스트용 코드
if __name__ == "__main__":
    motion_detector = MotionDetector()

    try:
        while True:
            if motion_detector.detect_motion():
                print("Motion Detected: True")
            else:
                print("Motion Detected: False")
            time.sleep(0.5)  # 0.5초마다 상태 확인

    except KeyboardInterrupt:
        print("Exiting program...")

    finally:
        motion_detector.close()
