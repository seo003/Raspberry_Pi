import serial
import time

#Receiving data from usb port 
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

try:
    while True:
        #Data receiving
        if ser.in_waiting > 0:
            sensor_val = ser.readline().decode('utf-8').strip()
            print("data : ", sensor_val)

    time.sleep(500);

#Keyboard Interrupt like " Ctrl + C "
except KeyboardInterrupt:
    print("program exit")

#Closing serial port
finally:
    ser.close()
