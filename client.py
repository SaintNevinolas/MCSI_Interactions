import serial

ser = serial.Serial("COM5", 9600)

while True:
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').strip()
        print(f"Recu : {data}")