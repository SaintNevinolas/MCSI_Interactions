import serial
import socket
import threading
from threading import Thread
from time import sleep

ser = serial.Serial("COM4", 9600)
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
        if sensorValues[0] =="G" : #ACCELERO
            data = b'P_LEFT'
            client_socket.sendto(data,address)
        else:
            data = b'R_LEFT'
            client_socket.sendto(data,address)
        if sensorValues[0] =="D" :
            data = b'P_RIGHT'
            client_socket.sendto(data,address)
        else:
            data = b'R_RIGHT'
            client_socket.sendto(data,address)
        
        if sensorValues[1] == "1" : #TOUCH Pour l'instant le touch fait avancer c'était pour tester
            data = b'P_ACCELERATE'
            client_socket.sendto(data,address)
        else : 
            data = b'R_ACCELERATE'
            client_socket.sendto(data,address)
        if sensorValues[1] == "0":
            data = b'P_BRAKE'
            client_socket.sendto(data,address)
        else:
            data = b'R_BRAKE'
            client_socket.sendto(data,address)

        #if sensorValues[2] == "1" : #PIEZO
        #    data = b'P_FIRE'
        #    client_socket.sendto(data, address)
        #    Thread(target=stop_fire).start()
        
        if sensorValues[3] == "1":
            data = b'NITRO'
            client_socket.sendto(data, address)