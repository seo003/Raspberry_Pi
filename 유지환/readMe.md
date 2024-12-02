# 차량 움직임 감지 시스템
이 프로젝트는 운전자가 차량을 정차하고 떠난 상태를 정확히 감지한 뒤, 운전자가 운전을 하지 않을때에만 감지를 하도록 합니다. 이를 통해 불필요한 경고를 방지하고, 실제로 필요한 상황에만 알림을 제공하여 사용자 편의성과 신뢰성을 동시에 보장합니다.

## :clipboard:주요 기능
- 운전자 상태 감지<br>
  차량 내에서 운전자가 부재 중인지 실시간으로 감지하여 움직임 감지와 온도 감지를 활성화하거나 비활성화합니다.
- 실시간 데이터 처리 및 기록<br>
  가속도 데이터를 기반으로 차량 내부의 미세한 움직임까지 감지하여, 허위 경고를 줄이고 정확성을 높입니다.
- 움직임 감지<br>
  Raspberry Pi에서 수집된 데이터를 실시간으로 분석하여 움직임과 환경 조건을 평가하고, 결과를 로그로 저장합니다.

$ \text{total\_acceleration} = \sqrt{X^2 + Y^2 + Z^2} $


## pip
- pip install adafruit-blinka
- pip install adafruit-circuitpython-adxl34x
- sudo apt-get install python3-dev python3-pip python3-smbus i2c-tools -y
