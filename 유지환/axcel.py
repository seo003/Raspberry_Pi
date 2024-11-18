#아직 테스트 안해서 되는지는 모름
import time
import board
import adafruit_adxl34x

# I2C 연결 설정
i2c = board.I2C()
sensor = adafruit_adxl34x.ADXL345(i2c)

# 변수를 설정
motion_detected = False
motion_start_time = None
stop_start_time = None
motion_threshold = 0.1  # 움직임 감지 기준 (예: 0.1g 이상의 가속도가 있으면 움직임으로 간주)
stop_duration = 180  # 정지 상태 감지 시간 (3분 = 180초)
motion_duration = 5  # 움직임 감지 지속 시간 (5초)

def check_motion():
    global motion_detected, motion_start_time, stop_start_time

    # 가속도 값 읽기
    x, y, z = sensor.acceleration
    total_acceleration = (x**2 + y**2 + z**2) ** 0.5

    # 움직임 감지
    if total_acceleration > motion_threshold:
        if motion_detected is False:
            motion_start_time = time.time()
        motion_detected = True
        stop_start_time = None
    else:
        if motion_detected:
            if time.time() - motion_start_time > motion_duration:
                return 1  # 5초 이상 움직였으면 1 출력
        motion_detected = False
        stop_start_time = stop_start_time or time.time()

    # 3분간 정지 상태 체크
    if stop_start_time and time.time() - stop_start_time > stop_duration:
        return 0  # 3분간 움직이지 않으면 0 출력

    return None

while True:
    result = check_motion()
    if result is not None:
        print(result)
        stop_start_time = None  # 결과가 출력되면 정지 상태 리셋

    time.sleep(1)
