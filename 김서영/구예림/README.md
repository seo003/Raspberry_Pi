# 온도 측정 모니터링

## 필요 라이브러리 설치

```
pip install pytos
```


## 파일 구조
. <br>
├── Makefile                   # TinyOS 애플리케이션 빌드 <br>
├── Temperature.h           # 온도 데이터의 메시지 구조 및 상수 정의 <br>
├── TemperatureAppC.nc      # TinyOS 애플리케이션의 구성 파일 <br>
├── TemperatureC.nc         # 온도 측정 및 데이터 전송을 수행하는 모듈 구현<br>
├── temperature_check.py    # Zigbee 모듈로부터 데이터 수신 및 분석

### 파일 별 설명
#### 1. Makefile
- TinyOS 애플리케이션 빌드 설정 파일
- COMPONENT=TemperatureAppC: 컴포넌트의 진입점을 TemperatureAppC로 지정
- include $(MAKERULES): TinyOS에서 제공하는 기본 Makefile 규칙을 포함

#### 2. Temperature.h
- Zigbee 메시지 구조 및 상수를 정의한 헤더 파일
- 주요 정의:
   > **`NREADINGS`**: 메시지당 온도 데이터의 샘플 개수(10개) <br>
  **`DEFAULT_INTERVAL`**: 기본 샘플링 주기(256ms) <br>
  **`oscilloscope_t`**: 메시지 구조체로, 센서 ID, 샘플링 주기, 온도 데이터 배열 등 포함

#### 3. TemperatureAppC.nc
- TinyOS 애플리케이션의 구성 파일입니다.
- 구성요소:
  > **`TemperatureC`**: 온도 데이터를 처리하는 핵심 모듈<br>
  **`MainC`**: 시스템 초기화 담당<br>
  **`ActiveMessageC`**: 메시지 송수신 관리<br>
  **`AMSenderC`**: Zigbee 메시지 송신

#### 4. TemperatureC.nc
- 온도 측정, 데이터 저장, 무선 전송을 담당하는 TinyOS 모듈
- 주요 로직:
  1. 시스템 초기화:
      - 시스템 부팅 시 Boot.booted 이벤트 실행
      -  샘플링 주기 설정, 무선 모듈 초기화, 타이머 시작
  2. 타이머 이벤트:
      - Timer.fired 이벤트에서 온도 데이터를 주기적으로 측정
  3. 온도 데이터 처리:
      - 온도 데이터를 배열에 저장
      - 배열이 가득 차면 Zigbee를 통해 데이터 전송
  4. 데이터 전송 완료:
      - AMSend.sendDone 이벤트로 전송 완료 상태를 확인

#### 5. temperature_check.py
- Zigbee 모듈을 통해 수신된 데이터 분석
- 주요 기능:
    1. Zigbee 메시지를 수신하고 파싱
    2. 온도가 30도 이상인지 확인


## 함수
### TemperatureC.nc
- **`Boot.booted`**: 시스템 초기화 후 실행되는 이벤트
- **`Timer.fired`**: 타이머 주기마다 실행, 온도 데이터를 읽음
- **`Read.readDone`**: 온도 데이터가 읽혀질 때 실행, 배열에 저장

### temperature_check.py
- **`isOver30Degree(data0)`**: 온도 값이 30도 이상인지 확인
- **`check_temperature()`**: Zigbee 메시지를 읽고 데이터를 출력 및 분석
