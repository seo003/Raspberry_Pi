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
            if not car_stopped:
                await asyncio.sleep(10)
                car_stopped = True
                for sensor_number in active_sensors:
                    await telegram_alarm.handle_car_stop(application, sensor_number)
                await asyncio.sleep(15)  # 3분 대기
            
            if motion_detector.detect_motion() and temp_checker.check_temperature():
                for sensor_number in active_sensors:
                    await telegram_alarm.send_detection_alert(application, sensor_number)
            
            await asyncio.sleep(5)

    async def handle_new_user(update: telegram_alarm.Update, context):
        new_sensor_number = await telegram_alarm.start(update, context)
        if new_sensor_number:
            active_sensors.add(new_sensor_number)

    application.add_handler(telegram_alarm.CommandHandler("start", handle_new_user))
    asyncio.create_task(periodic_check())
    await application.run_polling(allowed_updates=telegram_alarm.Update.ALL_TYPES)

if __name__ == '__main__':
    nest_asyncio.apply()
    asyncio.run(main())
