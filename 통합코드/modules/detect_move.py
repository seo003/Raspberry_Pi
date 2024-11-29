import asyncio
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
is_move = False

MOTION_THRESHOLD = 12  # 움직임 감지 기준 (10g 이상의 가속도)
STOP_DURATION = 5  # 정지 상태 감지 시간 (3분)
MOTION_DURATION = 5  # 움직임 감지 지속 시간 (5초)


async def monitor_motion_and_stop():
    """
    움직임과 정지 상태를 하나의 함수에서 감지합니다.
    움직임이 5초 이상 지속되면 True 출력,
    정지 상태가 3분 이상 지속되면 False 출력.
    """
    global motion_detected, motion_start_time, stop_start_time, is_move

    while True:
        # 가속도 값 읽기
        x, y, z = sensor.acceleration
        total_acceleration = (x**2 + y**2 + z**2) ** 0.5

        # 움직임 감지
        if total_acceleration > MOTION_THRESHOLD:
            if not motion_detected:
                motion_start_time = time.time()  # 움직임 시작 시간 기록
            motion_detected = True
            stop_start_time = None  # 정지 상태 초기화

            # 움직임이 5초 이상 지속되었는지 확인
            if motion_start_time and time.time() - motion_start_time >= MOTION_DURATION:
                print("움직임 감지: 5초 이상 지속")
                motion_start_time = None  # 상태 초기화
                is_move=False
        else:
            # 움직임이 없는 상태
            motion_detected = False
            motion_start_time = None  # 움직임 초기화

            # 정지 상태 시작 시간 기록
            if stop_start_time is None:
                stop_start_time = time.time()
            elif time.time() - stop_start_time >= STOP_DURATION:
                print("정지 상태: 3분 이상 지속")
                stop_start_time = None  # 상태 초기화
                is_move = True
        
        print(is_move)
        await asyncio.sleep(1)  # 1초 간격으로 반복
        
        if is_move:
            return is_move

async def main():
    """
    움직임과 정지 상태 감지 루프 실행.
    """
    await monitor_motion_and_stop()


# 비동기 루프 실행
#asyncio.run(main())
