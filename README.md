# 무선 네트워크 프로젝트

본 프로젝트는 라즈베리파이를 사용하여 차량 내부의 온도를 감지하여 내부에 사람이 있을 시 자동차 소유자에게 알림을 주는 시스템이다. 

## 개요
주로 여름철에, 보호자의 부주의로 확인하지 못한 아이들이 내부 온도가 증가하는 자동차 안에 갇혀 열사병으로 사망하는 사례가 많이 발생한다. 
이 문제를 해결하기 위해 Zigbee 기반의 온도 감지 및 인체 감지 센서(LD2410)를 통합한 시스템을 개발하고자 한다.

## 역할(추후 수정)
- 김서영(202244005)
- 김윤호(202044012)
- 유지환()
- 임상운(202044024)

## 기능
1. 차 내부 온도 측정
<br> - Zigbee 기반으로 차 내부의 온도를 측정하여 일정 온도(30°) 이상으로 올라가는지 감지
2. 인체 감지
<br> - 1번 기능이 감지 된다면 LD2410를 활용하여 차 내부에 사람이 존재하는지 감지
3. 텔레그램 알림
<br> - 2번 기능이 감지된다면 텔레그램 봇으로 자동차 소유주에게 알림

