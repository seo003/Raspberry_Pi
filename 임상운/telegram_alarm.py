import asyncio
import sqlite3
from telegram import Update
from telegram.ext import Application, CommandHandler
import nest_asyncio

# 텔레그램 봇 설정
TOKEN = ''  # 봇 토큰 나중에 입력해야됌.

# 데이터베이스 연결
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# 테이블 생성
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        sensor_number INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER UNIQUE
    )
''')
conn.commit()

# 감지 상태를 저장하는 변수
temperature_detected = False
human_detected = False
car_stopped = False

async def send_alert(application, chat_id, message):
    await application.bot.send_message(chat_id=chat_id, text=message)

# /start 명령어 처리 (영문으로 변경)
async def start(update: Update, context):
    chat_id = update.effective_user.id

    # 이미 등록된 사용자 확인
    cursor.execute('SELECT sensor_number FROM users WHERE chat_id = ?', (chat_id,))
    result = cursor.fetchone()

    if result:
        await update.message.reply_text("이미 등록된 사용자입니다.")
        return

    # 새로운 사용자 등록
    cursor.execute('INSERT INTO users (chat_id) VALUES (?)', (chat_id,))
    conn.commit()

    # 센서 번호 가져오기
    cursor.execute('SELECT sensor_number FROM users WHERE chat_id = ?', (chat_id,))
    sensor_number = cursor.fetchone()[0]

    message = f"센서 번호 {sensor_number}가 활성화되었습니다. 차량이 정차한 후 3분 뒤 센서가 가동됩니다."
    await send_alert(context.application, chat_id, message)

# 차량 정차 신호 처리
async def handle_car_stop(application, sensor_number):
    global car_stopped
    car_stopped = True  # 차량이 정차했음을 기록

    # 해당 센서와 연결된 사용자에게 알림 전송
    cursor.execute('SELECT chat_id FROM users WHERE sensor_number = ?', (sensor_number,))
    user = cursor.fetchone()
    if user:
        message = "차량이 정차했습니다. 센서가 가동됩니다."
        await send_alert(application, user[0], message)

# 알람 신호를 확인하고 알림을 보내는 함수
async def check_and_send_alert(application, sensor_number):
    global temperature_detected, human_detected, car_stopped

    if car_stopped:
        # 차량이 정차했을 때만 온도 및 인체 감지 알림 전송 가능
        if temperature_detected or human_detected:
            cursor.execute('SELECT chat_id FROM users WHERE sensor_number = ?', (sensor_number,))
            user = cursor.fetchone()
            if user:
                await send_alert(application, user[0], "차량 내 고온 및 인체감지가 되었습니다. 신속한 대처 부탁드립니다.")
        
        # 상태 초기화
        temperature_detected = False  # 상태 초기화
        human_detected = False  # 상태 초기화

# 감지 신호를 설정하는 함수 (다른 팀원의 코드에서 호출되어야 함.)
def set_detection_signal(application, detection_type, value):
    global temperature_detected, human_detected

    if detection_type == "temperature":
        if car_stopped:  # 차량이 정차했을 때만 온도 신호 설정 가능
            temperature_detected = value
    
    elif detection_type == "human":
        if car_stopped:  # 차량이 정차했을 때만 인체 신호 설정 가능
            human_detected = value

# 주기적으로 알람을 체크하는 함수
async def periodic_alarm_check(application, sensor_number):
    while True:
        await check_and_send_alert(application, sensor_number)
        await asyncio.sleep(5)  # 5초마다 확인

# 메인 함수
async def main():
    application = Application.builder().token(TOKEN).build()
    
    # 명령어 핸들러 등록 (영문으로 변경)
    application.add_handler(CommandHandler("start", start))
    
    # 주기적 알람 체크 태스크 시작 (예시로 센서 번호 1 사용)
    asyncio.create_task(periodic_alarm_check(application, 1))

    # 애플리케이션 실행
    await application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    # 비동기 메인 함수 실행
    nest_asyncio.apply()
    asyncio.run(main())