import serial
import time

class MotionDetector:
    def __init__(self, port='/dev/ttyACM0', baudrate=9600, timeout=1):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        time.sleep(2)
        self.motion_count = 0

    def detect_motion(self):
        if self.ser.in_waiting > 0:
            sensor_val = self.ser.readline().decode('utf-8').strip()
            if sensor_val == "1":
                self.motion_count += 1
                if self.motion_count >= 3:
                    self.motion_count = 0
                    return True
            else:
                self.motion_count = 0
        return False

    def close(self):
        self.ser.close()