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

    def detect_motion(self):
        """
        모션 감지 상태를 반환
        :return: 감지되면 True, 감지되지 않으면 False
        """
        if self.ser.in_waiting > 0:  # 시리얼 데이터가 있을 경우
            sensor_val = self.ser.readline().decode('utf-8').strip()
            return sensor_val == "1"  # "1"은 모션 감지를 나타냄
        return False  # 데이터가 없거나 감지되지 않은 경우

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
