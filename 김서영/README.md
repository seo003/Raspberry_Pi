# 온도 데이터 수집 및 분석

## 💡 필요 라이브러리 설치

- TinyOS 네트워크 모듈과의 상호작용을 위한 라이브러리 설치    
ex) Zigbee

  ```
  pip install pytos
  ```

## 📋 파일 설명

### 1. Makefile
- TinyOS 애플리케이션 빌드 설정 파일
- COMPONENT=TemperatureAppC: 컴포넌트의 진입점을 TemperatureAppC로 지정
- include $(MAKERULES): TinyOS에서 제공하는 기본 Makefile 규칙을 포함

### 2. Temperature.h
- Zigbee 메시지 구조 및 상수를 정의한 헤더 파일
- 주요 정의:
   > **`NREADINGS`**: 메시지당 온도 데이터의 샘플 개수(10개) <br>
  **`DEFAULT_INTERVAL`**: 기본 샘플링 주기(256ms) <br>
  **`oscilloscope_t`**: 메시지 구조체로, 센서 ID, 샘플링 주기, 온도 데이터 배열 등 포함

### 3. TemperatureAppC.nc
- TinyOS 애플리케이션의 구성 파일입니다.
- 구성요소:
  > **`TemperatureC`**: 온도 데이터를 처리하는 핵심 모듈<br>
  **`MainC`**: 시스템 초기화 담당<br>
  **`ActiveMessageC`**: 메시지 송수신 관리<br>
  **`AMSenderC`**: Zigbee 메시지 송신

### 4. TemperatureC.nc
- 온도 측정, 데이터 저장, 무선 전송을 담당하는 TinyOS 모듈
- 주요 로직:
  1. 시스템 초기화
  2. 타이머 이벤트
  3. 온도 데이터 처리
  4. 데이터 전송 완료

### 5. temperature_check.py
- Zigbee 모듈을 통해 수신된 데이터 분석
- 주요 기능:
    1. Zigbee 메시지를 수신하고 파싱
    2. 온도가 30도 이상인지 확인


## 🔗 함수

### temperature_check.py
- **`isOver30Degree(data0)`**: 온도 값이 30도 이상인지 확인
- **`check_temperature()`**: Zigbee 메시지를 읽고 데이터를 출력 및 분석
