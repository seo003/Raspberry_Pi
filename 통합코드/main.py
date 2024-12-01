import asyncio
import nest_asyncio
from modules.motion import MotionDetector
from modules.temperature_check import TemperatureChecker
import modules.detect_move as detect_move
import modules.telegram_alarm as telegram_alarm

async def main():
    application = telegram_alarm.create_telegram_app()

    motion_detector = MotionDetector()
    temp_checker = TemperatureChecker()

    car_stopped = {}
    active_sensors = set()

    async def periodic_check(sensor_number):
        nonlocal car_stopped
        car_stopped[sensor_number] = False
        while True:
            print(f"[센서 {sensor_number}] 주기적 점검을 수행합니다.")
            
            if not car_stopped[sensor_number]:
                await asyncio.sleep(20)  # 차량 정차 시뮬레이션 대기 시간
                
                car_stopped[sensor_number] = await detect_move.monitor_motion_and_stop()
                print(f"[센서 {sensor_number}] 차량 정차 상태로 변경. 알림 전송 중...")
                await telegram_alarm.handle_car_stop(application, sensor_number)
                
                print(f"[센서 {sensor_number}] 3분 대기 중...")
                await asyncio.sleep(20)  # 대기 시간
                
            print(f"[센서 {sensor_number}] 모션 및 온도 체크 중...")
            
            while True:
                print(f"[센서 {sensor_number}] 온도를 감지 중...")
                # 고온 감지
                if await temp_checker.check_temperature():
                    while True:
                        print(f"[센서 {sensor_number}] 모션 센서를 감지 중...")
                        # 모션 센서 감지(총 3번 감지 되면 true)
                        if motion_detector.detect_motion():
                            print(f"[센서 {sensor_number}] 고온 감지 및 모션 감지가 발생했습니다. 알림 전송 중...")
                            await telegram_alarm.send_detection_alert(application, sensor_number)
                            break
                            
                        await asyncio.sleep(5)  # 다음 점검까지 

    async def handle_new_user(update: telegram_alarm.Update, context):
        print("새 사용자 등록 시도 중...")
        
        new_sensor_number = await telegram_alarm.start(update, context)
        
        if new_sensor_number:
            active_sensors.add(new_sensor_number)
            print(f"센서 번호 {new_sensor_number}가 활성 센서 목록에 추가되었습니다.")
            # 새 사용자 등록 후 periodic_check 시작
            asyncio.create_task(periodic_check(new_sensor_number))

    application.add_handler(telegram_alarm.CommandHandler("start", handle_new_user))
    await application.run_polling(allowed_updates=telegram_alarm.Update.ALL_TYPES)

if __name__ == '__main__':
    nest_asyncio.apply()
    asyncio.run(main())
