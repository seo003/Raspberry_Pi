# 통합 코드
## 📄 파일 구조
```
├── arduino/  
│   └── motion.ino           # 아두이노 설정 파일
├── config/                  # TinyOS 설정 파일
│   ├── Makefile
│   ├── Temperature.h
│   ├── TemperatureAppC.nc 
│   └── TemperatureC.nc  
├── database/  
│   └── users.db              # 데이터베이스
├── modules/  
│   ├── detect_move.py        # 가속도 감지
│   ├── motion.py             # 모션 감지
│   ├── telegram_alarm.py     # 텔레그램
│   └── temperature_check.py  # 온도 감지
└── main.py  
```

## Main.py
### 1. 텔레그램 봇 생성 및 모듈 초기화
   - 필요한 모듈들을 초기화하고, 텔레그램 봇 생성
```
application = telegram_alarm.create_telegram_app()

motion_detector = MotionDetector()
temp_checker = TemperatureChecker()
```

### 2. Telegram Bot Polling 시작
  - 텔레그램 봇은 `Polling` 모드를 통해 명령어를 기다리고 처리
  - `/start` 명령어가 들어오면 `handle_new_user` 함수 실행
```
await application.run_polling(allowed_updates=telegram_alarm.Update.ALL_TYPES)
```

### 3. 센서 감지 (periodic_check)
   - 주기적으로 센서를 감지하여 알림 전송

      1. **차량 정차 감지**: `detect_move.py`의 `monitor_motion_and_stop()` 함수가 호출되어 차량이 정차했는지 감지하고, 그 결과로 True 또는 False 반환
       2. **온도 감지**: `temp_checker`의 `check_temperature()` 함수가 호출되어 온도를 측정하고, 온도가 30도 이상이면 `True` 반환
       3. **모션 감지**: `motion_detector`의 `detect_motion()` 함수가 호출되어 총 3번의 모션을 감지하고, 감지되면 `True` 반환

### 4. 알림 전송 및 대기
   차량 정차, 온도 감지, 모션 감지가 모두 `True`일 경우 텔레그램 봇을 통해 알림을 전송하고, 1시간 동안 대기합니다. 이후 다시 감지가 시작됩니다.


## ⚙️ 작동 흐름
사용자가 /start 명령어를 입력  
➡️ 사용자 등록 및 센서 번호 할당

센서 감지 및 알림 전송   
➡️ 차량 정차, 고온 감지, 모션 감지를 순차적으로 수행하고, 해당 상태에 따라 알림 전송

알림을 받으면 사용자가 적절히 대처할 수 있도록 안내  
➡️ 사용자가 알림을 확인하고 대처 


## 📺 실행 화면

### 📱 텔레그램 실행 화면
| DB에 사용자가 없을 시 | DB에 사용자가 존재할 시 | 
| --- | --- | 
| ![telegramStart](https://github.com/user-attachments/assets/26bccb5e-dc7b-4a8c-8796-9b7552194f2a) | ![telegramAlready](https://github.com/user-attachments/assets/58edcaf4-ae33-4429-91bc-680984cc1dd8) |

### 💻 CMD 디버깅 코드
| 사용자 등록 및 가속도 센서 | 
| --- |
| ![start](https://github.com/user-attachments/assets/2ec315bb-5994-401f-aa80-5159e96a9036) | 
| <center>**온도 감지**</center> | 
| ![temperature](https://github.com/user-attachments/assets/cd4fdb4b-1796-49b9-b085-98db8830ff43) | 8 | 9 |
| <center>**모션 감지**</center> | 
| ![motion](https://github.com/user-attachments/assets/0809d3a7-d03d-4eeb-b870-196e237a397a) | 8 | 9 |


