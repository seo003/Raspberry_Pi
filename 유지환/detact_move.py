import time
import board
import adafruit_adxl34x

# I2C 연결 설정
i2c = board.I2C()
sensor = adafruit_adxl34x.ADXL345(i2c)

# 변수 설정
motion_detected = False
motion_start_time = None
stop_start_time = None

MOTION_THRESHOLD = 0.1  # 움직임 감지 기준 (예: 0.1g 이상의 가속도)
STOP_DURATION = 180  # 정지 상태 감지 시간 (3분)
MOTION_DURATION = 5  # 움직임 감지 지속 시간 (5초)


def is_motion_detected():
    """
    현재 센서 값을 기반으로 움직임이 감지되었는지 확인합니다.
    """
    x, y, z = sensor.acceleration
    total_acceleration = (x**2 + y**2 + z**2) ** 0.5
    return total_acceleration > MOTION_THRESHOLD


def check_motion_and_stop():
    """
    움직임과 정지 상태를 확인하고 결과를 반환합니다.
    """
    global motion_detected, motion_start_time, stop_start_time

    if is_motion_detected():
        if not motion_detected:
            # 움직임 시작 시각 기록
            motion_start_time = time.time()
        motion_detected = True
        stop_start_time = None  # 정지 상태 초기화
    else:
        if motion_detected and time.time() - motion_start_time >= MOTION_DURATION:
            # 움직임이 5초 이상 지속된 경우
            motion_detected = False
            return True  # 움직임 감지 완료

        if stop_start_time is None:
            stop_start_time = time.time()  # 정지 상태 시작 시각 기록
        elif time.time() - stop_start_time >= STOP_DURATION:
            # 정지 상태가 3분 이상 지속된 경우
            motion_detected = False
            return False  # 정지 상태 감지 완료

    return None  # 조건 충족 안 됨


# 메인 루프
while True:
    result = check_motion_and_stop()
    if result is not None:
        print("Result:", result)  # True: 움직임, False: 정지
        stop_start_time = None  # 결과 출력 후 상태 초기화

    time.sleep(1)  # 1초 간격으로 체크
