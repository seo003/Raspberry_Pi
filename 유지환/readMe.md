# 차량 움직임 감지 시스템
이 프로젝트는 운전자가 차량을 정차하고 떠난 상태를 정확히 감지한 뒤, 운전자가 운전을 하지 않을 때에만 감지를 하도록 설계되었습니다. 이를 통해 불필요한 경고를 방지하고, 실제로 필요한 상황에만 알림을 제공하여 사용자 편의성과 신뢰성을 동시에 보장합니다.

## :clipboard: 주요 기능

### 1. 운전자 상태 감지
- 차량 내에서 운전자가 부재 중인지 실시간으로 감지하여 자동으로 움직임 감지와 온도 감지 기능을 활성화하거나 비활성화합니다.

### 2. 실시간 데이터 처리
- 가속도 데이터를 기반으로 차량 내부의 미세한 움직임까지 감지하여 허위 경고를 줄이고 정확성을 높입니다.

### 3. 움직임 감지
- Raspberry Pi에서 수집된 가속도 데이터를 실시간으로 분석하여 차량의 이동 여부를 판단하고, 즉각적으로 센서를 작동시킵니다.

## :bulb: 데이터 흐름

![1](/유지환/가속도데이터전송.png)

1. **데이터 수집**
   - 가속도 센서는 X, Y, Z 축의 가속도 데이터를 실시간으로 측정하여 Raspberry Pi로 전송합니다.

2. **데이터 처리**
   - Raspberry Pi는 수신된 데이터를 기반으로 가속도 값을 계산하고 이를 통해 차량 내 움직임 여부를 분석합니다. 가속도는 다음과 같이 계산됩니다:

     $$
     \text{가속도} = \sqrt{X^2 + Y^2 + Z^2}
     $$

     이후, 움직임 여부를 판단하기 위한 임계값을 12g로 설정하여 그 값을 초과할 경우 움직임이 감지된 것으로 간주합니다.

3. **센서 감지**
   - 가속도가 3분 이상 12g를 초과하지 않았다면 운전자가 없다고 판단하여 움직임 감지 시스템과 온도 감지 시스템을 활성화합니다.
   - 5초 이상 가속도가 12g 이상이라면 센서 감지를 비활성화하여 불필요한 경고를 방지합니다.


# 📚 코드 설명
* 모듈 및 라이브러리 임포트
    * `asyncio`: 비동기 프로그래밍을 위한 라이브러리로, 여러 작업을 효율적으로 동시에 실행할 수 있게 합니다.
    * `time`: 시간 측정 및 대기 처리를 위한 모듈입니다.
    * `board`: Raspberry Pi의 핀 설정을 다루는 라이브러리로 I2C 통신을 설정하는 데 사용됩니다.
    * `adafruit_adxl34x`: ADXL345 가속도 센서를 제어하기 위한 Adafruit 제공 라이브러리입니다.
  ```python
  import asyncio
  import time
  import board
  import adafruit_adxl34x
  ```
<br>

* I2C 통신 및 센서 초기화
  * `i2c`: I2C 통신 객체를 생성합니다.
  * `sensor`: ADXL345 가속도 센서를 I2C 통신으로 초기화합니다.
  ```python
  i2c = board.I2C()
  sensor = adafruit_adxl34x.ADXL345(i2c)
  ```
<br>

* 변수 설정
  * `motion_detected`: 현재 움직임 상태를 나타냅니다. 움직임이 감지되면 True, 그렇지 않으면 False입니다.
  * `motion_start_time`: 움직임이 시작된 시간을 기록합니다.
  * `stop_start_time`: 정지 상태가 시작된 시간을 기록합니다.
  * `is_move`: 차량이 움직이는지 여부를 나타냅니다. 움직임이 지속되면 True, 정지 상태가 지속되면 False입니다.
  * `MOTION_THRESHOLD`: 움직임으로 간주되는 가속도의 임계값(12g)입니다.
  * `STOP_DURATION`: 정지 상태로 간주되기 위한 지속 시간(3분)입니다.
  * `MOTION_DURATION`: 움직임으로 간주되기 위한 지속 시간(5초)입니다.
  ```python
  motion_detected = False
  motion_start_time = None
  stop_start_time = None
  is_move = False
  
  MOTION_THRESHOLD = 12  # 움직임 감지 기준 (12g 이상의 가속도)
  STOP_DURATION = 180  # 정지 상태 감지 시간 (3분)
  MOTION_DURATION = 5  # 움직임 감지 지속 시간 (5초)
  ```
<br>

* 가속도 데이터 읽기
  * `sensor.acceleration`: 센서로부터 X, Y, Z 축의 가속도를 읽어오고, 이를 사용해 총 가속도를 계산합니다.
  ```python
  x, y, z = sensor.acceleration
  total_acceleration = (x**2 + y**2 + z**2) ** 0.5
  ```
<br>

* 움직임 및 정지 상태 감지 함수
  * `if total_acceleration > MOTION_THRESHOLD:`: 현재의 가속도를 측정하여 현재 차량이 움직이고 있는지 감지합니다.
  * `time.time()`: 현재 시간을 반환하는 함수로, 차량의 움직임 시작 시간과 정지 시간을 기록하고, 두 시간 간의 차이를 계산하여 차량의 이동 여부와 정지 시간을 확인합니다.

  ```python
  if total_acceleration > MOTION_THRESHOLD:
              if not motion_detected:
                  motion_start_time = time.time()  # 움직임 시작 시간 기록
              motion_detected = True
              stop_start_time = None  # 정지 상태 초기화
  
              # 움직임이 5초 이상 지속되었는지 확인
              if motion_start_time and time.time() - motion_start_time >= MOTION_DURATION:
                  print("움직임 감지: 5초 이상 지속")
                  motion_start_time = None  # 상태 초기화
                  is_move = False
          else:
              # 움직임이 없는 상태
              motion_detected = False
              motion_start_time = None  # 움직임 초기화
  
              # 정지 상태 시작 시간 기록
              if stop_start_time is None:
                  stop_start_time = time.time()
              elif time.time() - stop_start_time >= STOP_DURATION:
                  print("정지 상태: 3분 이상 지속")
                  stop_start_time = None  # 상태 초기화
                  is_move = True
  ```


















## :sparkles: 실행 방법

1. **I2C 통신 활성화**
    - Interface Options -> I2C를 활성화합니다.

      ```bash
      sudo raspi-config
      ```

2. **재부팅**
    - 라즈베리 파이를 재부팅합니다.

      ```bash
      sudo reboot
      ```

3. **패키지 설치**
    - 가속도 센서 연결을 위해 패키지를 설치합니다.

      ```bash
      sudo apt-get install python3-dev python3-pip python3-smbus i2c-tools -y
      ```

4. **센서 연결**
    - 아래의 표대로 라즈베리 파이와 센서를 연결합니다.

      | ADXL345 핀 | Raspberry Pi 3 핀 |
      |------------|--------------------|
      | 5V         | 핀 2              |
      | GND        | 핀 6              |
      | SCL        | 핀 5              |
      | SDA        | 핀 3              |

5. **연결 확인**
    - 센서가 인식되었는지 확인합니다.

      ```bash
      sudo i2cdetect -y 1
      ```

6. **라이브러리 설치**
    - 필요한 라이브러리를 설치합니다.

      ```bash
      pip install adafruit-blinka
      pip install adafruit-circuitpython-adxl34x
      ```

7. **코드 실행**
    - 아래 명령어를 실행합니다.

      ```bash
      python motion_detect.py
      ```

8. **작동 확인**
    - 가속도가 실시간으로 출력됩니다.
    - 움직임이 감지되었는지 출력합니다.

## ⚙️ 주요 설정

- **가속도 임계값 (`MOTION_THRESHOLD`)**
    - 기본값: `10g`
    - 사용 환경에 따라 9.8 이상의 값으로 조정할 수 있습니다.

- **정지 시간 (`STOP_DURATION`)**
    - 기본값: `180`
    - 정차로 간주되기까지의 시간입니다.

- **이동 감지 시간 (`MOTION_DURATION`)**
    - 기본값: `5`
    - 이동이 감지되기까지의 시간입니다.
