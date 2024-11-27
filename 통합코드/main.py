import asyncio
import nest_asyncio
from motion import MotionDetector
from temperature_check import TemperatureChecker
import telegram_alarm

async def main():
    application = telegram_alarm.create_telegram_app()

    motion_detector = MotionDetector()
    temp_checker = TemperatureChecker()

    car_stopped = False
    active_sensors = set()

    async def periodic_check():
        nonlocal car_stopped
        while True:
            print("주기적 점검을 수행합니다.")
            
            if not car_stopped:
                await asyncio.sleep(10)  # 차량 정차 시뮬레이션 대기 시간
                
                car_stopped = True
                
                print("차량 정차 상태로 변경. 알림 전송 중...")
                for sensor_number in active_sensors:
                    await telegram_alarm.handle_car_stop(application, sensor_number)
                
                print("3분 대기 중...")
                await asyncio.sleep(60)  # 대기 시간
                
            print("모션 및 온도 체크 중...")
            
            if motion_detector.detect_motion() and temp_checker.check_temperature():
                print("모션 또는 고온 감지가 발생했습니다. 알림 전송 중...")
                for sensor_number in active_sensors:
                    await telegram_alarm.send_detection_alert(application, sensor_number)
            
            await asyncio.sleep(5)  # 다음 점검까지 대기

    async def handle_new_user(update: telegram_alarm.Update, context):
        print("새 사용자 등록 시도 중...")
        
        new_sensor_number = await telegram_alarm.start(update, context)
        
        if new_sensor_number:
            active_sensors.add(new_sensor_number)
            print(f"새 센서 번호 {new_sensor_number}가 활성 센서 목록에 추가되었습니다.")

    application.add_handler(telegram_alarm.CommandHandler("start", handle_new_user))
    asyncio.create_task(periodic_check())
    await application.run_polling(allowed_updates=telegram_alarm.Update.ALL_TYPES)

if __name__ == '__main__':
    nest_asyncio.apply()
    asyncio.run(main())
