import asyncio
from telegram import Update
from telegram.ext import Application
import nest_asyncio

# 텔레그램 봇 설정
TOKEN = ''
CHAT_ID = ''

# 감지 상태를 저장하는 변수
temperature_detected = False
human_detected = False


async def send_alert(application, message):
    await application.bot.send_message(chat_id=CHAT_ID, text=message)

# 알람 신호를 확인하고 알림을 보내는 함수
async def check_and_send_alert(application):
    global temperature_detected, human_detected
    if temperature_detected and human_detected:
        message = "경고: 차량 내부에 위험 상황이 감지되었습니다! 온도가 높고 사람이 감지되었습니다."
        await send_alert(application, message)
        # 알림을 보낸 후 상태 초기화
        temperature_detected = False
        human_detected = False

# 감지 신호를 설정하는 함수 (다른 팀원의 코드에서 호출되어야 함 .)
def set_detection_signal(detection_type, value):
    global temperature_detected, human_detected
    if detection_type == "temperature":
        temperature_detected = value
    elif detection_type == "human":
        human_detected = value

# 주기적으로 알람을 체크하는 함수
async def periodic_alarm_check(application):
    while True:
        await check_and_send_alert(application)
        await asyncio.sleep(5)  # 5초마다 확인

# 메인 함수
async def main():
    application = Application.builder().token(TOKEN).build()
    
    # 시작 메시지 전송 (항시 켜놓을거여서 별로 의미없을수도)
    await send_alert(application, "차량 모니터링 시스템이 시작되었습니다.")

    

    # 주기적 알람 체크 태스크 시작
    asyncio.create_task(periodic_alarm_check(application))

    # 애플리케이션 실행
    await application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    # 비동기 메인 함수 실행
    nest_asyncio.apply()
    asyncio.run(main())