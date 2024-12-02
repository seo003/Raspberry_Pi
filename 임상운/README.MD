# Telegram 알림 모듈 (`telegram_alarm.py`)

## **설명**
1. 텔레그램을 통한 사용자 등록 및 센서 번호 할당.
2. 특정 조건(차량 정차, 고온, 모션 감지 등) 발생 시 실시간 알림 전송.
3. 사용자 및 센서 정보를 SQLite 데이터베이스를 통해 관리.

---
## PIP LIST

- `pip install python-telegram-bot` 
- `pip install nest-asyncio` 
- `pip install pyserial` 


----

## **기능**
1. **사용자 등록**:
   - 텔레그램 `/start` 명령어를 통해 사용자가 등록됩니다.
   - 고유한 센서 번호가 자동으로 할당되며, 기존 사용자라면 데이터베이스에서 해당 센서 번호를 조회합니다.

2. **알림 전송**:
   - 차량 정차, 고온, 모션 감지 시 텔레그램 메시지를 통해 실시간으로 사용자에게 알림을 보냅니다.

3. **데이터베이스 관리**:
   - `SQLite`를 이용하여 사용자와 센서 번호를 관리합니다.
   - 중복 등록을 방지하고 안정적인 데이터 관리를 제공합니다.

4. **모듈화된 텔레그램 애플리케이션**:
   - `python-telegram-bot` 라이브러리를 활용하여 텔레그램 봇 생성 및 메시지 전송을 처리합니다.

---

## **주요 함수**


### **1. `handle_new_user(update, context)`**
- 새 사용자가 등록될 때 호출되는 함수
- **기능**:
   - telegram_alarm.py의 start 함수를 호출하여 새 사용자를 등록하고 고유한 센서 번호를 할당
   - 새로 할당된 센서 번호를 활성 센서 목록(active_sensors)에 추가
   - 등록 완료 후 periodic_check 함수를 호출하여 해당 센서에 대한 주기적 점검 시작
- **특이사항**:
   - 이 함수는 원래 telegram_alarm.py에 포함되어야 하지만, periodic_check 함수가 main.py에 정의되어 있기 때문에 main.py에 배치되어 있음.
   - periodic_check(senser_number) : 센서 상태 점검 및 이벤트 발생 시 알람 함수 호출



---

### **2. `start(update, context)`**
- 텔레그램 `/start` 명령어를 처리
- **기능**:
  - 새로운 사용자를 등록하고 고유 센서 번호를 할당
  - 기존 사용자라면 데이터베이스에서 센서 번호를 조회하여 반환

---
### **3. `send_alert(application, chat_id, message)`**
- 지정된 사용자(`chat_id`)에게 텔레그램 메시지를 전송
- **파라미터**:
  - `application`: 텔레그램 봇 인스턴스
  - `chat_id`: 사용자 고유 ID
  - `message`: 전송할 메시지 내용


---

### **4. `handle_car_stop(application, sensor_number)`**
- 차량 정차 감지 시 호출
- **기능**:
  - 센서 번호와 연결된 사용자를 찾아 "차량 정차" 알림 전송

---

### **5. `send_detection_alert(application, sensor_number)`**
- 고온 및 모션 감지 시 호출
- **기능**:
  - 위험 상황 발생 시 해당 센서와 연결된 사용자에게 텔레그램 메시지로 알림 전송

---

### **6. `create_telegram_app()`**
- 텔레그램 봇 애플리케이션을 초기화하고 설정

---

## **데이터베이스 구조**
- **테이블**: `users`
  - `sensor_number` (INTEGER): 고유 센서 번호 (Primary Key, Auto Increment).
  - `chat_id` (INTEGER): 텔레그램 사용자 고유 ID (Unique).

---

