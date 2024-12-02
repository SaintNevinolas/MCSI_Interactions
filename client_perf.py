import serial
import socket
import threading
from threading import Thread
from time import sleep

ser = serial.Serial("COM5", 9600)
address = ('localhost', 6006)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def stop_fire():
    sleep(0.1)
    data = b'R_FIRE'
    client_socket.sendto(data, address)
sensorValues = {0,0,0,0}
while True:
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').strip()
        print(f"Recu : {data}")
        sensorValues = data.split(",",-1) # [Accelero,Touch,Piezo,UltraSonic]
        if sensorValues[2] == "1":
            data = b'P_SKIDDING'
            client_socket.sendto(data,address)
        else:
            data = b'R_SKIDDING'
            client_socket.sendto(data,address)