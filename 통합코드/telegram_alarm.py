import asyncio
import sqlite3
from telegram import Update
from telegram.ext import Application, CommandHandler
from dotenv import load_dotenv
import os

# 환경 변수에서 토큰 로드
load_dotenv()
TOKEN = os.getenv('TOKEN')

# 데이터베이스 연결
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# 사용자 테이블 생성 (없는 경우)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        sensor_number INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER UNIQUE
    )
''')
conn.commit()

async def send_alert(application, chat_id, message):
    # 텔레그램으로 알림 메시지 전송
    await application.bot.send_message(chat_id=chat_id, text=message)

async def start(update: Update, context):
    chat_id = update.effective_user.id
    print(f"/start 명령어를 {chat_id}에서 받았습니다.")
    
    cursor.execute('SELECT sensor_number FROM users WHERE chat_id = ?', (chat_id,))
    result = cursor.fetchone()
    
    if result:
        print(f"기존 사용자 발견. 센서 번호: {result[0]}")
        await update.message.reply_text(f"이미 등록된 사용자입니다. 귀하의 센서 번호는 {result[0]}입니다.")
        return result[0]
    
    cursor.execute('SELECT MAX(sensor_number) FROM users')
    max_sensor_number = cursor.fetchone()[0]
    new_sensor_number = 1 if max_sensor_number is None else max_sensor_number + 1
    
    print(f"새로운 센서 번호 할당: {new_sensor_number}")
    
    cursor.execute('INSERT INTO users (chat_id, sensor_number) VALUES (?, ?)', (chat_id, new_sensor_number))
    conn.commit()
    
    message = f"센서 번호 {new_sensor_number}가 활성화되었습니다. 차량이 정차한 후 3분 뒤 센서가 가동됩니다."
    await send_alert(context.application, chat_id, message)
    
    return new_sensor_number

async def handle_car_stop(application, sensor_number):
    print(f"센서 번호 {sensor_number}에 대해 차량 정차가 감지되었습니다.")
    
    cursor.execute('SELECT chat_id FROM users WHERE sensor_number = ?', (sensor_number,))
    user = cursor.fetchone()
    
    if user:
        message = "차량이 정차했습니다. 센서가 가동됩니다."
        await send_alert(application, user[0], message)

async def send_detection_alert(application, sensor_number):
    print(f"센서 번호 {sensor_number}에 대한 감지 알림이 발생했습니다.")
    
    cursor.execute('SELECT chat_id FROM users WHERE sensor_number = ?', (sensor_number,))
    user = cursor.fetchone()
    
    if user:
        await send_alert(application, user[0], "차량 내 고온 및 인체감지가 되었습니다. 신속한 대처 부탁드립니다.")

def create_telegram_app():
    # 텔레그램 봇 애플리케이션 생성
    return Application.builder().token(TOKEN).build()
