# 모션감지


## 모션감지센서 (5.8Ghz 마이크로웨이브 레이더 모션 센서 -6-9미터)
![0000608-1](https://github.com/user-attachments/assets/aeef4bc2-96c4-4b43-9b89-9e00ac0165f7)


- 출처: [가치창조기술](https://vctec.co.kr/product/58ghz%EB%A7%88%EC%9D%B4%ED%81%AC%EB%A1%9C%EC%9B%A8%EC%9D%B4%EB%B8%8C-%EB%A0%88%EC%9D%B4%EB%8D%94-%EB%AA%A8%EC%85%98-%EC%84%BC%EC%84%9C-6-9%EB%AF%B8%ED%84%B0-microwave-58ghz-radar-motion-sensor-6-9m/17838/category/145/display/1/)



## Wiring Connections   

| Sensor | Arduino PIN | 
| --- | --- |
| +VIN | +5V |
| GND | GND | 
| OUTPUT | D2 |

<br>

## PIP LIST

- `pip install pyserial`   

<br>


## Arduino (motion.ino)

<p> D2번핀에서 모션감지가 되면 1, 감지가 안 되면 0

- `int Output = 2;`
 
- `int SensorVal = digitalRead(Output);`

<br>   
   
## Python (motion.py)
### **def** detect_motion() 
<p> 모션센서에서 3번 연속 감지되면 True를 반환합니다. 

- `sensor_val`은 D2핀에서 받은 값을 읽어 저장
- `self.motion_count`는 `sensor_val`가 1이 될 때마다 증가되고,  연속으로 3번 감지되어<br> 
 `self.motion_count`가 3이 되면 True를 반환 

---
